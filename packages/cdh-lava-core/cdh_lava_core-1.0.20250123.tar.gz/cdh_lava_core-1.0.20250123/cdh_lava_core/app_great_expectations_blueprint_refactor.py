import os
import sys
import traceback
from flask import Blueprint, render_template_string
from flask import render_template, request, make_response
from flask_restx import Resource, Api
import pandas as pd
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.core import RunIdentifier, ValidationDefinition
from great_expectations.exceptions import DataContextError
from great_expectations.data_context.types.base import DataContextConfig, FilesystemStoreBackendDefaults
from great_expectations.core.batch import BatchRequest
from great_expectations.expectations.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import SparkDFExecutionEngine

from typing import Dict, Any, Union, List, Optional
from datetime import datetime
from cdh_lava_core.app_shared_dependencies import get_config
from cdh_lava_core.az_key_vault_service import az_key_vault as cdh_az_key_vault
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_metadata_service import environment_metadata as cdc_env_metadata
import csv
from dotenv import load_dotenv
from pathlib import Path
import math
from databricks.connect import DatabricksSession
from sqlalchemy import create_engine
import json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, LongType, DoubleType, TimestampType
from pyspark.sql.functions import lit, regexp_extract, when
import uuid
from pydantic import BaseModel, Field
from copy import deepcopy


great_expectations_bp = Blueprint('great_expectations', __name__)

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(great_expectations_bp)  # Initialize Api with the blueprint
ENVIRONMENT = "dev"  # Set the environment name
DATA_PRODUCT_ID = "lava_core"

tracer, logger = LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
).initialize_logging_and_tracing()

# Helper function to validate SQL identifiers
def valid_sql_identifier(identifier):
    """Check if the identifier is a valid SQL name that isn't 'nan' or None."""
    if pd.isna(identifier) or identifier.strip() == "" or identifier.lower() == "nan":
        return False
    return True

def update_html(raw_html):
    # Step 1: Replace "Show Walkthrough" with "Run Tests"
    updated_html = raw_html.replace("Show Walkthrough", "Run Tests")

    # Step 2: Replace modal trigger with form submission action
    updated_html = updated_html.replace(
        'data-toggle="modal" data-target=".ge-walkthrough-modal"',
        'onclick="document.getElementById(\'myForm\').submit();"'
    )

    # Step 3: Replace "<strong>Actions</strong>" with form tag
    updated_html = updated_html.replace(
        "<strong>Actions</strong>",
        '<form id="myForm" method="post"></form>'
    )

    # Step 4: Update button type to "submit" within the form
    updated_html = updated_html.replace(
        '<button type="button" class="btn btn-info"',
        '<div><button onclick="history.back()" class="btn btn-secondary   w-200  " style="height:50px">Back</button></div><br>&nbsp;&nbsp;<br><button type="submit" style="height:50px" class="btn btn-info w-200 "'
    )

    return updated_html

