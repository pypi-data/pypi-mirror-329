import os
import sys
import shutil
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

def force_remove_expectations_directory(path):
    """
    Forcefully removes the expectations_directory_path.
    
    :param path: The path to the expectations directory to remove.
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            logger.info(f"Successfully removed the directory: {path}")
        except Exception as e:
            logger.info(f"Failed to remove the directory: {path}. Error: {e}")
    else:
        logger.info(f"Directory does not exist: {path}")

def add_value_set_expectation(expectation_suite, column_name, value_set, result_format, expectation_name, expectation_type):
    """
    Adds an expectation to the suite if the value_set is not empty, not None, and not NaN.
    """
    
    logger.info("=======================================================================================")
    logger.info(f"Adding expectation: {expectation_name} for column: {column_name} with value_set: {value_set}")
    logger.info("=======================================================================================")

    if (
        column_name is not None  # Ensure column_name is not None
        and not (isinstance(column_name, float) and math.isnan(column_name))  # Ensure column_name is not NaN
        and value_set is not None  # Ensure value_set is not None
        and not (isinstance(value_set, float) and math.isnan(value_set))  # Ensure value_set is not NaN
        and isinstance(value_set, list)  # Ensure value_set is a list
        and len(value_set) > 0  # Ensure value_set is not empty
    ):
        if expectation_type == "ExpectColumnValuesToBeInSet":
            expectation = gx.expectations.ExpectColumnValuesToBeInSet(
                column=column_name,
                value_set=value_set,
                result_format=result_format
            )
        elif expectation_type == "ExpectColumnValuesToNotBeInSet":
            expectation = gx.expectations.ExpectColumnValuesToNotBeInSet(
                column=column_name,
                value_set=value_set,
                result_format=result_format
            )
        else:
            logger.error(f"Unknown expectation_type: {expectation_type}")
            return
        
        expectation_suite.add_expectation(expectation)
        expectation_suite.save()
    else:
        logger.info(f"Skipping expectation for column {column_name} because value_set is empty, None, or NaN.")


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

def split_and_clean(input_string, delimiter=',', strip_whitespace=True, remove_empty=True, strip_ticks=False):
    """Splits the input string by a delimiter and optionally cleans the resulting items."""
    if strip_whitespace:
        items = [item.strip() for item in input_string.split(delimiter)]
    else:
        items = input_string.split(delimiter)
    
    if strip_ticks:
        # Remove only outer single and double quotes
        items = [item[1:-1] if item.startswith("'") and item.endswith("'") else item for item in items]
        items = [item[1:-1] if item.startswith('"') and item.endswith('"') else item for item in items]

    if remove_empty:
        items = [item for item in items if item]
    return items


def initialize_file_context(expectations_dir, data_product_id):
    """Initialize or load a Great Expectations context."""
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
    Validates a data asset using a run ID and a defined expectation suite, with added debugging and logging.
    """
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    suite_name = expectation_suite.name
    run_name = f"{data_asset_name}_validation_{suite_name}_{current_time}"

    logger.info(f"Starting validation with run_name: {run_name}")
    
    try:
        # Create the validation definition
        validation_definition = ValidationDefinition(
            name=run_name,
            data=batch_definition,  # The active batch being validated
            suite=expectation_suite
        )
        logger.debug("ValidationDefinition created successfully.")

        # Add ValidationDefinition to the context
        try:
            context.validation_definitions.add(validation_definition)
            logger.info(f"ValidationDefinition added to context: {run_name}")
        except DataContextError as e:
            logger.warning(f"ValidationDefinition already exists, updating: {run_name}. Error: {str(e)}")
            context.validation_definitions.remove(run_name)
            context.validation_definitions.add(validation_definition)
            logger.info(f"ValidationDefinition updated: {run_name}")

        # Create a list of Actions for the Checkpoint to perform
        action_list = [
            gx.checkpoint.UpdateDataDocsAction(
                name="update_all_data_docs",
            ),
        ]
        logger.debug("Action list for checkpoint created: update_all_data_docs")

        # Get Validation Definitions
        validation_definitions = [
            context.validation_definitions.get(run_name)
        ]
        logger.debug(f"Validation definitions retrieved: {validation_definitions}")

        # Create the Checkpoint
        checkpoint_name = f"{run_name}_checkpoint"
        checkpoint = gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=validation_definitions,
            actions=action_list,
            result_format={"result_format": "COMPLETE"},
        )
        logger.info(f"Checkpoint created: {checkpoint_name}")

        # Save the Checkpoint to the Data Context
        context.checkpoints.add(checkpoint)
        logger.info(f"Checkpoint added to context: {checkpoint_name}")

        # Run the validation
        run_id = RunIdentifier(run_name=run_name)
        validation_results = checkpoint.run(
            batch_parameters=batch_parameters,
            run_id=run_id
        )
        logger.info(f"Validation completed successfully for run_id: {run_id} with batch_parameters: {batch_parameters}")
        
        return validation_results

    except Exception as e:
        logger.error(f"An unexpected error occurred during validation: {str(e)}", exc_info=True)
        raise


