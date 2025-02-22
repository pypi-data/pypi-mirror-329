"""Module to conditionally execute transform logic for silver and gold workflows based on project metadata
   including creating Databricks views and/or tables.
"""

import os
import sys  # don't remove required for error handling
import re
import subprocess

from pathlib import Path
from importlib import util  # library management
import cdh_lava_core.databricks_service.notebook as dbx_notebook
import cdh_lava_core.python_service.python_client as py_client

pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    # import pyspark.pandas  as pd
    # bug - pyspark version will not read local files in the repo
    os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
    import pyspark.pandas as pd
else:
    import pandas as pd


OS_NAME = os.name
sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

import cdh_lava_core.databricks_service.sql as databricks_sql
import cdh_lava_core.az_key_vault_service.az_key_vault as az_key_vault
import cdh_lava_core.cdc_tech_environment_service.environment_core as az_environment_core


class WorkflowMetaData:
    """Class to conditionally execute transform logic for silver and gold workflows based on project metadata
    including creating Databricks views and/or tables.
    """

    @classmethod
    def get_configuration_for_pipeline(cls, config, workflow_metadata):
        """Takes in config dictionary and workflow_metadata, returns populated config_workflow dictionary

        Args:
            config (dict): A dictionary containing configuration parameters.
            workflow_metadata (dict): A dictionary containing metadata for the workflow.

        Returns:
            dict: A dictionary containing the populated config_workflow.

        """
        data_product_id = config["data_product_id"]
        environment = config["environment"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_configuration_for_pipeline"):
            try:
                arg_list = {}

                yyyy_param = config["yyyy"]
                mm_param = config["mm"]
                dd_param = config["dd"]
                if (
                    len(dd_param.strip()) == 0
                    or dd_param.strip() == "N/A"
                    or dd_param.strip() == "NA"
                ):
                    transmission_period = mm_param + "_" + yyyy_param
                    dd_param = "NA"
                else:
                    transmission_period = yyyy_param + "_" + mm_param + "_" + dd_param

                environment = config["environment"]
                override_save_flag = config["override_save_flag"]

                row = workflow_metadata

                execute_flag = row["execute_flag"]
                workflow_parameters = row["workflow_parameters"]
                export_schema_metrics = row["export_schema_metrics"]
                view_name = row["view_name"]
                workflow_type = row["workflow_type"]
                workflow_name = row["workflow_name"]
                query_name = row["workflow_name"]
                if view_name is not None:
                    view_name = str(view_name).strip()
                    if len(view_name) > 0:
                        # some queries have multiple params, save for each
                        workflow_name = view_name

                if workflow_name is view_name:
                    logger.info(f"saving workflow with view name: {view_name}")
                else:
                    if workflow_name is None or workflow_name == "":
                        logger.info("workflow_name is blank")
                    else:
                        logger.info(
                            f"saving workflow with workflow_name:{workflow_name}"
                        )

                row_id_keys = row["row_id_keys"]

                # execute
                arg_dictionary = dict()

                if workflow_parameters is None:
                    logger.info("workflow_parameters are empty")
                    workflow_parameters = ""
                else:
                    workflow_parameters = workflow_parameters.strip()

                config_workflow = {"workflow_parameters": workflow_parameters}

                if workflow_parameters != "":
                    logger.info("workflow_parameters are " + workflow_parameters)
                    arg_list = [x.strip() for x in workflow_parameters.split("|")]
                    for line in arg_list:
                        pair = [x.strip() for x in line.split(":")]
                        if len(pair) > 1:
                            arg_dictionary[pair[0]] = pair[1]
                        else:
                            arg_dictionary[pair[0]] = ""
                else:
                    logger.info("workflow_parameters are blank")

                arg_dictionary["environment"] = environment
                arg_dictionary["yyyy"] = yyyy_param
                arg_dictionary["mm"] = mm_param
                arg_dictionary["dd"] = dd_param
                arg_dictionary["transmission_period"] = transmission_period

                # save the workflow name as view name
                # this allows for the same pipeline to be saved multiple times with different paramters

                if override_save_flag == "override_with_save":
                    save_flag = "save"
                elif override_save_flag == "override_with_skip_save":
                    save_flag = "skip_save"
                else:
                    save_flag = "default"

                if save_flag == "default":
                    if row["save_flag"] is not None:
                        if len(row["save_flag"]) > 0:
                            save_flag = row["save_flag"]
                    else:
                        save_flag = "save"

                execute_results_flag = row["execute_results_flag"]
                if execute_results_flag is None:
                    execute_results_flag = "skip_execute"
                if execute_results_flag.strip() == "":
                    execute_results_flag = "skip_execute"

                config_workflow["workflow_type"] = workflow_type
                config_workflow["transmission_period"] = transmission_period
                config_workflow["workflow_name"] = workflow_name
                config_workflow["query_name"] = query_name
                config_workflow["view_name"] = view_name
                config_workflow["save_flag"] = save_flag
                config_workflow["execute_flag"] = execute_flag
                config_workflow["arg_dictionary"] = arg_dictionary
                config_workflow["export_schema_metrics"] = export_schema_metrics
                config_workflow["row_id_keys"] = row_id_keys
                config_workflow["execute_results_flag"] = execute_results_flag

                return config_workflow

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def contains_workspace(repository_path):
        """
        Check if the given repository path contains the '/Workspace' directory.

        Args:
            repository_path (str): The path of the repository.

        Returns:
            bool: True if the repository path contains '/Workspace', False otherwise.
        """
        return "/Workspace" in repository_path
    
    @staticmethod
    def remove_duplicate_folder(base_path):
        # Normalize and split the path into components
        base_path = os.path.normpath(base_path)
        path_parts = base_path.split(os.sep)
        
        # Check if the last two folder names are the same
        if len(path_parts) >= 2 and path_parts[-1] == path_parts[-2]:
            # Remove the last folder if it is a duplicate
            new_path = os.sep.join(path_parts[:-1])
            return new_path
        return base_path
        
    @classmethod
    def get_execute_workflow_parameters(cls, config, config_workflow):
        """Takes in config dictionary and config_workflow, and returns the result of executed pipelines.

        Args:
            config (dict): A dictionary containing configuration parameters.
            config_workflow (dict): A dictionary containing pipeline-specific configuration parameters.

        Returns:
            dict: A dictionary containing the updated config_workflow with additional parameters.

        """

        environment = config["environment"]
        data_product_id = config["data_product_id"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_execute_workflow_parameters"):
            try:
                repository_path = config["repository_path"]

                data_product_id_root = config["data_product_id_root"]
                workflow_name = config_workflow["workflow_name"]
                arg_dictionary = config_workflow["arg_dictionary"]

                running_local = config.get("running_local")
                if cls.contains_workspace(repository_path) or running_local is True:
                    repository_path = repository_path.rstrip("/")
                    if running_local is False:
                        base_path = repository_path
                    else:
                        base_path = repository_path
                        base_path = base_path.replace("/Workspace", "")
                else:
                    cdh_databricks_repository_path = config[
                        "cdh_databricks_repository_path"
                    ]
                    base_path = cdh_databricks_repository_path.rstrip("/")


                    # Remove the 'config/' part
                    # Here we assume 'config' is always a direct folder and not nested
                    new_parts = [part for part in path.parts if part != "config"]

                    # Create a new Path object from the remaining parts
                    new_path = Path(*new_parts)

                    # Convert back to string if needed
                    base_path = str(new_path)

                    base_path = cls.remove_duplicate_folder(base_path)
                    # Create a Path object
                    path = Path(base_path)
                    
                dir_name_python = "/".join([base_path, "autogenerated", "python"])
                workflow_name = workflow_name.replace(
                    ".", ""
                )
                workflow_name = data_product_id + "_" + workflow_name + ".py"
                path_to_execute = os.path.join(dir_name_python, workflow_name)

                database_prefix = config["cdh_database_name"]

                arg_dictionary["database_prefix"] = database_prefix

                config_workflow["arg_dictionary"] = arg_dictionary
                config_workflow["path_to_execute"] = path_to_execute
                logger.info(f"config_workflow:{str(config_workflow)}")
                return config_workflow

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_view_dataframe(cls, config, spark, config_workflow):
        """Takes in config dictionary, spark and config pipeline
        and returns dataframe with columns sorted

        Args:
            config (dict): A dictionary containing configuration parameters.
            spark (pyspark.sql.SparkSession): The Spark session object.
            config_workflow (dict): A dictionary containing pipeline configuration.

        Returns:
            pyspark.sql.DataFrame: A dataframe with columns sorted.
        """

        data_product_id = config["data_product_id"]
        environment = config["environment"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_view_dataframe"):
            try:
                cdh_database_name = config["cdh_database_name"]
                view_name = config_workflow["view_name"]

                full_view_name = f"{cdh_database_name}.{view_name}"
                sql_statement = f"SELECT * FROM {full_view_name}"
                logger.info(f"sql_statement:{sql_statement}")
                unsorted_df = spark.sql(sql_statement)
                sorted_df = unsorted_df.select(sorted(unsorted_df.columns))
                sorted_df.createOrReplaceTempView("table_sorted_df")

                config_workflow["full_view_name"] = full_view_name

                return sorted_df

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


   
    @classmethod
    def execute_workflow(cls, config, config_workflow, workflow_type, dbutils=None):
        """
        Executes a pipeline based on the provided configuration.

        Args:
            config (dict): The overall configuration for the workflow.
            config_workflow (dict): The specific configuration for the workflow to be executed.

        Returns:
            None
        """

        data_product_id = config.get("data_product_id")
        environment = config.get("environment")
        workflow_name = config_workflow["workflow_name"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        span_name = f"execute_workflow: {workflow_name}"
        with tracer.start_as_current_span(span_name):
            try:
                running_local = config["running_local"]
                workflow_type = config_workflow["workflow_type"]
                client_secret = config["client_secret"]
                if workflow_type is None:
                    workflow_type = "databricks_sql"
                workflow_name = config_workflow["workflow_name"]
                execute_flag = config_workflow["execute_flag"]
                logger.info(f"execute_flag: {execute_flag}")
                if execute_flag is None:
                    execute_flag = "skip_execute"
                elif execute_flag == "skip_execute":
                    logger.info(f"skip execute requested: {workflow_name}")
                else:
                    execute_flag = "execute"
                    if workflow_type == "databricks_sql":
                        logger.info(f"execute_flag requested: {workflow_name}")
                        config_workflow = cls.get_execute_workflow_parameters(
                            config, config_workflow
                        )
                        path_to_execute = config_workflow["path_to_execute"]
                        arg_dictionary = config_workflow["arg_dictionary"]
                        # time out in 15 minutes: 900 sec or 600 10 min
                        if running_local is True:
                            logger.info(f"running_local true:{running_local}")

                            # Initialize running_interactive as False
                            running_interactive = False

                            # Check if the client_secret is None or a zero-length string
                            if not client_secret or len(client_secret) == 0:
                                running_interactive = True
                                logger.info(
                                    f"running_local:{running_local} and running_interactive:{running_interactive}"
                                )
                        else:
                            logger.info(f"running_local false:{running_local}")
                            # Trim leading and trailing whitespace from client_secret

                            running_interactive = False

                        databricks_instance_id = config["databricks_instance_id"]
                        az_sub_tenant_id = config.get("az_sub_tenant_id")
                        az_sub_client_id = config.get("az_sub_client_id")
                        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
                        az_sub_client_secret_key = config.get(
                            "az_sub_client_secret_key"
                        )
                        az_sub_client_secret_key = az_sub_client_secret_key.replace(
                            "-", "_"
                        )
                        client_secret = config.get("client_secret")
                        logger.info(
                            f"az_sub_client_secret_key:{az_sub_client_secret_key}"
                        )
                        logger.info(f"az_sub_client_id:{az_sub_client_id}")

                        if running_local is True:
                            if client_secret is None or client_secret == "":
                                running_interactive = True
                            else:
                                running_interactive = False
                            obj_pyclient = py_client.PythonClient()
                            result = obj_pyclient.execute_python_file(path_to_execute, data_product_id, environment )
                        else:
                            running_interactive = False

                            az_sub_client_secret_key = config.get("az_sub_client_secret_key")
                            obj_key_vault = az_key_vault.AzKeyVault(
                                az_sub_tenant_id,
                                az_sub_client_id,
                                client_secret,
                                az_kv_key_vault_name,
                                running_interactive,
                                data_product_id,
                                environment,
                                az_sub_client_secret_key
                            )

                            cdh_databricks_pat_secret_key = config[
                                "cdh_databricks_pat_secret_key"
                            ]

                            cdh_databricks_kv_scope = config.get("cdh_databricks_kv_scope")
                            dbx_pat_token = obj_key_vault.get_secret(
                                cdh_databricks_pat_secret_key,
                                cdh_databricks_kv_scope,
                                dbutils,
                            )

                            cdh_databricks_cluster = config.get("cdh_databricks_cluster")
                            timeout_minutes = 15
                        
                            obj_notebook = dbx_notebook.Notebook()
                            obj_notebook.run_notebook_and_poll_status(
                                dbx_pat_token,
                                databricks_instance_id,
                                cdh_databricks_cluster,
                                path_to_execute,
                                arg_dictionary,
                                timeout_minutes,
                                data_product_id,
                                environment,
                            )

                    else:
                        logger.info("run remote")
                        if "dbutils" in locals():
                            dbutils.notebook.run(path_to_execute, 900, arg_dictionary)
                        else:
                            dbutils = None
                return f"Success: {workflow_name} executed"
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def fetch_and_save_workflow(cls, config, config_workflow, dbutils):
        """Takes in config dictionary, config_workflow dictionary, token, repository_path
        and saves sql

        Args:
            config (dict): A dictionary containing configuration parameters.
            config_workflow (dict): A dictionary containing pipeline configuration parameters.

        Returns:
            None
        """

        data_product_id = config["data_product_id"]
        environment = config["environment"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        workflow_name = config_workflow["workflow_name"]
        span_name = f"fetch_and_save_workflow: {workflow_name}"
        with tracer.start_as_current_span(span_name):
            try:
                # environment vars
                running_local = config["running_local"]
                yyyy_param = config["yyyy"]
                mm_param = config["mm"]
                dd_param = config["dd"]
                environment = config["environment"]
                databricks_instance_id = config["databricks_instance_id"]
                data_product_id = config["data_product_id"]
                data_product_id_root = config["data_product_id_root"]
                repository_path = config["repository_path"]
                tenant_id = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")
                vault_url = config.get("az_kv_key_vault_name")
                az_sub_client_secret_key = config.get("az_sub_client_secret_key")

                # pipeline vars
                query_name = config_workflow["query_name"]
                query_name = query_name.strip()
                workflow_name = config_workflow["workflow_name"]
                workflow_name = workflow_name.strip()
                execute_results_flag = config_workflow["execute_results_flag"]
                arg_dictionary = config_workflow["arg_dictionary"]
                transmission_period = config_workflow["transmission_period"]
                logger.info(f"query_name: {query_name}")
                logger.info(f"workflow_name: {workflow_name}")
                logger.info(f"execute_results_flag: {execute_results_flag}")
                logger.info(f"arg_dictionary: {arg_dictionary}")
                logger.info(f"transmission_period: {transmission_period}")

                obj_sql = databricks_sql.DatabricksSQL()

                cdh_databricks_pat_secret_key = config.get(
                    "cdh_databricks_pat_secret_key"
                )

                client_secret = config.get("client_secret")
                if client_secret is None or client_secret == "":
                    obj_core = az_environment_core.EnvironmentCore()
                    logger.info(
                        f"getting environment variable: {az_sub_client_secret_key}"
                    )
                    client_secret = obj_core.get_environment_variable(
                        az_sub_client_secret_key
                    )

                client_secret_key = config.get("az_sub_client_secret_key")
                if client_secret_key is None:
                    raise ValueError("az_sub_client_secret_key is not set in configuration file")
                obj_az_keyvault = az_key_vault.AzKeyVault(
                    tenant_id,
                    client_id,
                    client_secret,
                    vault_url,
                    False,
                    data_product_id,
                    environment,
                    client_secret_key,
                )

                cdh_databricks_kv_scope = config.get("cdh_databricks_kv_scope")

                databricks_access_token = obj_az_keyvault.get_secret(
                    cdh_databricks_pat_secret_key, cdh_databricks_kv_scope, dbutils
                )
                if databricks_access_token is None:
                    databricks_access_token = ""
                    databricks_access_token_length = 0
                else:
                    databricks_access_token_length = len(databricks_access_token)
                logger.info(
                    f"databricks_access_token_length: {databricks_access_token_length}"
                )

                # configure to download and save sql only in dev
                # In future, add support for notebook pipelines in addition to sql pipelines
                if environment == "dev":
                    # Always download and save in dev
                    save_flag = "save"
                    logger.info(f"save_flag: {save_flag}")

                    obj_sql = databricks_sql.DatabricksSQL()
                    cdh_databricks_repository_path = config.get(
                        "cdh_databricks_repository_path"
                    )
                    response_text = obj_sql.fetch_and_save_workflow(
                        databricks_access_token,
                        repository_path,
                        environment,
                        databricks_instance_id,
                        data_product_id_root,
                        data_product_id,
                        query_name,
                        workflow_name,
                        execute_results_flag,
                        arg_dictionary,
                        running_local,
                        yyyy_param,
                        mm_param,
                        dd_param,
                        transmission_period,
                        cdh_databricks_repository_path,
                    )
                else:
                    # in non-dev environments, only download and save if requested
                    save_flag = config_workflow["save_flag"]
                    if save_flag.lower() == "save":
                        logger.warning(f"save_flag: {save_flag}")
                        logger.warning(
                            "save_flag not supported in non-dev environments - using override"
                        )
                        obj_sql = databricks_sql.DatabricksSQL()
                        cdh_databricks_repository_path = config.get(
                            "cdh_databricks_repository_path"
                        )
                        response_text = obj_sql.fetch_and_save_workflow(
                            databricks_access_token,
                            repository_path,
                            environment,
                            databricks_instance_id,
                            data_product_id_root,
                            data_product_id,
                            query_name,
                            workflow_name,
                            execute_results_flag,
                            arg_dictionary,
                            running_local,
                            yyyy_param,
                            mm_param,
                            dd_param,
                            transmission_period,
                            cdh_databricks_repository_path,
                        )
                    else:
                        response_text = "skip_save"

                return response_text

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