def get_parent_directory():
    """Retrieve the parent directory of the current file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, os.pardir))

def get_csv_data(csv_path):
    """Read CSV data and return as list of dictionaries."""
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

def is_valid_string(s):
    """
    Check if the given variable is a valid string.
    A valid string is defined as:
    - An instance of the str class
    - Non-empty
    - Not equal to "NaN" (case insensitive)
    Args:
        s (any): The variable to check.
    Returns:
        bool: True if the variable is a valid string, False otherwise.
    """

    return isinstance(s, str) and bool(s) and s.strip().lower() != "nan"


def split_and_clean(input_string, delimiter=',', strip_whitespace=True, remove_empty=True):
    """
    Splits the input string by the specified delimiter and optionally strips whitespace and removes empty items.

    Args:
        input_string (str): The string to be split and cleaned.
        delimiter (str, optional): The delimiter to split the string by. Defaults to ','.
        strip_whitespace (bool, optional): Whether to strip leading and trailing whitespace from each item. Defaults to True.
        remove_empty (bool, optional): Whether to remove empty items from the result. Defaults to True.

    Returns:
        list: A list of cleaned items from the input string.
    """

    if strip_whitespace:
        items = [item.strip() for item in input_string.split(delimiter)]
    else:
        items = input_string.split(delimiter)
    if remove_empty:
        items = [item for item in items if item]
    return items


def initialize_file_context(expectations_dir, data_product_id):
    """
    Initialize the Great Expectations file context for a given data product.

    This function sets up the necessary directory structure and configuration for Great Expectations
    to manage expectations, validation results, validation definitions, and checkpoints. If the 
    specified expectations directory does not exist, it will be created along with the required 
    subdirectories.

    Args:
        expectations_dir (str): The directory where Great Expectations configurations and results will be stored.
        data_product_id (str): The identifier for the data product, used to construct the path to the expectations directory.

    Returns:
        DataContext: The initialized Great Expectations DataContext.
    """

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
    logger.info(f"expectations_dir:{expectations_dir}")
    if not os.path.exists(expectations_dir):
        os.makedirs(expectations_dir, exist_ok=True)
        ## Define the store backend
        ## Define the validations store configuration

        # Create DataContextConfig with the validations store
        context_config = DataContextConfig(
            stores={
                    "expectations_store": {
                        "class_name": "ExpectationsStore",
                        "store_backend": {
                            "class_name": "TupleFilesystemStoreBackend",
                            "base_directory": f"{expectations_dir}/expectations/"
                        }
                    },
                    "validation_results_store": {
                        "class_name": "ValidationResultsStore",
                        "store_backend": {
                            "class_name": "TupleFilesystemStoreBackend",
                            "base_directory": f"{expectations_dir}/uncommitted/validations/"
                        }
                    },
                    "validation_definition_store": {
                        "class_name": "ValidationDefinitionStore",
                        "store_backend": {
                            "class_name": "TupleFilesystemStoreBackend",
                            "base_directory": f"{expectations_dir}/validation_definitions/"
                        }
                    },
                    "checkpoint_store": {
                        "class_name": "CheckpointStore",
                        "store_backend": {
                            "class_name": "TupleFilesystemStoreBackend",
                            "base_directory": f"{expectations_dir}/checkpoints/"
                        }
                    }
                },
            data_docs_sites={
                "local_site": {
                    "class_name": "SiteBuilder",
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": f"{expectations_dir}/uncommitted/data_docs/local_site"
                    },
                    "site_index_builder": {
                        "class_name": "DefaultSiteIndexBuilder"
                    }
                }
            },
                store_backend_defaults=FilesystemStoreBackendDefaults(
        root_directory=expectations_directory_path
    ))
        context =  gx.get_context(context_config)
        logger.info(f"Great Expectations project initialized at: {expectations_dir}")
    else:
        context =  gx.get_context(context_root_dir=expectations_directory_path)
        logger.info(f"Great Expectations project already exists at: {expectations_dir}")
    return context

def validate_with_run_id(context, data_asset_name, expectation_suite, batch_definition, batch_parameters):
    """
    Validate a data asset using a specific expectation suite and batch definition, and run the validation with a unique run ID.

    Args:
        context (DataContext): The Great Expectations DataContext object.
        data_asset_name (str): The name of the data asset to be validated.
        expectation_suite (ExpectationSuite): The expectation suite to validate against.
        batch_definition (BatchDefinition): The batch definition for the data asset.
        batch_parameters (dict): Additional parameters for the batch.

    Returns:
        ValidationResults: The results of the validation run.
    """

    with tracer.start_as_current_span("validate_with_run_id"):
        try:

            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            suite_name = expectation_suite.name
            run_name = f"{data_asset_name}_validation_{suite_name}_{current_time}"

            validation_definition = ValidationDefinition(
                name=run_name,
                data=batch_definition,  # The active batch being validated
                suite=expectation_suite
            )

            # Add ValidationDefinition to the context
            try:
                context.validation_definitions.add(validation_definition)
            except DataContextError as e:
                # Handle existing definition, perhaps update or recreate
                context.validation_definitions.remove(run_name)
                context.validation_definitions.add(validation_definition)

            # Create a list of Actions for the Checkpoint to perform
            action_list = [
                # This Action updates the Data Docs static website with the Validation
                #   Results after the Checkpoint is run.
                gx.checkpoint.UpdateDataDocsAction(
                    name="update_all_data_docs",
                ),
            ]


            # Create a list of one or more Validation Definitions for the Checkpoint to run
            validation_definitions = [
                context.validation_definitions.get(run_name)
            ]

            # Create the Checkpoint
            checkpoint_name = f"{run_name}_checkpoint"
            checkpoint = gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=validation_definitions,
            actions=action_list,
            result_format={"result_format": "COMPLETE"},
            )

            # Save the Checkpoint to the Data Context
            context.checkpoints.add(checkpoint)

            # Run validation
            # validation_result = validator.validate()

            # Add run_id to the meta if not present to avoid KeyError
            # if "run_id" not in validation_result.meta:
            #    validation_result.meta["run_id"] = str(run_id)

            run_id = RunIdentifier(run_name=run_name)

            validation_results = checkpoint.run(
                batch_parameters=batch_parameters,
                run_id=run_id
            )

            return validation_results
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def configure_data_docs(context, expectations_dir):
    """
    Configures and builds data documentation sites for the given Great Expectations context.

    This function checks if there are any existing data documentation sites configured in the 
    Great Expectations context. If not, it sets up a local data documentation site using 
    TupleFilesystemStoreBackend and DefaultSiteIndexBuilder. It then adds this site configuration 
    to the context and builds the data documentation.

    Args:
        context (DataContext): The Great Expectations context to configure.
        expectations_dir (str): The directory where the expectations are stored.

    Returns:
        None
    """

    data_docs_sites = context.get_config().data_docs_sites
    if not data_docs_sites:
        data_docs_sites = {
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder"
                }
            }
        }
        context.add_data_docs_site(name="local_site", site_config=data_docs_sites["local_site"])
        logger.info("Data Docs site configuration added.")
    context.build_data_docs()


def manage_expectation_suite(context, suite_name):
    """
    Manages an expectation suite within the given Great Expectations context.

    This function attempts to retrieve an existing expectation suite by name. If the suite does not exist,
    it creates a new one, adds it to the context, and saves it.

    Args:
        context (DataContext): The Great Expectations context to manage the suite in.
        suite_name (str): The name of the expectation suite to manage.

    Returns:
        ExpectationSuite: The managed expectation suite.

    Raises:
        DataContextError: If there is an error accessing the context or suite.
    """

    with tracer.start_as_current_span(f"manage_expectation_suite for suite_name: {suite_name}"):
        try:

            # Retrieve an Expectation Suite from the Data Context
            existing_suite_name = (
            suite_name  # replace this with the name of your Expectation Suite
            )
            suite = context.suites.get(name=suite_name)

            logger.info(f"Loaded existing suite '{existing_suite_name}'")
            return suite

        except DataContextError as e:
            # If the suite does not exist, create a new one
            logger.warning(f"Suite '{suite_name}' not found; creating a new one.")

            suite = gx.ExpectationSuite(name=suite_name)

            # Add the Expectation Suite to the Data Context
            suite = context.suites.add(suite)

            logger.info(f"Created and added new suite '{suite_name}'")
            return suite
        
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message)
            raise Exception(error_message)

        return suite

def setup_spark_data_source(context, data_product_id):
    """
    Sets up a Spark data source in the given context based on the provided data product ID.

    This function retrieves configuration settings, extracts metadata, and attempts to retrieve
    an existing Spark data source. If the data source does not exist, it creates a new one.

    Args:
        context (DataContext): The Great Expectations context in which to set up the data source.
        data_product_id (str): The identifier for the data product, expected to be in the format "root_individual".

    Returns:
        tuple: A tuple containing:
            - data_source (DataSource): The configured Spark data source.
            - data_source_name (str): The name of the data source.
            - catalog_name (str): The catalog name extracted from the database name.
            - schema_name (str): The schema name extracted from the database name.
    """

    master_config = get_config()
    obj_env_metadata = cdc_env_metadata.EnvironmentMetaData()
    data_product_id_root = data_product_id.split("_")[0]
    data_product_id_individual = data_product_id.split("_")[1]
    repository_path_default = master_config.get("repository_path")
    running_local = master_config.get("running_local")
    environment = master_config.get("environment")

    parameters = {
    "data_product_id": data_product_id,
    "data_product_id_root": data_product_id_root,
    "data_product_id_individual": data_product_id_individual,
    "environment": environment,
    "repository_path": repository_path_default,
    "running_local": running_local,
    }
    logger.info(f"parameters: {parameters}")
    config = obj_env_metadata.get_configuration_common(
    parameters, None, data_product_id, environment
    )

    database_name = config.get("cdh_database_name")
    logger.info(f"database_name:{database_name}")
    catalog_name = database_name.split(".")[0]
    schema_name = database_name.split(".")[1]
    data_source_name = f"{database_name}"

    data_source = None
    try:
        # Attempt to retrieve the datasource
        data_source = context.data_sources.get(data_source_name)
        logger.info(f"Data source '{data_source_name}' already exists.")
    except (KeyError,ValueError):
        # If datasource is not found, create it
        data_source = context.data_sources.add_spark(name=data_source_name)
        logger.info(f"Created new data source '{data_source_name}'")

    return data_source, data_source_name, catalog_name, schema_name


def setup_sql_alchemy_data_source(data_product_id):
    """Retrieve or create a Databricks data source."""
    try:

        master_config = get_config()
        obj_env_metadata = cdc_env_metadata.EnvironmentMetaData()
        data_product_id_root = data_product_id.split("_")[0]
        data_product_id_individual = data_product_id.split("_")[1]
        repository_path_default = master_config.get("repository_path")
        running_local = master_config.get("running_local")
        environment = master_config.get("environment")

        parameters = {
        "data_product_id": data_product_id,
        "data_product_id_root": data_product_id_root,
        "data_product_id_individual": data_product_id_individual,
        "environment": environment,
        "repository_path": repository_path_default,
        "running_local": running_local,
        }
        config = obj_env_metadata.get_configuration_common(
        parameters, None, data_product_id, environment
        )

        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        environment = config.get("cdh_environment")
        client_secret = config.get("client_secret")
        tenant_id = config.get("az_sub_tenant_id")
        client_id = config.get("az_sub_client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        running_interactive = False
        if not client_secret:
            running_interactive = True

        az_sub_web_client_secret_key = config.get(
        "az_sub_web_client_secret_key"
        )
        obj_az_keyvault = cdh_az_key_vault.AzKeyVault(
        tenant_id,
        client_id,
        client_secret,
        az_kv_key_vault_name,
        running_interactive,
        data_product_id,
        environment,
        az_sub_web_client_secret_key,
        )

        database_name = config.get("cdh_database_name")
        catalog_name = database_name.split(".")[0]
        schema_name = database_name.split(".")[1]

        data_source_name = database_name
        host_name = config.get("cdh_databricks_instance_id")
        token_key = config.get("cdh_databricks_pat_secret_key")
        token = obj_az_keyvault.get_secret(token_key)
        http_path = config.get("cdh_databricks_endpoint_path_sql")
        # Set environment variables dynamically
        os.environ["DATABRICKS_TOKEN"] = token
        os.environ["DATABRICKS_HTTP_PATH"] = http_path

        connection_string = (
        f"databricks://token:{token}@{host_name}:443?http_path={http_path}&catalog={catalog_name}&schema={schema_name}"
        )
        data_source = None
        # try:
        #     # Attempt to retrieve the datasource
        #     data_source = context.data_sources.get(data_source_name)
        #     logger.info(f"Data source '{data_source_name}' already exists.")
        # except (KeyError,ValueError):
        #     # If datasource is not found, create it
        #     logger.info(f"connection_string: {connection_string}")
        #     data_source = context.data_sources.add_databricks_sql(
        #         name=data_source_name,
        #         connection_string=connection_string
        #     )
        #     logger.info(f"Created new data source '{data_source_name}'")

        engine = create_engine(connection_string)

        return  data_source_name, catalog_name, schema_name, engine, connection_string
    except DataContextError as e:
        logger.error(f"Failed to retrieve or create data source '{data_source_name}': {e}")
        return None


def get_raw_file(file_system: str, file_name: str) -> str:
    """
    Reads the content of a file from the specified directory and returns it as a string.

    Args:
        file_system (str): The directory path where the file is located.
        file_name (str): The name of the file to read.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        logger.info("get_raw_file")
        file_path = os.path.join(file_system, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def setup_and_get_batch(context, dataset_name, data_asset_name, catalog_name, schema_name, data_access_method, data_source, data_set_sql):
    with tracer.start_as_current_span("setup_and_get_batch"):
        try:
            logger.info(f"setup_and_get_batch: {dataset_name}")

            # Fetch or create data asset
            try:
                data_asset = data_source.get_asset(data_asset_name)
            except (LookupError):
                if data_access_method == "spark_dataframe":
                    data_asset = data_source.add_dataframe_asset(name=data_asset_name)
                else:
                    data_asset = data_source.add_table_asset(name=data_asset_name, table_name=dataset_name)

            # Prepare batch definition and request
            if data_access_method == "spark_dataframe":
                batch_definition_name = f"{dataset_name}_batch_definition"
                spark = DatabricksSession.builder.getOrCreate()
                dataframe = spark.sql(data_set_sql)
                batch_parameters = {"dataframe": dataframe}
            else:
                batch_definition_name = f"{dataset_name}_batch_definition_sql_alchemy"
                batch_parameters = {}

            # Add or fetch batch definition
            try:
                batch_definition = data_asset.get_batch_definition(name=batch_definition_name)
                logger.info(f"fetched batch_definition: {batch_definition_name}")
            except (KeyError, ValueError):
                if data_access_method ==  "spark_dataframe":
                    batch_definition = data_asset.add_batch_definition_whole_dataframe (batch_definition_name)
                else:
                    batch_definition = data_asset.add_batch_definition_whole_table(batch_definition_name)
                logger.info(f"added batch_definition: {batch_definition_name}")

            if data_access_method == "spark_dataframe":
                batch_request = data_asset.build_batch_request(options={"dataframe": dataframe})
                batch = batch_definition.get_batch(batch_parameters=batch_parameters)
            else:
                batch = batch_definition.get_batch()
                batch_request = {}
                batch_parameters = None

            if not batch:
                logger.info("batch is None")
            return batch, batch_definition, batch_request, batch_parameters

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)