def configure_data_docs(context, expectations_dir):
    """Configure and build Data Docs site if not already configured."""
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
    """Retrieve or create an expectation suite."""
    try:
        suite = context.suites.get(suite_name)
        if suite is None:
            logger.warning(f"Suite '{suite_name}' not found; creating a new one.")
            suite = ExpectationSuite(suite_name)
            context.suites.add(suite)
            suite.save()  # Explicit save
            logger.info(f"Created and added new suite '{suite_name}'")
        else:
            logger.info(f"Loaded existing suite '{suite_name}'")
            suite.save()  # Explicit save
        return suite
    except DataContextError:
        logger.warning(f"Suite '{suite_name}' not found; creating a new one.")
        suite = ExpectationSuite(suite_name)
        context.suites.add(suite)
        suite.save()  # Explicit save
        return suite

def setup_spark_data_source(context, data_product_id):
    
    spark = DatabricksSession.builder.getOrCreate()

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

    # Fetch or create data asset
    try:
        data_asset = data_source.get_asset(data_asset_name)
    except (LookupError):
        if data_access_method == "spark_dataframe":
            data_asset = data_source.add_dataframe_asset(name=data_asset_name)
        else:
            data_asset = data_source.add_table_asset(name=data_asset_name, table_name=dataset_name)

    # Prepare batch definition and request
    batch_definition_name = f"{dataset_name}_batch_definition"
    spark = DatabricksSession.builder.getOrCreate()
    dataframe = spark.sql(data_set_sql)
    batch_parameters = {"dataframe": dataframe}

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
    # Determine the data asset name based on the access method

    # Setup and get batch, batch_definition, and batch_request
    batch, batch_definition, batch_request, batch_parameters  = setup_and_get_batch(context, dataset_name, data_asset_name, catalog_name, schema_name, data_access_method, data_source, data_set_sql)
    
    logger.info("Type of batch_definition: %s", type(batch_definition))


    # Check if the data asset does not exist
    if data_asset_name not in data_assets:
        data_assets[data_asset_name] = {
            "batch": batch,
            "batch_definition": batch_definition,
            "batch_request": batch_request,
            "batch_parameters": batch_parameters,
            "suites": []  # Initialize an empty list to store suites
        }
        print(f"Added new data asset: {data_asset_name}")
    else:
        print(f"Data asset already exists: {data_asset_name}")

    return data_assets

def add_or_update_suite(context, data_assets, data_asset_name, suite):
    # Log the initial state of data_assets
    logger.info(f"Starting suite management for {data_asset_name}. Current suites: {len(data_assets.get(data_asset_name, {}).get('suites', []))}")

    if data_asset_name in data_assets:
        existing_suites = data_assets[data_asset_name]["suites"]
        found = False
        for index, existing_suite in enumerate(existing_suites):
            if existing_suite['name'] == suite['name']:
                # Log before updating
                logger.info(f"Found existing suite {suite['name']} in {data_asset_name}. Updating...")
                existing_suites[index] = suite
                found = True
                break
        if not found:
            # Log before adding new suite
            logger.info(f"No existing suite matched {suite['name']} in {data_asset_name}. Adding new suite...")
            existing_suites.append(suite)

        # Log after modification
        logger.info(f"Updated suites in {data_asset_name}: {len(existing_suites)}")

    else:
        # Log when creating new data asset
        logger.info(f"No data asset found for {data_asset_name}. Creating new data asset with suite.")
        data_assets[data_asset_name] = {"suites": [suite]}
    
    # Log the number of expectations in the new or updated suite
    logger.info(f"Final suite {suite['name']} has {len(suite.get('expectations', []))} expectations.")

    # Explicitly save the suite if necessary
    # Note: Depending on your Great Expectations setup, you might not need to manually save each suite here if the context manages it globally.
    # context.suites.add(suite)
    # Log final state of data assets
    logger.info(f"Final suites in {data_asset_name}: {len(data_assets[data_asset_name]['suites'])}")

    return data_assets