class GreatExpectationsHomeList(Resource):
    def get(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        csv_path = os.path.join(parent_dir, "lava_core", "bronze_great_expectations.csv")

        # Read the CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient="records")

        # Retrieve other parameters if needed
        calling_page_url = request.args.get("calling_page")

        # Render the template with the data
        return make_response(render_template('great_expectations/great_expectations_home.html',
                               data=data, calling_page_url=calling_page_url))


def add_data_asset(context, data_assets, data_asset_name, dataset_name, data_access_method, catalog_name, schema_name, data_source, data_set_sql):
    with tracer.start_as_current_span("add_data_asset"):
        try:

            logger.info(f"add_data_asset: {data_asset_name}")

            # Setup and get batch, batch_definition, and batch_request
            batch, batch_definition, batch_request, batch_parameters  = setup_and_get_batch(context, dataset_name, data_asset_name, catalog_name, schema_name, data_access_method, data_source, data_set_sql)
            #logger.info("Type of batch_definition: %s", type(batch_definition))

            # Check if the data asset does not exist
            if data_asset_name not in data_assets:
                data_assets[data_asset_name] = {
                    "batch": batch,
                    "batch_definition": batch_definition,
                    "batch_request": batch_request,
                    "batch_parameters": batch_parameters,
                    "suites": []  # Initialize an empty list to store suites
                }
                logger.info(f"Added new data asset: {data_asset_name}")
            else:
                logger.info(f"Data asset already exists: {data_asset_name}")

            return data_assets

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)


def add_or_update_suite(context, data_assets, data_asset_name, suite_name):
    with tracer.start_as_current_span("add_or_update_suite"):
        try:
            # Retrieve or create the expectation suite
            logger.info(f"manage_expectation_suite:{suite_name}")
            suite = manage_expectation_suite(context, suite_name)

            # Log the initial state of data_assets
            logger.info(f"Starting suite management for {data_asset_name}. Current suites: {len(data_assets.get(data_asset_name, {}).get('suites', []))}")

            # Ensure the suite object is valid
            if suite is None:
                raise ValueError(f"Provided suite for {data_asset_name} is None")

            if data_asset_name in data_assets:
                existing_suites = data_assets[data_asset_name].get("suites", [])
                found = False
                for index, existing_suite in enumerate(existing_suites):
                    if existing_suite.name == suite_name:
                        # Log before updating
                        logger.info(f"Found existing suite {suite_name} in {data_asset_name}. Updating...")
                        existing_suites[index] = suite
                        found = True
                        break

                if not found:
                    # Log before adding new suite
                    logger.info(f"No existing suite matched in {data_asset_name}. Adding new suite...")
                    existing_suites.append(suite)

                # Log after modification
                logger.info(f"Updated suites in {data_asset_name}: {len(existing_suites)}")
                data_assets[data_asset_name]["suites"] = existing_suites

            else:
                # Log when creating new data asset
                logger.info(f"No data asset found for {data_asset_name}. Creating new data asset with suite.")
                data_assets[data_asset_name] = {"suites": [suite]}

            # Log the number of expectations in the new or updated suite
            expectations = suite.expectations
            logger.info(f"Final suite {suite_name} has {len(expectations)} expectations.")

            # Log final state of data assets
            logger.info(f"Final suites in {data_asset_name}: {len(data_assets[data_asset_name]['suites'])}")

            return data_assets

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)



def validate_suite(context, data_asset_name, suite, batch_definition, batch_parameters):
    with tracer.start_as_current_span("validate_suite"):
        try:
            suite.save()
            logger.info(f"Validating suite: {suite.name} in data asset: {data_asset_name}")

            validation_result = validate_with_run_id(context, data_asset_name, suite, batch_definition, batch_parameters)

            if validation_result:
                logger.info(f"Validation completed for suite: {suite.name}")
            else:
                logger.error(f"Validation failed or returned no results for suite: {suite.name}")

            return validation_result

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)



def validate_data_asset(context, data_asset_name, asset_details, batch_definition, batch_parameters):
    with tracer.start_as_current_span("validate_data_asset"):
        try:
            logger.info(f"validate_data_asset: {data_asset_name}")

            num_suites = len(asset_details['suites'])
            if num_suites == 0:
                logger.warning(f"No suites found for validation in data asset: {data_asset_name}")
                return []
            else:
                logger.info(f"{num_suites} suites found for validation in data asset: {data_asset_name}")

            asset_validation_results = []
            for suite in asset_details['suites']:
                validation_result = validate_suite(context, data_asset_name, suite, batch_definition, batch_parameters)
                asset_validation_results.append(validation_result)

            return asset_validation_results

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
          
def validate_all_assets(context, assets_details, batch_definition, batch_parameters):
    with tracer.start_as_current_span("validate_all_assets"): 	
        try:
            all_validation_results = {}
            for data_asset_name, asset_details in assets_details.items():
                asset_validation_results = validate_data_asset(context, data_asset_name, asset_details, batch_definition, batch_parameters)
                all_validation_results[data_asset_name] = asset_validation_results
                logger.info(f"Validation results stored for data asset: {data_asset_name}")

            return all_validation_results
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def validate_all_data_assets(context, data_assets):

    with tracer.start_as_current_span("validate_all_data_assets"): 	
        try:
            all_validation_results = {}

            # Loop through each data asset in the dictionary
            for data_asset_name, asset_details in data_assets.items():
                logger.info(f"Starting validation for data asset: {data_asset_name}")

                # Retrieve batch_definition and batch_parameters from the data asset
                batch_definition = asset_details.get('batch_definition')
                batch_parameters = asset_details.get('batch_parameters', {})
                # Log the number of suites about to be processed
                num_suites = len(asset_details.get('suites', []))
                logger.info(f"Found {num_suites} suites for data asset {data_asset_name}")

                # Initialize a list to store results for each suite in this data asset
                asset_validation_results = []

                if num_suites == 0:
                    logger.warning(f"No suites found for validation in data asset: {data_asset_name}")

                # Loop through each suite associated with the data asset
                for suite in asset_details['suites']:
                    suite.save()
                    logger.info(f"Validating suite: {suite.name} in data asset: {data_asset_name}")

                    # Perform validation using a function that runs validation and returns a result object
                    validation_result = validate_with_run_id(context, data_asset_name, suite, batch_definition, batch_parameters)
                    # Check if validation returned any results and log accordingly
                    if validation_result:
                        logger.info(f"Validation completed for suite: {suite.name}")
                    else:
                        logger.error(f"Validation failed or returned no results for suite: {suite.name}")
                    # Append the result to the asset's result list
                    asset_validation_results.append(validation_result)

                # Store results for this data asset in the main dictionary
                all_validation_results[data_asset_name] = asset_validation_results
                logger.info(f"Validation results stored for data asset: {data_asset_name}")

            return all_validation_results
        
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def safe_str(obj):
    """Safely convert object to string for logging"""
    try:
        return str(obj)
    except:
        return "Unable to convert to string"