def validate_all_data_assets(context, data_assets):
    # Dictionary to hold all validation results
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
                                column_name = result_format.get('column_name_checked', str(expectation_config.get('kwargs', {}).get('column', '')))
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
                                    'column_name': column_name,
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


def update_suite_expectations(suite):
    """
    Update all expectations in a suite to be serializable
    """
    if hasattr(suite, "expectations"):
        updated_expectations = []
        for exp in suite.expectations:
            if not hasattr(exp, 'configuration'):
                # Create a new serializable expectation
                new_exp = SerializableExpectationConfiguration(
                    type=exp.type,
                    kwargs=deepcopy(exp.kwargs)
                )
                new_exp.meta = deepcopy(exp.meta)
                updated_expectations.append(new_exp)
            else:
                updated_expectations.append(exp)
        suite.expectations = updated_expectations
    return suite

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
        with tracer.start_as_current_span("great_expectation"):
            try:
                environment = "dev"
                snapshot_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Setup paths and context
                parent_dir = get_parent_directory()
                expectations_dir = os.path.join(parent_dir, data_product_id, "gx")
 
                csv_dataset_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_datasets.csv")
                csv_column_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_columns.csv")
                config_dataset_data = get_csv_data(csv_dataset_path)
                config_dataset_data_length = len(config_dataset_data)
                logger.info(f"config_dataset_data_length: {config_dataset_data_length}")
                
                # Initialize context and data docs
                data_source_name, catalog_name, schema_name, engine, connection_string = setup_sql_alchemy_data_source(data_product_id)

                # Get the directory of the current file
                current_dir = os.path.dirname(os.path.abspath(__file__))

                # Go up one directory from the current directory
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

                # Construct the relative path to the CSV file
                expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
                
                force_remove_expectations_directory(expectations_directory_path)

                logger.info("initialize_file_context")
                context = initialize_file_context(expectations_dir, data_product_id)
                configure_data_docs(context, expectations_dir)
                logger.info("initialize_sql_alchemy_context")
                data_access_method = "spark_dataframe"
                logger.info(f"data_access_method:{data_access_method}")


                if data_access_method == "spark_dataframe":
                    logger.info(f"setting up datasource for data_product_id:{data_product_id}")
                    data_source, data_source_name, catalog_name, schema_name = setup_spark_data_source(context, data_product_id)
                    logger.info(f"setup_spark_data_source:{data_source_name}")

                # Manage suites and read dataset CSV
                for row in config_dataset_data:
                    dataset_name = row.get("dataset_name")
                    row_id_keys = row.get("row_id_keys")

                    logger.info(f"dataset_name:{dataset_name}")
                    data_assets = {} 
                    batch = None
                    if dataset_name:
                        data_access_method = "spark_dataframe"  # or "sql_alchemy"
                        if data_access_method == "spark_dataframe":                  
                            data_asset_name = dataset_name
                        else:
                            data_asset_name = f"{dataset_name}_sql_alchemy"

                        table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
                        data_set_sql = f"Select * from {table_name}"
                       
                        logger.info(f"add_data_asset: {data_asset_name}: data_access_method:{data_access_method} ")
                        data_assets = add_data_asset(context, data_assets, data_asset_name, dataset_name, data_access_method, catalog_name, schema_name, data_source, data_set_sql)
                        logger.info(f"added data_asset:{data_asset_name}")

                        # Determine suite name based on access method
                        if data_access_method == "spark_dataframe":
                            suite_name = f"{data_asset_name}_suite"
                        else:
                            suite_name =  f"{data_asset_name}_suite_sql_alchemy"
                        logger.info(f"suite_name:{suite_name}")

                        # Manage expectation suite
                        expectation_suite = manage_expectation_suite(context, suite_name)
                        
                        # Clear all expectations
                        expectation_suite.expectations = []
                        # Save the empty suite back to the data context
                        expectation_suite.save()

                        ##########################
                        # Table level validations
                        ##########################

                        if data_access_method == "spark_dataframe":                  
                            data_asset_name = dataset_name
                        else:
                            data_asset_name = f"{dataset_name}_sql_alchemy"

                        # Check primary key versus expected values
                        if row_id_keys and batch:
                            expected_values = row.get("expected_values")
                            # Split the string and strip quotes and spaces from each item
                            if isinstance(expected_values, str) and expected_values.strip():
                                expected_values_list = split_and_clean(expected_values)
                                logger.info(f"expected_values:{expected_values}")
                                logger.info(f"expected_values_list length: {len(expected_values_list)}")
                                
                                add_value_set_expectation(
                                expectation_suite=expectation_suite,
                                column_name=row_id_keys,
                                value_set=expected_values_list,
                                result_format={
                                "result_format": "COMPLETE",
                                "unexpected_rows_query": "",
                                "expectation_name": f"{row_id_keys} key for table is expected to be in csv expected value list"},
                                expectation_name=f"{column_name} should contain expected values",
                                expectation_type="ExpectColumnValuesToBeInSet"
                                )
                            else:
                                logger.info("Expected values list is empty")
                            
                        compare_table = row.get("compare_table")
                        logger.info(f"compare_table: {compare_table}")
                        compare_row_id_keys = row.get("compare_row_id_keys")
                        logger.info(f"compare_row_id_keys: {compare_row_id_keys}")
                        compare_table_name = f"{catalog_name}.{schema_name}.{compare_table}"
                        logger.info(f"row_id_keys: {row_id_keys}")
                        if isinstance(row_id_keys, str) and row_id_keys.strip():
                            row_id_keys_list = split_and_clean(row_id_keys)
                        else:
                            row_id_keys_list = []

                        logger.info(f"compare_row_id_keys: {compare_row_id_keys}")
                        if isinstance(compare_row_id_keys, str) and row_id_keys.strip():
                            compare_row_id_keys_list = split_and_clean(compare_row_id_keys)
                        else:
                            compare_row_id_keys_list = []
                            
                        filter_clause = ""
                        compare_filter_clause = ""

                        if compare_table and compare_row_id_keys and row_id_keys and valid_sql_identifier(compare_table) and valid_sql_identifier(row_id_keys):
                            logger.info(f"creating expectation for compare_table:{compare_table}")
 
                            # expectation =add_custom_value_set_expectation(expectation_suite, row_id_keys, unexpected_rows_list, name=expectation_name, notes=unexpected_rows_query)
                            # expectation = ExpectPrimaryKeyMatchSpark()
                            # expectation.unexpected_rows_query=unexpected_rows_query

                            spark = DatabricksSession.builder.getOrCreate()

                            # Execute the SQL query and store the result in a DataFrame
                            # # Define the required unexpected_rows_query attribute
                            # unexpected_rows_query: str = (
                            #     f"SELECT { row_id_keys} "
                            #     f"FROM {table_name} "
                            #     f"WHERE { row_id_keys} NOT IN "
                            #     f"(SELECT { compare_row_id_keys} FROM {compare_table_name})"
                            # )


                            # logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                            # df_additional_key = spark.sql(unexpected_rows_query)
                            # # Collect the results into a list of values as strings or numbers depending on their type
                            # unexpected_rows_list = [
                            #     str(value) if isinstance(value, str) else value 
                            #     for row in df_additional_key.collect() 
                            #     for value in row.asDict().values()
                            # ]

                            # # PK In Actual but not in expected Missing Expectation
                            # expectation =  gx.expectations.ExpectColumnValuesToNotBeInSet(
                            #                       column=row_id_keys,
                            #                       value_set=unexpected_rows_list,
                            #                       result_format={
                            #                         "result_format": "COMPLETE",
                            #                         "unexpected_rows_query": unexpected_rows_query,
                            #                         "expectation_name": "PK In Actual but not in expected"}
                            #                       )

                            # # Add the expectation to the suite
                            # expectation_suite.add_expectation(expectation)
                            # expectation_suite.save()
                                                       
                            # # Execute the SQL query and store the result in a DataFrame
                            # # Define the required unexpected_rows_query attribute
                            # unexpected_rows_query: str = (
                            #     f"SELECT { row_id_keys} "
                            #     f"FROM {compare_table_name} "
                            #     f"WHERE { row_id_keys} NOT IN "
                            #     f"(SELECT { compare_row_id_keys} FROM {table_name})"
                            # )

                            # logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                            # df_additional_key = spark.sql(unexpected_rows_query)
                            # # Collect the results into a list of values as strings or numbers depending on their type
                            # unexpected_rows_list = [
                            #     str(value) if isinstance(value, str) else value 
                            #     for row in df_additional_key.collect() 
                            #     for value in row.asDict().values()
                            # ]

                            # # PK In Actual but not in expected Missing Expectation
                            # expectation =  gx.expectations.ExpectColumnDistinctValuesToContainSet(
                            #                       column=row_id_keys,
                            #                       value_set=unexpected_rows_list,
                            #                       result_format={
                            #                         "result_format": "COMPLETE",
                            #                         "unexpected_rows_query": unexpected_rows_query,
                            #                         "expectation_name": "PK In Expected but not in actual"}
                            #                       )

                            # # Add the expectation to the suite
                            # expectation_suite.add_expectation(expectation)
                            # expectation_suite.save()
 
                         
                        else:
                            logger.info("No compare table dataframe rule configured for comparison.")

                        expected_row_count_min = row.get("expected_row_count_min")
                        expected_row_count_max = row.get("expected_row_count_max")
                        unexpected_rows_query = f"Select count(*) as row_count, {expected_row_count_min} row_count_min, {expected_row_count_max} row_count_max from {table_name} "
                        # Check if expected_row_count is a valid number, not NaN, and greater than 0
                        if isinstance(expected_row_count_max, (int, float)) and not math.isnan(expected_row_count_max) and expected_row_count_max > 0:
                            if isinstance(expected_row_count_min, (int, float)) and not math.isnan(expected_row_count_min) and expected_row_count_min > 0:
                                expectation =  gx.expectations.ExpectTableRowCountToBeBetween(min_value=expected_row_count_min, max_value=expected_row_count_max,
                                                                result_format={
                                                                    "result_format": "COMPLETE",
                                                                    "unexpected_rows_query": unexpected_rows_query,
                                                                    "expectation_name": f"{table_name} row count is expected to be between {expected_row_count_min} and {expected_row_count_max} ",
                                                                    "expectation_test_type": "Is Invalid"
                                                                }
                                )
                                expectation_suite.add_expectation(expectation)
                                expectation_suite.save()

                        # save the expectation suite        
                        logger.info(f"Adding expectations to data_asset_name: {data_asset_name}")
                        add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                        expectation_suite.save()

                        ####################################
                        # Perform column level validations
                        ####################################

                        config_column_data = get_csv_data(csv_column_path)
                        config_column_data_length = len(config_column_data)
                        logger.info(f"config_column_data_length:{config_column_data_length}")
                        config_column_data = list(filter(lambda x: x.get("dataset_name") == dataset_name, config_column_data))
                        config_column_data_length = len(config_column_data)
                        config_column_data = list(filter(lambda x: x.get("dataset_name") == dataset_name, config_column_data))
                        logger.info(f"filtered_config_column_data_length for dataset_name:{dataset_name}:{config_column_data_length}")
                        if config_column_data:
                            for column in config_column_data:

                                column_name = column.get("column_name")
                                logger.info("#################################################################")
                                logger.info(f"#### {column_name}")
                                logger.info("#################################################################")
                                
                                compare_table = column.get("compare_table")
                                compare_filter =  column.get("compare_filter")
                                compare_row_id_keys = column.get("compare_row_id_keys")
                                compare_row_columns =  column.get("compare_row_columns")

                                if column_name is None or column_name == "" or (isinstance(column_name, float) and math.isnan(column_name)):
                                    # Skip this iteration if column_name is NaN or invalid
                                    continue
                                apply_expectations_by_date = column.get("apply_expectations_by_date")
                                # Check by Date / Month and column
                                if apply_expectations_by_date is not None and apply_expectations_by_date != "" and not (isinstance(apply_expectations_by_date, float) and math.isnan(apply_expectations_by_date)):
                                    date_field = apply_expectations_by_date
                                    table_name = f"{catalog_name}.{schema_name}.{dataset_name}"
                                    compare_table_name = f"{catalog_name}.{schema_name}.{compare_table}"
                                    apply_expectations_for_n_dates_back = column.get("apply_expectations_for_n_dates_back")
                                    if apply_expectations_for_n_dates_back is not None and apply_expectations_for_n_dates_back != "" and not math.isnan(apply_expectations_for_n_dates_back):
                                        apply_expectations_for_n_dates_back = int(apply_expectations_for_n_dates_back)
                                        date_sql = f"SELECT DISTINCT {date_field} FROM {table_name} order by  {date_field} desc LIMIT {apply_expectations_for_n_dates_back}"
                                    else:
                                        date_sql = f"SELECT DISTINCT {date_field} FROM {table_name} order by  {date_field} desc"
                                        
                                    logger.info(f"date_sql:{date_sql}")
                                    spark = DatabricksSession.builder.getOrCreate()
                                    df_dates = spark.sql(date_sql)
                                    dates = df_dates.collect()
                                    for row in dates:
                                        # Retrieve the batch using the above request
                                        date_value = row[date_field]
                                        logger.info(f"date_value:{date_value}")
                                        if data_access_method == "spark_dataframe":                  
                                            data_asset_name = f"{dataset_name}:{apply_expectations_by_date}_{date_value}"
                                        else:
                                            data_asset_name = f"{dataset_name}:{apply_expectations_by_date}_{date_value}_sql_alchemy"                                    
                                        # Define a query that selects everything from the table for a specific date
                                        date_data_set_sql = f"SELECT * FROM {table_name} WHERE {date_field} = '{date_value}'"
                                        logger.info(f"add_data_asset: {data_asset_name}: data_access_method:{data_access_method} ")
                                        data_assets = add_data_asset(context, data_assets, data_asset_name, dataset_name, data_access_method, catalog_name, schema_name, data_source, date_data_set_sql)
                                        # Determine suite name based on access method
                                        suite_name = f"{data_asset_name}_suite" if data_access_method == "spark_dataframe" else f"{data_asset_name}_suite_sql_alchemy"
                                        logger.info(f"suite_name:{suite_name}")
                                        
                                        # Manage expectation suite
                                        expectation_suite = manage_expectation_suite(context, suite_name)

                                        logger.info(f"column_name:{column_name}")
                                    
                                        spark = DatabricksSession.builder.getOrCreate()
                                        logger.info(f"#### {column_name} - {date_value} - CHECK 1 - In Expected but not Actual")

                                        if compare_table and valid_sql_identifier(compare_table) and valid_sql_identifier(column_name):
                                            # Execute the SQL query and store the result in a DataFrame
                                            # Define the required unexpected_rows_query attribute
                                            if compare_filter:
                                                unexpected_rows_query: str = (
                                                    f"SELECT {compare_row_id_keys} "
                                                    f"FROM {compare_table_name} "
                                                    f"WHERE concat_ws('.',{ compare_row_id_keys}, { compare_row_columns})  NOT IN "
                                                    f"(SELECT concat_ws('.',{ compare_row_id_keys}, { column_name})  FROM {table_name} "
                                                    f"where {date_field} = '{date_value}' and {compare_filter})  "
                                                    f"and {date_field} = '{date_value}' and {compare_filter}"
                                                )
                                            else:
                                                unexpected_rows_query: str = (
                                                    f"SELECT {compare_row_id_keys} "
                                                    f"FROM {compare_table_name} "
                                                    f"WHERE concat_ws('.',{ compare_row_id_keys}, { compare_row_columns})  NOT IN "
                                                    f"(SELECT concat_ws('.',{ compare_row_id_keys}, { column_name})  FROM {table_name} "
                                                    f"where {date_field} = '{date_value}') "
                                                    f"and {date_field} = '{date_value}'"
                                                )


                                            logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                                            df_additional_key = spark.sql(unexpected_rows_query)
                                            # Collect the results into a list of values as strings or numbers depending on their type
                                            unexpected_rows_list = [
                                                str(value) if isinstance(value, str) else value 
                                                for row in df_additional_key.collect() 
                                                for value in row.asDict().values()
                                            ]
                                            logger.info(f"unexpected_rows_list:{unexpected_rows_list}")
                                            logger.info(f"unexpected_rows_list length: {len(unexpected_rows_list)}")
                                            # PK In Expected but not in Actual

                                            add_value_set_expectation(
                                                expectation_suite=expectation_suite,
                                                column_name=compare_row_id_keys,
                                                value_set=unexpected_rows_list,
                                                result_format={
                                                "result_format": "COMPLETE",
                                                "column_name_checked": column_name,
                                                "unexpected_rows_query": unexpected_rows_query,
                                                "expectation_name": f"{column_name} partitioned by {date_field} In Expected but not in Actual",
                                                "expectation_test_type": "Is Invalid"
                                                },
                                                expectation_name=f"{column_name} In Expected but not in Actual",
                                                expectation_type="ExpectColumnValuesToNotBeInSet"
                                            )

                                            add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                                            expectation_suite.save()

                                            logger.info(f"#### {column_name} - {date_value} - CHECK 2 - In Actual but Not Expected")

                                            # Execute the SQL query and store the result in a DataFrame
                                            # Define the required unexpected_rows_query attribute
                                            if compare_filter:
                                                unexpected_rows_query: str = (
                                                    f"SELECT { compare_row_id_keys} "
                                                    f"FROM {table_name} "
                                                    f"WHERE concat_ws('.',{ compare_row_id_keys}, { column_name}) NOT IN "
                                                    f"(SELECT concat_ws('.',{ compare_row_id_keys}, { compare_row_columns}) FROM {compare_table_name} "
                                                    f"where {date_field} = '{date_value}'  and {compare_filter}) "
                                                    f"and {date_field} = '{date_value}' and {compare_filter}"
                                                )
                                            else:
                                                unexpected_rows_query: str = (
                                                    f"SELECT { compare_row_id_keys} "
                                                    f"FROM {table_name} "
                                                    f"WHERE  concat_ws('.',{ compare_row_id_keys}, { column_name})  NOT IN "
                                                    f"(SELECT concat_ws('.',{ compare_row_id_keys}, { compare_row_columns}) FROM {compare_table_name} "
                                                    f"where {date_field} = '{date_value}') "
                                                    f"and {date_field} = '{date_value}'"
                                                )

                                            logger.info(f"unexpected_rows_query:{unexpected_rows_query}")
                                            df_additional_key = spark.sql(unexpected_rows_query)
                                            # Collect the results into a list of values as strings or numbers depending on their type
                                            unexpected_rows_list = [
                                                str(value) if isinstance(value, str) else value 
                                                for row in df_additional_key.collect() 
                                                for value in row.asDict().values()
                                            ]

                                            # PK In Actual but not in expected Missing Expectation
                                            logger.info(f"unexpected_rows_list length: {len(unexpected_rows_list)}")

                                            add_value_set_expectation(
                                                expectation_suite=expectation_suite,
                                                column_name=compare_row_id_keys,
                                                value_set=unexpected_rows_list,
                                                result_format={
                                                                        "result_format": "COMPLETE",
                                                                        "column_name_checked": column_name,
                                                                        "unexpected_rows_query": unexpected_rows_query,
                                                                        "expectation_name": f"{column_name} partitioned by {date_field} In Actual but not in Expected",
                                                                        "expectation_test_type":"Is Invalid"},
                                                expectation_name=f"{column_name} should not contain unexpected values",
                                                expectation_type="ExpectColumnValuesToNotBeInSet"
                                            )

                                            add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                                            expectation_suite.save()

                                        logger.info(f"#### {column_name} - {date_value} - CHECK 3 - NOT NULL")

                                        # NOT NUll Check
                                        mostly = column.get("expected_percent_to_not_be_null")
                                        logger.info(f"mostly:{mostly}")
                                        expected_percent_to_not_be_null = column.get("expected_percent_to_not_be_null")
                                        logger.info(f"expected_percent_to_not_be_null:{expected_percent_to_not_be_null}")
                                        if expected_percent_to_not_be_null is not None and not math.isnan(expected_percent_to_not_be_null):
                                            expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column=column_name, mostly=mostly, 
                                                  result_format={
                                                    "result_format": "COMPLETE",
                                                    "column_name_checked": column_name,
                                                    "unexpected_rows_query": "",
                                                    "expectation_name": f"{column_name} partitioned by {date_field} is expected to be NOT NULL",
                                                    "expectation_test_type":"Is Unknown"}
                                                  )
                                            expectation_suite.add_expectation(expectation)
                                            expectation_suite.save()
                                        else:
                                            logger.info("No expected_percent_to_not_be_null check for column :{column_name}")
                                            
                                        # Not in List Check
                                        
                                        logger.info(f"#### {column_name} - {date_value} - CHECK 4 - In Hard Coded Exclusion List")

                                        expect_column_values_to_not_be_in_set = column.get("expect_column_values_to_not_be_in_set")
                                        logger.info(f"expect_column_values_to_not_be_in_set:{expect_column_values_to_not_be_in_set}")
                                        if isinstance(expect_column_values_to_not_be_in_set, str) and expect_column_values_to_not_be_in_set.strip():
                                            expect_column_values_to_not_be_in_set_list = split_and_clean(expect_column_values_to_not_be_in_set)
                                            add_value_set_expectation(
                                            expectation_suite=expectation_suite,
                                            column_name=column_name,
                                            value_set=expect_column_values_to_not_be_in_set_list,
                                            result_format={
                                                        "result_format": "COMPLETE",
                                                        "column_name_checked": column_name,
                                                        "unexpected_rows_query": "",
                                                        "expectation_name": f"{column_name} partitioned by {date_field} is expected to not be in EXCLUSION csv list" ,
                                                        "expectation_test_type":"Is Unknown"},
                                            expectation_name=f"{column_name} should not contain unexpected values",
                                            expectation_type="ExpectColumnValuesToNotBeInSet"
                                            )
                                        else:
                                            logger.info("expect_column_values_to_not_be_in_set is empty or missing")
                                        
                                        add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                                        expectation_suite.save()

                                        # in List Check
                                        
                                        logger.info(f"#### {column_name} - {date_value} - CHECK 4 -  Not In Hard Coded Inclusion List")

                                        expect_column_values_to_be_in_set = column.get("expect_column_values_to_be_in_set")
                                        logger.info(f"expect_column_values_to_be_in_set:{expect_column_values_to_be_in_set}")
                                        if isinstance(expect_column_values_to_be_in_set, str) and expect_column_values_to_be_in_set.strip():
                                            expect_column_values_to_be_in_set_list = split_and_clean(expect_column_values_to_be_in_set, strip_ticks=True)
                                            add_value_set_expectation(
                                            expectation_suite=expectation_suite,
                                            column_name=column_name,
                                            value_set=expect_column_values_to_be_in_set_list,
                                            result_format={
                                                        "result_format": "COMPLETE",
                                                        "column_name_checked": column_name,
                                                        "unexpected_rows_query": "",
                                                        "expectation_name": f"{column_name} partitioned by {date_field} is expected to be in INCLUSION csv list" ,
                                                        "expectation_test_type":"Is Invalid"},
                                            expectation_name=f"{column_name} should contain expected values",
                                            expectation_type="ExpectColumnValuesToBeInSet"
                                            )
                                        else:
                                            logger.info("expect_column_values_to_be_in_set is empty or missing")
                                        
                                        add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                                        expectation_suite.save()

                                # Check by column only
                                else:

                                    if data_access_method == "spark_dataframe":                  
                                        data_asset_name = "{dataset_name}"
                                    else:
                                        data_asset_name = f"{dataset_name}_sql_alchemy"

                                    logger.info(f"checking by column only whole dataset: {dataset_name}")
                                    data_asset_name = f"{dataset_name}" if data_access_method == "spark_dataframe" else f"{dataset_name}_sql_alchemy"
                                                
                                    logger.info(f"column_name:{column_name}")
                                    mostly = column.get("expected_percent_to_not_be_null")
                                    logger.info(f"mostly:{mostly}")
                                    expected_percent_to_not_be_null = column.get("expected_percent_to_not_be_null")
                                    logger.info(f"expected_percent_to_not_be_null:{expected_percent_to_not_be_null}")
                                    if expected_percent_to_not_be_null is not None and not math.isnan(expected_percent_to_not_be_null):
                                        expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column=column_name, mostly=mostly, result_format={
                                                    "result_format": "COMPLETE",
                                                    "column_name_checked": column_name,
                                                    "unexpected_rows_query": "",
                                                    "expectation_name": f"{column_name} is expected to be NOT NULL",
                                                    "expectation_test_type":"Is Unknown"}
                                                  )
                                        expectation_suite.add_expectation(expectation)
                                        expectation_suite.save()

                                    expect_column_values_to_not_be_in_set = column.get("expect_column_values_to_not_be_in_set")
                                    
                                    if (
                                        expect_column_values_to_not_be_in_set is not None
                                        and  isinstance(expect_column_values_to_not_be_in_set, str)  # Ensure it's a number
                                    ):
                                        logger.info(f"expect_column_values_to_not_be_in_set:{expect_column_values_to_not_be_in_set}")
                                        expected_values_list = split_and_clean(expect_column_values_to_not_be_in_set)
                                        logger.info(f"expected_values_list: {len(expected_values_list)}")
                                        
                                        add_value_set_expectation(
                                            expectation_suite=expectation_suite,
                                            column_name=column_name,
                                            value_set=expected_values_list,
                                            result_format={
                                                    "result_format": "COMPLETE",
                                                    "column_name_checked": column_name,
                                                    "unexpected_rows_query": "",
                                                    "expectation_name": f"{column_name} is expected to not be in csv list of UNKNOWN values",
                                                    "expectation_test_type":"Is Unknown"},
                                            expectation_name=f"{column_name} should not contain unexpected values",
                                            expectation_type="ExpectColumnValuesToNotBeInSet")
                                        
                                        add_or_update_suite(context, data_assets, data_asset_name, expectation_suite)
                                        expectation_suite.save()
                                    

                        logger.info(f"Running validation on dataset_name: {dataset_name} for all data_assets")
                        validation_results = validate_all_data_assets(context, data_assets)

                        table_name = "bronze_gx_validations"
                        lava_schema_name = "cdh_lava"
                        spark = DatabricksSession.builder.getOrCreate()
                        save_validation_results(catalog_name, lava_schema_name, table_name, validation_results, spark, snapshot_date, data_product_id, environment)

                default_path = os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                file_name = text
                raw_html = get_raw_file(default_path, file_name)
                raw_html = update_html(raw_html)
                return make_response(render_template_string(raw_html))

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