def save_validation_results(
    catalog_name: str,
    schema_name: str,
    table_name_to_save: str,
    validation_results: Dict[str, Any],
    spark,
    snapshot_date,
    data_product_id,
    environment
) -> None:
    """
    Save Great Expectations validation results to a Delta table using Spark.

    Args:
        catalog_name (str): Name of the catalog
        schema_name (str): Name of the schema
        table_name (str): Name of the target table
        validation_results (Dict[str, Any]): Validation results from Great Expectations
        spark: Active SparkSession
    """
    try:
        logger.info(f"Starting validation results processing")
        data = []

        # Process each result in validation_results
        for result_key, checkpoint_result in validation_results.items():
            logger.info(f"Processing checkpoint result key: {result_key}")

            for item in checkpoint_result:
                logger.info("Processing checkpoint item")
                if hasattr(item, 'run_id'):
                    run_id_info = item.run_id
                    run_name = run_id_info.get('run_name', '') if isinstance(run_id_info, dict) else ''
                    run_time = run_id_info.get('run_time', '') if isinstance(run_id_info, dict) else ''
                    logger.info(f"Processing run_name: {run_name}")
                    # Access run_results from the CheckpointResult object
                    run_results = getattr(item, 'run_results', {})

                    # Process each validation result
                    for validation_id, validation_result in run_results.items():
                        # Convert ValidationResultIdentifier to string if necessary
                        validation_id_str = str(validation_id) if not isinstance(validation_id, str) else validation_id
                        results = validation_result.get('results', [])
                        meta = validation_result.get('meta', {})
                        logger.info(f"meta: {meta}")

                        data_asset_name = meta["active_batch_definition"]["data_asset_name"]
                        table_name = data_asset_name.split(":")[0] if ":" in data_asset_name else data_asset_name

                        # Parsed data without report_date
                        parsed_data = {
                            "data_asset_name": meta["active_batch_definition"]["data_asset_name"],
                            "data_connector_name": meta["active_batch_definition"]["data_connector_name"],
                            "datasource_name": meta["active_batch_definition"]["datasource_name"],
                            "ge_load_time": meta["batch_markers"].get("ge_load_time", "N/A"),
                            "validation_time": meta.get("validation_time", "N/A"),
                            "checkpoint_id": meta.get("checkpoint_id", "N/A"),
                            "great_expectations_version": meta.get("great_expectations_version", "N/A"),
                        }

                        run_id = meta.get("run_id", None)

                        if run_id is not None:
                            run_name = getattr(run_id, "run_name", "N/A")
                            run_time = getattr(run_id, "run_time", "N/A")
                        else:
                            run_name = "N/A"
                            run_time = "N/A"

                        for result in results:
                            try:
                                expectation_config = result.get('expectation_config', {})
                                result_dict = result.get('result', {})
                               # Extract result_format and expectation_name
                                result_format = expectation_config.get('kwargs', {}).get('result_format', {})
                                expectation_name = result_format.get('expectation_name', 'Unknown Expectation')
                                unexpected_rows_query  = result_format.get('unexpected_rows_query', 'Unknown unexpected_rows_query')
                                expectation_test_type = result_format.get('expectation_test_type', 'Unknown expectation_test_type')
                                # Convert all values to basic Python types
                                result_data = {
                                    "expectation_name": expectation_name,
                                    "unexpected_rows_query": unexpected_rows_query,
                                    "run_time": str(parsed_data.get("run_time", "")),
                                    "ge_load_time": str(parsed_data.get("ge_load_time", "")),
                                    "validation_time": str(parsed_data.get("validation_time", "")),
                                    "great_expectations_version": str(parsed_data.get("great_expectations_version", "")),
                                    "data_asset_name": str(parsed_data.get("data_asset_name", "")),
                                    'run_name': str(run_name) if run_name else '',
                                    'run_time': str(run_time) if run_time else '',
                                    'validation_id': validation_id_str,
                                    'expectation_id': str(expectation_config.get('id', '')),
                                    'type': str(expectation_config.get('type', '')),
                                    'column_name': str(expectation_config.get('kwargs', {}).get('column', '')),
                                    'success': bool(result.get('success', False)),
                                    'element_count': int(result_dict.get('element_count', 0)),
                                    'unexpected_count': int(result_dict.get('unexpected_count', 0)),
                                    'unexpected_percentage': float(result_dict.get('unexpected_percent', 0.0)),
                                    'mostly_threshold': float(expectation_config.get('kwargs', {}).get('mostly', 1.0)),
                                    'batch_id': str(expectation_config.get('kwargs', {}).get('batch_id', '')),
                                    'snapshot_date': snapshot_date,
                                    'data_product_id': data_product_id,
                                    'environment': environment,
                                    'table_name': table_name,
                                    'expectation_test_type': expectation_test_type
                                }

                                data.append(result_data)

                            except Exception as e:
                                logger.error(f"Error processing individual result: {str(e)}")
                                logger.error(f"Problematic result: {json.dumps(result, default=str)}")
                                continue
                else:
                    logger.warning("Result is missing run_id")

        if not data:
            logger.warning("No validation results found to process")
            return

        # Define schema with TimestampType for time fields, excluding `report_date`
        schema = StructType([
            StructField("expectation_name", StringType(), True),
            StructField("unexpected_rows_query", StringType(), True),
            StructField("run_name", StringType(), True),
            StructField("run_time", StringType(), True),  # Convert to TimestampType if needed
            StructField("validation_time", StringType(), True),  # Convert to TimestampType if needed
            StructField("ge_load_time", StringType(), True),  # Convert to TimestampType if needed
            StructField("great_expectations_version", StringType(), True),
            StructField("data_asset_name", StringType(), True),
            StructField("validation_id", StringType(), True),
            StructField("expectation_id", StringType(), True),
            StructField("type", StringType(), True),
            StructField("column_name", StringType(), True),
            StructField("success", BooleanType(), True),
            StructField("element_count", LongType(), True),
            StructField("unexpected_count", LongType(), True),
            StructField("unexpected_percentage", DoubleType(), True),
            StructField("mostly_threshold", DoubleType(), True),
            StructField("batch_id", StringType(), True),
            StructField("snapshot_date", StringType(), True),
            StructField("data_product_id", StringType(), True),
            StructField("environment", StringType(), True),
            StructField("table_name", StringType(), True),
            StructField("expectation_test_type", StringType(), True)
        ])

        # Create Spark DataFrame directly from the list of dictionaries with schema
        spark_df = spark.createDataFrame(data, schema=schema)
        # Extract date from batch_id if it ends with a date in YYYY-MM-DD format
        spark_df = spark_df.withColumn(
            "report_date",
            when(regexp_extract("batch_id", r"(\d{4}-\d{2}-\d{2})$", 1) != "", regexp_extract("batch_id", r"(\d{4}-\d{2}-\d{2})$", 1))
            .otherwise(lit(None))
        )

        target_table = f"{catalog_name}.{schema_name}.{table_name_to_save}"
        logger.info(f"Writing to Delta table: {target_table}")
        spark_df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .saveAsTable(target_table)
        logger.info(f"Successfully saved validation results to {target_table}")
    except Exception as e:
        logger.error(f"Error saving validation results: {str(e)}")
        logger.error("Full exception info:", exc_info=True)
        raise


def add_custom_value_set_expectation(suite, column, value_set, name=None, notes=None):
    """
    Create and add a value set expectation using the correct configuration format

    Args:
        suite: Great Expectations suite
        column: Column name or list of column names
        value_set: Set of values to check against
        name: Optional name for the expectation
        notes: Optional notes/query for the expectation
    """
    # Create the base configuration
    base_config = {
        "kwargs": {
            "column": column,
            "value_set": value_set,
            "result_format": {
                "result_format": "COMPLETE",
                "include_unexpected_rows": True
            }
        },
        "meta": {
            "name": name if name else "Column Value Set Validation",
            "notes": notes if notes else "",
            "basic_status": "active"
        }
    }

    try:
        # Create the expectation using positional arguments
        expectation = ExpectationConfiguration(
            type="expect_column_values_to_not_be_in_set",
            kwargs=base_config["kwargs"]
        )
        
        # Set metadata after creation
        expectation.meta = base_config["meta"]
        
        # Convert the expectation to a dictionary representation
        expectation_dict = {
            "type": "expect_column_values_to_not_be_in_set",
            "kwargs": deepcopy(base_config["kwargs"]),
            "meta": deepcopy(base_config["meta"])
        }
        
        # Create a new class to handle the configuration attribute
        class SerializableExpectationConfiguration(ExpectationConfiguration):
            @property
            def configuration(self):
                return {
                        "type": self._type,
                        "kwargs": deepcopy(self._kwargs),
                        "meta": deepcopy(self.meta)
                    }
                
            def to_dict(self):
                return self.configuration
        
        # Create a serializable version of the expectation
        serializable_expectation = SerializableExpectationConfiguration(
            type="expect_column_values_to_not_be_in_set",
            kwargs=base_config["kwargs"]
        )
        serializable_expectation.meta = base_config["meta"]
        
        # Update the suite's expectations list
        if not hasattr(suite, "expectations"):
            suite.expectations = []
        suite.expectations.append(serializable_expectation)
        
        return serializable_expectation
        
    except Exception as e:
        logger.error(f"Error creating expectation: {str(e)}")
        raise

class GreatExpectationHome(Resource):
    def get(self, data_product_id: str, text: str):
        with tracer.start_as_current_span("great_expectation"):
            try:
                # Setup paths and context
                parent_dir = get_parent_directory()
                expectations_dir = os.path.join(parent_dir, data_product_id, "gx")

                # Initialize context and data docs
                data_source_name, catalog_name, schema_name, engine, connection_string = setup_sql_alchemy_data_source(data_product_id)
                logger.info("initialize_file_context")
                context = initialize_file_context(expectations_dir, data_product_id)
                configure_data_docs(context, expectations_dir)

                default_path = os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                file_name = text

                raw_html = get_raw_file(default_path, file_name)
                updated_html_content = update_html(raw_html)
                return make_response(render_template_string(updated_html_content))

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                logger.error(error_message, exc_info=sys.exc_info())
                return make_response(render_template("error.html", error_message=error_message), 500)

    def post(self, data_product_id: str, text: str):
        """
        Handles the POST request for processing Great Expectations validation.
        Args:
            data_product_id (str): The identifier for the data product.
            text (str): The text to be included in the HTML response.
        Returns:
            Response: A Flask response object containing the rendered HTML or an error message.
        Raises:
            Exception: If any error occurs during the processing of the request.
        """

        with tracer.start_as_current_span("great_expectation"):
            try:
                environment = "dev"
                snapshot_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                parent_dir = get_parent_directory()
                expectations_dir = os.path.join(parent_dir, data_product_id, "gx")
                csv_dataset_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_datasets.csv")
                csv_column_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_columns.csv")

                config_dataset_data = get_csv_data(csv_dataset_path)
                logger.info(f"config_dataset_data_length: {len(config_dataset_data)}")

                context = initialize_context(expectations_dir, data_product_id)
                data_source, data_source_name, catalog_name, schema_name = setup_data_source(context, data_product_id)
                logger.info(f"setup datasource_name: {data_source_name}")
                for row in config_dataset_data:
                    process_row_expectations(context, row, data_source, catalog_name, schema_name, csv_column_path, snapshot_date, data_product_id, environment)

                default_path = os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                raw_html = get_raw_file(default_path, text)
                raw_html = update_html(raw_html)
                return make_response(render_template_string(raw_html))

            except Exception as ex:
                return handle_exception(ex)

def initialize_context(expectations_dir, data_product_id):
    with tracer.start_as_current_span("initialize_context"):
        try:
            logger.info("initialize_file_context")
            context = initialize_file_context(expectations_dir, data_product_id)
            configure_data_docs(context, expectations_dir)
            return context
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def setup_data_source(context, data_product_id):
    with tracer.start_as_current_span("setup_data_source"):
        try:
            # logger.info("initialize_sql_alchemy_context")
            # data_source_name, catalog_name, schema_name, engine, connection_string = setup_sql_alchemy_data_source(data_product_id)
            
            data_source, data_source_name, catalog_name, schema_name = setup_spark_data_source(context, data_product_id)
            logger.info(f"setup_spark_data_source:{data_source_name}")
            return data_source, data_source_name, catalog_name, schema_name
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def process_row_expectations(context, row, data_source, catalog_name, schema_name, csv_column_path, snapshot_date, data_product_id, environment):
    """
    Processes a single dataset row by performing various data validation and expectation tasks.
    Args:
        context: The context object for managing the data processing.
        row (dict): A dictionary representing a single row of the dataset.
        data_source (str): The source of the data.
        catalog_name (str): The name of the data catalog.
        schema_name (str): The name of the schema within the catalog.
        csv_column_path (str): The path to the CSV file containing column definitions.
        snapshot_date (str): The date of the data snapshot.
        data_product_id (str): The ID of the data product.
        environment (str): The environment in which the process is running.
    Returns:
        Response: An HTTP response object in case of an error.
    """

    dataset_name = row.get("dataset_name")
            
    with tracer.start_as_current_span(f"process_row_expectations: {dataset_name}"):
        try:
            row_id_keys = row.get("row_id_keys")
            logger.info(f"dataset_name:{dataset_name}")

            if dataset_name:
                # Create Data Asset for Dataset if it does not exist
                # 1 Data Asset per Table
                data_assets = add_data_assets(context, dataset_name, data_source, catalog_name, schema_name)
                # Create Expectation Suite for Datasets if it does not exist
                # 1 Expectation Suite Per Table
                expectation_suite_name =  f"{dataset_name}_suite"
                expectation_suite = manage_expectation_suite(context, expectation_suite_name)
                expectation_suite.expectations = []
                expectation_suite.save()

                if row_id_keys:
                    # Add Expectation to check primary key versus set
                    add_primary_key_expectations(expectation_suite, row, row_id_keys, dataset_name)
                else:
                    logger.info("No row_id_keys expectation list")
                #Add Expectation to compare table versus expectation table
                process_row_count_expectations(expectation_suite, row, dataset_name, catalog_name, schema_name)

                # Add the dataset by date suite to the data asset
                data_assets = add_or_update_suite(context, data_assets, dataset_name, expectation_suite_name)

                row_id_keys = row.get("row_id_keys")
                process_column_expectations(context, dataset_name, csv_column_path, data_assets, expectation_suite, catalog_name, schema_name, data_source, row_id_keys)

                logger.info(f"Running validation on dataset_name: {dataset_name} for all data_assets")
                validation_results = validate_all_data_assets(context, data_assets)

                table_name = "bronze_gx_validations"
                spark = DatabricksSession.builder.getOrCreate()
                save_validation_results(catalog_name, schema_name, table_name, validation_results, spark, snapshot_date, data_product_id, environment)
            else:
                logger.warning("Dataset name not available in process row expectations")
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def add_data_assets(context, dataset_name, data_source, catalog_name, schema_name):
    """
    Adds data assets to the given context.
    Args:
        context: The context to which the data assets will be added.
        dataset_name (str): The name of the dataset.
        data_source (str): The data source from which the data is retrieved.
        catalog_name (str): The name of the catalog containing the dataset.
        schema_name (str): The name of the schema containing the dataset.
    Returns:
        dict: A dictionary containing the added data assets.
    Raises:
        Exception: If an unexpected error occurs during the process.
    """
    
    with tracer.start_as_current_span("add_data_assets"):
        try:
            data_assets = {}
            data_asset_name = dataset_name
            table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
            data_set_sql = f"Select * from {table_name}"
            logger.info(f"add_data_asset: {data_asset_name}")
            data_assets = add_data_asset(context, data_assets, data_asset_name, dataset_name, "spark_dataframe", catalog_name, schema_name, data_source, data_set_sql)
            logger.info(f"added data_asset:{data_asset_name}")
            return data_assets
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def add_primary_key_expectations(expectation_suite, row, row_id_keys, dataset_name):
    """
    Adds primary key expectations to the given expectation suite.
    This function creates an expectation that the values in the specified primary key column(s) 
    should be within a set of expected values. The expected values are retrieved from the provided 
    row dictionary. If the expected values are not provided or are not a string, a warning is logged.
    Args:
        expectation_suite (ExpectationSuite): The expectation suite to which the primary key expectations will be added.
        row (dict): A dictionary containing the expected values for the primary key.
        row_id_keys (str): The name of the column(s) that represent the primary key.
        dataset_name (str): The name of the dataset being processed.
    Returns:
        None
    """
    
    with tracer.start_as_current_span("add_primary_key_expectations"):
        try:
            expected_values = row.get("expected_values")
            if expected_values and isinstance(expected_values, str):
                expected_values_list = [item.strip(" '\t") for item in expected_values.split(",")]
                logger.info(f"expected_values:{expected_values}")
                expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                    column=row_id_keys,
                    value_set=expected_values_list,
                    result_format={
                        "result_format": "COMPLETE",
                        "unexpected_rows_query": "",
                        "expectation_name": f"{row_id_keys} key for table is expected to be in csv expected value list"
                    }
                )
                expectation_suite.add_expectation(expectation)
                expectation_suite.save()
            else:
                logger.info(f"Expected values for primary key are missing or not a string for dataset: {dataset_name}")

            return expectation_suite
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def process_column_in_compare_expectations(expectation_suite, column, row_id_keys, dataset_name, catalog_name, schema_name, date_field, date_value):
    with tracer.start_as_current_span("process_column_in_compare_expectations"):
        try:
            column_name = column.get("column_name")
            compare_table = column.get("compare_table")
            compare_row_id_keys = column.get("compare_row_id_keys")
            if is_valid_string(compare_table) and is_valid_string(compare_row_id_keys) and is_valid_string(row_id_keys):
                logger.info(f"creating expectation for compare_table:{compare_table}")
                spark = DatabricksSession.builder.getOrCreate()
                table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
                compare_table_name = f"{catalog_name}.{schema_name}.{compare_table}"

                unexpected_rows_query = (
                    f"SELECT {column_name} FROM {table_name} WHERE {column_name} NOT IN "
                    f"(SELECT {compare_row_id_keys} FROM {compare_table_name} where {date_field} = '{date_value}') "
                    f" and {date_field} = '{date_value}' " 
                    
                )
                logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                df_additional_key = spark.sql(unexpected_rows_query)
                unexpected_rows_list = [str(value) if isinstance(value, str) else value for row in df_additional_key.collect() for value in row.asDict().values()]

                expectation = gx.expectations.ExpectColumnValuesToNotBeInSet(
                    column=row_id_keys,
                    value_set=unexpected_rows_list,
                    result_format={
                        "result_format": "COMPLETE",
                        "unexpected_rows_query": unexpected_rows_query,
                        "expectation_name": f"{column_name} In Actual but not in expected"
                    }
                )
                expectation_suite.add_expectation(expectation)
                expectation_suite.save()

                unexpected_rows_query = (
                    f"SELECT {compare_row_id_keys} FROM {compare_table_name} WHERE {column_name} NOT IN "
                    f"(SELECT {column_name} FROM {table_name} where {date_field} = '{date_value}') "
                    f"and {date_field} = '{date_value}' "
                )
                logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                df_additional_key = spark.sql(unexpected_rows_query)
                unexpected_rows_list = [str(value) if isinstance(value, str) else value for row in df_additional_key.collect() for value in row.asDict().values()]

                expectation = gx.expectations.ExpectColumnDistinctValuesToContainSet(
                    column=row_id_keys,
                    value_set=unexpected_rows_list,
                    result_format={
                        "result_format": "COMPLETE",
                        "unexpected_rows_query": unexpected_rows_query,
                        "expectation_name": f"{column_name} In Expected but not in actual"
                    }
                )
                expectation_suite.add_expectation(expectation)
                expectation_suite.save()

                return expectation_suite
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def process_row_count_expectations(expectation_suite, row, dataset_name, catalog_name, schema_name):
    with tracer.start_as_current_span("process_row_count_expectations"):
        try:
            expected_row_count_min = row.get("expected_row_count_min")
            expected_row_count_max = row.get("expected_row_count_max")
            table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
            unexpected_rows_query = f"Select count(*) as row_count, {expected_row_count_min} row_count_min, {expected_row_count_max} row_count_max from {table_name}"
            if isinstance(expected_row_count_max, (int, float)) and not math.isnan(expected_row_count_max) and expected_row_count_max > 0:
                if isinstance(expected_row_count_min, (int, float)) and not math.isnan(expected_row_count_min) and expected_row_count_min > 0:
                    expectation = gx.expectations.ExpectTableRowCountToBeBetween(
                        min_value=expected_row_count_min,
                        max_value=expected_row_count_max,
                        result_format={
                            "result_format": "COMPLETE",
                            "unexpected_rows_query": unexpected_rows_query,
                            "expectation_name": f"{table_name} row count is expected to be between {expected_row_count_min} and {expected_row_count_max}",
                            "expectation_test_type": "Is Invalid"
                        }
                    )
                    expectation_suite.add_expectation(expectation)
                    expectation_suite.save()
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)
        
def process_column_expectations(context, dataset_name, csv_column_path, data_assets, expectation_suite, catalog_name, schema_name, data_source, row_id_keys):
    """
    Processes column expectations for a given dataset.
    This function reads column configuration data from a CSV file, filters it based on the dataset name,
    and applies expectations to the columns either by date or without date.
    Args:
        context (object): The context object for the current operation.
        dataset_name (str): The name of the dataset to process.
        csv_column_path (str): The file path to the CSV containing column configuration data.
        data_assets (object): The data assets to be used for processing.
        expectation_suite (object): The expectation suite to be applied.
        catalog_name (str): The name of the catalog.
        schema_name (str): The name of the schema.
        data_source (str): The data source to be used.
    Returns:
        Response: A Flask response object in case of an error.
    """
    

    with tracer.start_as_current_span(f"process_column_expectations for dataset: {dataset_name}"):
        try:
            config_column_data = get_csv_data(csv_column_path)
            config_column_data = list(filter(lambda x: x.get("dataset_name") == dataset_name, config_column_data))
            logger.info(f"filtered_config_column_data_length for dataset_name:{dataset_name}:{len(config_column_data)}")

            if config_column_data:

                for column in config_column_data:
                    column_name = column.get("column_name")
                    if not column_name or (isinstance(column_name, float) and math.isnan(column_name)):
                        continue

                    apply_expectations_by_date = column.get("apply_expectations_by_date")
                    if apply_expectations_by_date:
                        process_column_expectations_by_date(context, column, dataset_name, data_assets, expectation_suite, catalog_name, schema_name, data_source, row_id_keys)
                    else:
                        process_column_expectations_without_date(context, column, dataset_name, data_assets, expectation_suite, catalog_name, schema_name)
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def process_column_expectations_by_date(context, column, dataset_name, data_assets, expectation_suite, catalog_name, schema_name, data_source, row_id_keys):
    """
    Processes column expectations by date for a given dataset.
    Args:
        context (object): The context object for managing expectations.
        column (dict): A dictionary containing column details and expectations.
        dataset_name (str): The name of the dataset.
        data_assets (list): A list of data assets.
        expectation_suite (object): The expectation suite object.
        catalog_name (str): The name of the catalog.
        schema_name (str): The name of the schema.
        data_source (str): The data source identifier.
    Returns:
        None
    Raises:
        Exception: If an unexpected error occurs during processing.
    """
    
    column_name = column.get("column_name")
    with tracer.start_as_current_span(f"process_column_expectations_by_date for column: {column_name}"):
        try:
            logger.info(f"process_column_expectations_by_date for column: {column_name}")
            date_field = column.get("apply_expectations_by_date")
            table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
            compare_table_name = f"{catalog_name}.{schema_name}.{column.get('compare_table')}"
            apply_expectations_for_n_dates_back = column.get("apply_expectations_for_n_dates_back")

            if apply_expectations_for_n_dates_back:
                date_sql = f"SELECT DISTINCT {date_field} FROM {table_name} order by {date_field} desc LIMIT {int(apply_expectations_for_n_dates_back)}"
            else:
                date_sql = f"SELECT DISTINCT {date_field} FROM {table_name} order by {date_field} desc"

            logger.info(f"date_sql:{date_sql}")
            spark = DatabricksSession.builder.getOrCreate()
            df_dates = spark.sql(date_sql)
            dates = df_dates.collect()

            for row in dates:
                date_value = row[date_field]
                logger.info(f"date_value:{date_value}")
                data_asset_name = f"{dataset_name}:{date_field}_{date_value}"
                date_data_set_sql = f"SELECT * FROM {table_name} WHERE {date_field} = '{date_value}'"
                logger.info(f"add_data_asset: {data_asset_name}")
                data_assets = add_data_asset(context, data_assets, data_asset_name, dataset_name, "spark_dataframe", catalog_name, schema_name, data_source, date_data_set_sql)
                suite_name = f"{data_asset_name}_suite"
                logger.info(f"suite_name:{suite_name}")

                expectation_suite = manage_expectation_suite(context, suite_name)
                process_column_is_not_unkown_expectations(expectation_suite, column, date_field, date_value, table_name, compare_table_name)
    
                # Validate that row_id_keys is a list or a valid string (if applicable)
                if not row_id_keys:
                    logger.warning(f"row_id_keys is missing or empty for row: {row}")
                    # Handle the case where row_id_keys is missing or not valid
                    return None
                else:
                    process_column_in_compare_expectations(expectation_suite, column, row_id_keys, dataset_name, catalog_name, schema_name, date_field, date_value)
                
                # Add the dataset by date suite to the data asset
                data_assets = add_or_update_suite(context, data_assets, dataset_name, suite_name)

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def process_column_expectations_without_date(context, column, dataset_name, data_assets, expectation_suite, catalog_name, schema_name):
    with tracer.start_as_current_span("process_column_expectations_without_date"):
        try:
            logger.info(f"process_column_expectations_without_date for column: {column_name}")
            data_asset_name = dataset_name
            logger.info(f"checking by column only whole dataset: {dataset_name}")
            logger.info(f"column_name:{column.get('column_name')}")
            process_column_is_not_unkown_expectations(expectation_suite, column, None, None, f"{catalog_name}.{schema_name}.{dataset_name}", None)
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)
        
def process_column_is_not_unkown_expectations(expectation_suite, column, date_field, date_value, table_name, compare_table_name):
    with tracer.start_as_current_span("process_column_is_not_unkown_expectations"):
        try:
            column_name = column.get("column_name")
            mostly = column.get("expected_percent_to_not_be_null")
            if mostly:
                expectation = gx.expectations.ExpectColumnValuesToNotBeNull(
                    column=column_name,
                    mostly=mostly,
                    result_format={
                        "result_format": "COMPLETE",
                        "unexpected_rows_query": "",
                        "expectation_name": f"{column_name} is expected to be NOT NULL",
                        "expectation_test_type": "Is Unknown"
                    }
                )
                expectation_suite.add_expectation(expectation)
                expectation_suite.save()

            expect_column_values_to_not_be_in_set = column.get("expect_column_values_to_not_be_in_set")
            if expect_column_values_to_not_be_in_set:
                expected_values_list = [
                    str(item).strip(" '\t") if isinstance(item, str) else item
                    for item in str(expect_column_values_to_not_be_in_set).split(",") 
                    if isinstance(expect_column_values_to_not_be_in_set, str)
                ]
                expectation = gx.expectations.ExpectColumnValuesToNotBeInSet(
                    column=column_name,
                    value_set=expected_values_list,
                    result_format={
                        "result_format": "COMPLETE",
                        "unexpected_rows_query": "",
                        "expectation_name": f"{column_name} is expected to not be in csv list of UNKNOWN values",
                        "expectation_test_type": "Is Unknown"
                    }
                )
                expectation_suite.add_expectation(expectation)
                expectation_suite.save()

                return expectation_suite
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            raise Exception(error_message)

def handle_exception(ex):
    with tracer.start_as_current_span("handle_exception"):
        try:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            return make_response(render_template("error.html", error_message=error_message), 500)
        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            logger.error(error_message, exc_info=sys.exc_info())
            return make_response(render_template("error.html", error_message=error_message), 500)

class ExpectPrimaryKeyMatchSpark(gx.expectations.UnexpectedRowsExpectation):
    """Expect that the composite primary keys of two Spark DataFrames are identical after optional filtering."""
    unexpected_rows_query: str = ""  # or any default query that suits your logic
    description: str = "Unexpected rows query."

    # def __init__(self, unexpected_rows_query: str, id: Optional[str] = None, meta: Optional[Dict[str, Any]] = None,  notes: Optional[str] = None, rendered_content: Optional[Any] = None):
    #     super().__init__()
    #     self.unexpected_rows_query = unexpected_rows_query


class GreatExpectationModule(Resource):
    def get(self, data_product_id: str, module: str, text: str):
        """
        Retrieves and renders an HTML file from a specified directory structure.

        Args:
            data_product_id (str): The identifier for the data product.
            module (str): The module name used to construct the directory path.
            text (str): The name of the HTML file to be retrieved.

        Returns:
            Response: A Flask response object containing the rendered HTML content.
        """

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
        file_name = os.path.basename(text)
        dir_path = module
        path = os.path.join(expectations_directory_path, "uncommitted", "data_docs", "local_site", dir_path)
        raw_html = get_raw_file(file_system=path, file_name=file_name)
        return make_response(render_template_string(raw_html))

class GreatExpectationPage(Resource):
    def get(self, data_product_id: str, module: str, suite: str, run: str, page: str, text: str):
        """
        Retrieves and processes an HTML file based on the provided parameters and returns a rendered HTML response.

        Args:
            data_product_id (str): The ID of the data product.
            module (str): The module name.
            suite (str): The suite name.
            run (str): The run identifier.
            page (str): The page identifier.
            text (str): The text containing the file name.

        Returns:
            Response: A Flask response object containing the rendered HTML.
        """

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
        file_name = os.path.basename(text)
        dir_path = module
        path = os.path.join(expectations_directory_path, "uncommitted", "data_docs", "local_site", dir_path, suite, run, page)
        raw_html = get_raw_file(file_system=path, file_name=file_name)
        raw_html = update_html(raw_html)
        return make_response(render_template_string(raw_html))
