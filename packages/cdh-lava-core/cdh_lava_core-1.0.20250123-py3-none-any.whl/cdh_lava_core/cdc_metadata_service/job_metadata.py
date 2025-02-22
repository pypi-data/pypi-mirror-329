""" Module for job_metadata for the developer service with metadata config file dependencies. """

import os
import sys
import json
import copy
from pathlib import Path
import pandas as pd_legacy
from pyspark.sql import functions as F
import cdh_lava_core.cdc_metadata_service.workflow_metadata as lava_pl_metadata
import cdh_lava_core.cdc_metadata_service.dataset_metadata as lava_ds_metadata
import cdh_lava_core.cdc_metadata_service.environment_metadata as lava_env_metadata
import cdh_lava_core.cdc_tech_environment_service.job_core as lava_job_core
import cdh_lava_core.databricks_service.repo_core as dbx_repo_core
import cdh_lava_core.databricks_service.database as dbx_database
import cdh_lava_core.databricks_service.dataset_crud as dbx_ds_crud
import cdh_lava_core.databricks_service.dataset_core as dbx_ds_core
import cdh_lava_core.databricks_service.cluster as dbx_cluster
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
from cdh_lava_core.az_log_analytics_service.az_kql import AzKql


from opentelemetry.trace.status import StatusCode, Status

import cdh_lava_core.az_storage_service.az_storage_file as az_storage_file
from opentelemetry import trace
import traceback
from opentelemetry.trace.status import StatusCode, Status

IPY_ENABLED = False  # Set this based on whether IPython features are required

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name

ENV_SHARE_FALLBACK_PATH = "/usr/local/share"

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "\\..\\share")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "/.."))
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "/../share")))


class JobMetaData:
    """Class to drives jobs via meta data"""

    @staticmethod
    def install_cluster_library(config) -> str:
        """Installs cluster library

        Args:
            config (dict): Dictionary of LAVA configuration parameters

        Returns:
            str: Installation status message
        """
        library_source = "whl"
        lava_root_project_url = config["lava_root_project_url"]
        cdh_lava_core_version = config["cdh_lava_core_version"]
        cdh_lava_core_version = cdh_lava_core_version.replace("v", "")
        library_folder = f"{lava_root_project_url}dist/"
        library_file = f"{library_folder}{cdh_lava_core_version}-py3-none-any.whl"
        obj_cluster = dbx_cluster.DbxCluster()
        results = obj_cluster.install_cluster_library(
            config, library_source, library_file
        )
        return results

    @staticmethod
    def get_cluster_library_status(config) -> str:
        """Gets cluster library installation status

        Args:
            config (dict): Dictionary of LAVA configuration parameters

        Returns:
            str: Installation status message
        """

        library_source = "whl"
        lava_root_project_url = config["lava_root_project_url"]
        cdh_lava_core_version = config["cdh_lava_core_version"]
        cdh_lava_core_version = cdh_lava_core_version.replace("v", "")
        library_folder = f"{lava_root_project_url}dist/"
        library_file = f"{library_folder}{cdh_lava_core_version}-py3-none-any.whl"
        obj_cluster = dbx_cluster.DbxCluster()
        results = obj_cluster.get_cluster_library_status(
            config, library_source, library_file
        )
        return results

    @staticmethod
    def download_config(
        config: dict,
        dbutils: object,
        data_product_id: str,
        environment: str,
    ) -> str:
        """Downloads configuration from abfss to local machine / repository

        Args:
            config (dict): Dictionary of LAVA configuration parameters
            dbutils (object): Delta.io dbutils object

        Returns:
            str: File download status message
        """

        obj_file = az_storage_file.AzStorageFile()

        cdh_folder_config = config["cdh_folder_config"]
        destination_path = config["environment_json_path"]
        json_file_name = os.path.basename(destination_path)
        source_path_1 = obj_file.convert_abfss_to_https_path(
            cdh_folder_config, data_product_id, environment
        )
        source_message_1 = f"source_path_1:{source_path_1}"
        destination_path = destination_path.replace("/config/" + json_file_name, "")
        copy_result1 = obj_file.file_adls_copy(
            config, source_path_1, destination_path, "BlobFSLocal", dbutils, data_product_id, environment
        )
        result = f"{str(source_message_1)}-{str(copy_result1)}"
        return result

    @staticmethod
    def get_standard_parameters(
        environment: str,
        dbutils,
        spark,
        config_jobs_path: str,
        data_product_id: str,
    ) -> dict:
        """Get standard parameters used to populate run jobs notebook parameters

        Args:
            environment (str): Default environment
            dbutils (_type_): Databricks dbutils object
            spark (_type_): Spark session object
            config_jobs_path (str): Path to the configuration jobs file

        Returns:
            dict: Parameter values
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_standard_parameters"):
            try:
                obj_job_core = lava_job_core.JobCore()

                parameters = obj_job_core.get_standard_parameters(
                    environment, dbutils, data_product_id
                )
                info_msg = f"config_jobs_path:{config_jobs_path}"
                logger.info(info_msg)

                df_jobs = pd_legacy.read_csv(config_jobs_path)
                df_jobs[df_jobs.columns] = df_jobs.apply(
                    lambda x: x.str.strip() if x.dtype == "object" else x
                )
                df_job_names = df_jobs["job"]
                job_name_values = []
                # create copy that won't change
                job_name_values = copy.copy(df_job_names.to_list())
                # remove dupes
                job_name_values_list = [*set(job_name_values)]
                # sort
                job_name_values_list.sort()
                job_name_values_list.insert(0, "Select job to run")
                default_job_name = job_name_values_list[0]

                if dbutils is None:
                    logger.warning("Warning: dbutils is None")
                    running_local = True
                else:
                    widgets = dbutils.widgets
                    running_local = False

                parameters["running_local"] = running_local

                logger.info(f"job_name_values_list:{job_name_values_list}")
                logger.info(f"config_jobs_path:{config_jobs_path}")
                if not running_local:
                    try:
                        job_name = dbutils.widgets.get("job_name")
                        logger.info(f"job_name widget:{job_name}")
                        if job_name == "Select job to run":
                            logger.info("job_name widget does not have job selected")
                            dbutils.widgets.remove("job_name")
                            dbutils.widgets.dropdown(
                                "job_name", default_job_name, job_name_values_list
                            )
                    except Exception as ex:
                        logger.warning("job_name widget not found")
                        dbutils.widgets.dropdown(
                            "job_name",
                            default_job_name,
                            [str(x) for x in job_name_values_list],
                        )
                        job_name = None

                parameters["array_jobs"] = job_name_values_list

                config_jobs_path.split("cdh_lava_core")[0] + "cdh_lava_core"
                # Check if 'cdh_lava_core' is in the path and set repository_path accordingly
                if "cdh_lava_core" in config_jobs_path:
                    parameters["repository_path"] = (
                        config_jobs_path.split("cdh_lava_core")[0] + "cdh_lava_core"
                    )
                else:
                    # Split the path into parts
                    path_parts = config_jobs_path.split(os.sep)
                    # Go three directories up
                    if len(path_parts) >= 3:
                        up_two_dirs = os.sep.join(path_parts[:-2])
                    else:
                        up_two_dirs = os.sep
                    parameters["repository_path"] = up_two_dirs

                # Check if the repository_path exists
                if not os.path.exists(parameters["repository_path"]):
                    # Move to parent directory
                    parent_dir = os.path.dirname(parameters["repository_path"])
                    if os.path.exists(parent_dir):
                        parameters["repository_path"] = parent_dir
                    else:
                        # If the parent directory also doesn't exist, raise an error
                        raise FileNotFoundError(
                            "Neither the repository_path nor its parent directory exists."
                        )

                return parameters

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def setup_project_mount(
        config: dict, spark, dbutils, data_product_id: str, environment: str
    ) -> str:
        """Mounts a project to a specified path in the Databricks file system.

        Args:
            config (dict): A dictionary containing configuration parameters.
            spark: The Spark session object.
            dbutils: The Databricks utilities object.

        Returns:
            str: A string indicating the success or failure of the mount operation.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("setup_project_mount"):
            try:
                environment = config["environment"]
                data_product_id = config["data_product_id"]
                configs = {
                    "fs.azure.account.auth.type": "CustomAccessToken",
                    "fs.azure.account.custom.token.provider.class": spark.conf.get(
                        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
                    ),
                }

                mount_path = f"/mnt/{environment}/{data_product_id}"
                source_path = config["lava_root_project_url"]
                logger.info(f"mount_path:{mount_path}")
                logger.info(f"source_path:{source_path}")

                if dbutils is None:
                    logger.error("Error: dbutils not configured")

                if any(mount.mountPoint == mount_path for mount in dbutils.fs.mounts()):
                    dbutils.fs.unmount(mount_path)

                dbutils.fs.mount(
                    source=source_path, mount_point=mount_path, extra_configs=configs
                )

                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def trigger_pull_request(
        config: dict,
        dbutils,
        data_product_id: str,
        environment: str,
    ) -> str:
        """Triggers pull request

        Args:
            obj_env_metadata (lava_env_metadata.EnvironmentMetaData): The environment metadata object.
            config (dict): The configuration dictionary.
            dbutils (_type_): The dbutils object.

        Returns:
            str: The trigger request file status message.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("trigger_pull_request"):
            try:
                source_path = config["cicd_action_path"]
                root_parts = Path(os.getcwd()).parts
                # get first 4 parts of path should be repo
                folder_root = "/".join(root_parts[0:5])
                logger.info(f"folder_root:{folder_root}")
                logger.info(f"source_path:{source_path}")

                obj_file_core = az_storage_file.AzStorageFile()
                obj_repo_core = dbx_repo_core.RepoCore()
                destination_path = obj_repo_core.get_cicd_destination_path(
                    folder_root, data_product_id, environment
                )
                copy_result = obj_file_core.file_adls_copy(
                    config, source_path, destination_path, "LocalBlobFS", dbutils, data_product_id, environment
                )
                return copy_result

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def run_publish_config(
        config: dict,
        spark,
        dbutils,
        data_product_id,
        environment,
    ) -> str:
        """Runs publish configuration

        Args:
            config (dict): The configuration dictionary.
            spark: The Spark object.
            dbutils: The dbutils object.

        Returns:
            str: Configuration publish status message
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_standard_parameters"):
            try:
                environment = config["environment"]
                sql_statement = (
                    f"Select json_value from lava_ezdx_foodnet_{environment}"
                )
                sql_statement = (
                    sql_statement + ".silver_export_translationfoodnet_json_vw"
                )
                logger.info("sql_statement:" + sql_statement)
                df_json = spark.sql(sql_statement)

                ingress_mount = config["ingress_mount"]
                json_data = json.loads(df_json.toPandas().to_json(orient="columns"))
                json_string = json_data["json_value"]["0"]
                logger.info(json_string)
                config_mount_path = "".join(
                    [
                        "/dbfs",
                        ingress_mount.rstrip("/"),
                        "/lava/translationFoodnet.json",
                    ]
                )
                with open(config_mount_path, "w", encoding="UTF-8") as f_translation:
                    f_translation.write(json_string)
                    f_translation.close()

                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def run_publish_release(config) -> str:
        """Publishes a release to the appropriate environment in Databricks.  This function is not complete.
        Args:
            config (Any): The configuration object containing additional parameters.

        Returns:
            str: A string indicating the success or failure of the release publishing process.
        """

        return "Success"

    @staticmethod
    def run_pull_request(
        config,
        data_product_id,
        environment,
    ) -> str:
        """Triggers pull request from the repository

        Args:
            obj_env_metadata (lava_env_metadata.EnvironmentMetaData): The environment metadata object.
            config (Any): The configuration object.

        Returns:
            str: The result of the pull request execution.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_standard_parameters"):
            try:
                obj_repo_core = dbx_repo_core.RepoCore()
                environment = config["environment"]
                token = config["access_token"]
                branch_name = environment.upper()
                obj_repo_core.pull_repository_latest(
                    config,
                    token,
                    "/Repos/DEV/",
                    "LAVA",
                    branch_name,
                    data_product_id,
                    environment,
                )
                logger.info("pull request completed")
                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def run_data_processing(
        obj_env_metadata: lava_env_metadata.EnvironmentMetaData,
        config,
        spark,
        dbutils,
        export_schema,
        filter_column_name,
        filter_value,
        data_product_id,
        environment,
    ) -> str:
        """Runs data processing: This is the second step in the 5 step (IDEAS) process.

        Args:
            obj_env_metadata (lava_env_metadata.EnvironmentMetaData): An instance of the EnvironmentMetaData class that provides environment metadata.
            config: The configuration object containing various settings.
            spark: The SparkSession object for running Spark jobs.
            dbutils: The Databricks utilities object for interacting with the Databricks environment.
            export_schema: The schema type for exporting data.
            filter_column_name: The name of the column to filter the dataset on.
            filter_value: The value to filter the dataset on.

        Returns:
            str: A status message indicating the result of the data processing.

        Raises:
            Exception: If an error occurs during the data processing.

        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_data_processing"):
            try:
                running_local = config["running_local"]

                logger.info(f"running_local:{running_local}")

                if export_schema == "export":
                    config["is_export_schema_required_override"] = True

                # setup database
                obj_database = dbx_database.Database()
                cdh_folder_database = obj_database.setup_databricks_database(
                    config, spark
                )
                config["cdh_folder_database"] = cdh_folder_database
                df_datasets = obj_env_metadata.get_dataset_list(
                    config, spark, data_product_id, environment
                )

                count_string = str(df_datasets.count())
                msg = f"df_datasets unfiltered count:{count_string}"
                logger.info(msg)
                df_columns = obj_env_metadata.get_column_list(
                    config, spark, dbutils, data_product_id, environment
                )

                # Make sure apply table filters to columns dataframe
                if (
                    filter_column_name is not None
                    and filter_column_name != "all"
                    and filter_column_name.strip() != ""
                ):
                    filter_text = f"{filter_column_name} == '{filter_value}'"
                    df_datasets = df_datasets.filter(filter_text)
                    # filter for current project
                    count_string = str(df_datasets.count())
                    msg = f"df_datasets filtered count:{count_string}"
                    logger.info(msg)
                    msg = f"filter_text:{filter_text}"
                    logger.info(msg)
                    msg = f"dataset_name:{df_datasets}"
                    logger.info(msg)

                data_collect = df_datasets.collect()

                for dataset_metadata in data_collect:
                    obj_dataset = lava_ds_metadata.DataSetMetaData()
                    config_dataset = obj_dataset.get_configuration_for_dataset(
                        config, dataset_metadata, data_product_id, environment
                    )
                    if config_dataset["is_active"] is True:
                        return_text = obj_dataset.save_dataset(
                            config,
                            spark,
                            dbutils,
                            df_columns,
                            config_dataset,
                            data_product_id,
                            environment,
                        )
                        logger.info(return_text)

                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def run_analytics_processing(
        obj_env_metadata: lava_env_metadata.EnvironmentMetaData,
        config: dict,
        spark,
        dbutils,
        export_schema: str,
        filter_column_name: str,
        filter_value: str,
        data_product_id: str,
        environment: str,
    ) -> str:
        """Run analytics processing.  This is the third step in the 5 step (IDEAS) process.

        Args:
            obj_env_metadata (lava_env_metadata.EnvironmentMetaData): Object containing environment metadata.
            config (dict): Configuration dictionary.
            spark: Spark object.
            dbutils: DBUtils object.
            export_schema (str): Export schema flag.
            filter_column_name (str): Name of the column to filter on.
            filter_value (str): Value to filter on.

        Returns:
            str: Analytic processing status message
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_analytics_processing"):
            try:
                obj_ds_crud = dbx_ds_crud.DataSetCrud()
                obj_ds_core = dbx_ds_core.DataSetCore()
                environment = config["environment"]
                data_product_id = config["data_product_id"]

                if export_schema == "export":
                    config["is_export_schema_required_override"] = True

                bronze_sps_config_workflows_df = obj_env_metadata.get_workflow_list(
                    config, spark, data_product_id, environment
                )

                logger.info(
                    f"bronze_sps_config_workflows_df row count: {bronze_sps_config_workflows_df.count()}"
                )

                if (
                    filter_column_name is not None
                    and filter_column_name != "all"
                    and filter_column_name.strip() != ""
                ):
                    filter_text = f"(data_product_id == '{data_product_id}') and {filter_column_name} == '{filter_value}'"
                    bronze_sps_config_workflows_df = (
                        bronze_sps_config_workflows_df.filter(filter_text)
                    )
                    logger.info(
                        f"Filtered row count: {bronze_sps_config_workflows_df.count()}"
                    )

                data_collect = bronze_sps_config_workflows_df.collect()
                for row in data_collect:
                    obj_workflow = lava_pl_metadata.WorkflowMetaData()
                    logger.info(f"getting config for pipeline: {row}")
                    config_workflow = obj_workflow.get_configuration_for_pipeline(
                        config, row
                    )

                    workflow_type = config_workflow["workflow_type"]

                    workflow_name = config_workflow["workflow_name"]
                    # only a few views need to export schema metrics
                    export_schema_metrics = config_workflow["export_schema_metrics"]

                    # fetch and conditionally save
                    fetch_and_save_workflow_text = obj_workflow.fetch_and_save_workflow(
                        config, config_workflow, dbutils
                    )
                    logger.info(fetch_and_save_workflow_text)

                    # conditionally execute
                    execute_text = obj_workflow.execute_workflow(
                        config, config_workflow, workflow_type, dbutils
                    )
                    logger.info(str(execute_text))

                    if workflow_type == "databricks_export":
                        logger.info("run generic export")
                        export_format = "parquet"
                        environment = config["environment"]
                        query_name = config_workflow["query_name"]
                        query_name = query_name.split(".", 1)[1]
                        lava_parquet_folder = config["cdh_folder_database"].replace(
                            "/delta", "/" + export_format
                        )
                        lava_parquet_path = (
                            lava_parquet_folder.rstrip("/")
                            + ("/")
                            + query_name
                            + "."
                            + export_format
                        )
                        sql_command = config_workflow["view_name"]
                        sql_command = sql_command.replace("{environment}", environment)
                        logger.info(f"sql_command:{sql_command}")
                        logger.info(f"lava_parquet_path:{lava_parquet_path}")
                        df_export = spark.sql(f"{sql_command}")
                        df_export.repartition(1).write.format(export_format).mode(
                            "overwrite"
                        ).save(lava_parquet_path)

                    # conditionally export schema metrics
                    # only a few views need to export schema metrics
                    if export_schema_metrics is None:
                        export_schema_metrics = "skip_export"
                        logger.info(f"export_schema_metrics: {workflow_name}")
                    else:
                        if export_schema_metrics == "export":
                            sorted_df = obj_workflow.get_view_dataframe(
                                config, spark, config_workflow
                            )

                            # move row_id generation upstream to view and dataset
                            if set(["row_id"]).issubset(sorted_df.columns) is False:
                                yyyy_param = config["yyyy"]
                                if yyyy_param is None:
                                    yyyy_param = ""
                                mm_param = config["mm"]
                                if mm_param is None:
                                    mm_param = ""
                                dd_param = config["dd"]
                                if dd_param is None:
                                    dd_param = ""

                                row_id_keys = "column_name, full_dataset_name"

                                sorted_df = obj_ds_core.add_row_id_to_dataframe(
                                    sorted_df,
                                    row_id_keys,
                                    yyyy_param,
                                    mm_param,
                                    dd_param,
                                    data_product_id,
                                    environment,
                                )
                            view_or_schema = "view"

                            if sorted_df is None:
                                logger.info("Error: sorted_df is None")

                            config_schema = (
                                obj_ds_crud.get_export_dataset_or_view_schema_config(
                                    config,
                                    config_workflow,
                                    spark,
                                    sorted_df,
                                    view_or_schema,
                                    data_product_id,
                                    environment,
                                )
                            )
                            logger.info(str(config_schema))
                            schema_dataset_df = config_schema["schema_dataset_df"]
                            schema_column_df = config_schema["schema_column_df"]

                            obj_ds_crud.upsert(
                                spark,
                                config,
                                dbutils,
                                schema_dataset_df,
                                config_schema["schema_full_dataset_name"],
                                config_schema["schema_dataset_file_path"],
                                config_schema["is_using_dataset_folder_path_override"],
                                "parquet_delta",
                                "calculated_table",
                                False,
                                config_schema["partitioned_by"],
                                "incremental",
                                data_product_id,
                                environment,
                            )

                            obj_ds_crud.upsert(
                                spark,
                                config,
                                dbutils,
                                schema_column_df,
                                config_schema["schema_full_dataset_name"],
                                config_schema["schema_dataset_file_path"],
                                config_schema["is_using_dataset_folder_path_override"],
                                "parquet_delta",
                                "calculated_table",
                                False,
                                config_schema["partitioned_by"],
                                "incremental",
                                data_product_id,
                                environment,
                            )

                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise ex

    @classmethod
    def on_dropdown_job_change(cls, change, config: dict, button_run) -> str:
        """Dropdown job on change handler

        This method is called when the value of the dropdown job changes. It updates the config dictionary with the new job name and updates the button_run widget with the new job name as its description and tooltip.

        Args:
            change (dict): The change event object containing information about the change.
            config (dict): The configuration dictionary.
            button_run (widget): The button widget to update.

        Returns:
            str: The new value of the dropdown job.
        """

        if change["type"] == "change" and change["name"] == "value":
            config["dropdown_job_name"] = change
            result = f"Click to run: {change['new']}"
            button_run.description = result
            button_run.tooltip = result
        else:
            result = "No job change"

        return result

    @classmethod
    def run_job_name(
        cls,
        obj_env,
        spark,
        job_name,
        config,
        dbutils,
        data_product_id,
        environment,
        config_jobs_path=None,
    ) -> str:
        """
        Runs a job with the specified name.

        Args:
            cls: The class object.
            obj_env: The environment object.
            spark: The Spark session.
            job_name: The name of the job to run.
            config: The configuration dictionary.
            dbutils: The DBUtils object.
            config_jobs_path: The path to the jobs configuration file (optional).

        Returns:
            str: The result of the job processing.

        Raises:
            Exception: If an error occurs during job processing.
        """

        azure_trace_exporter = None

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()


        # Start a span for tracing the job
        import time
        from datetime import timedelta, datetime

        MAX_ATTEMPTS = 10
        WAIT_INTERVAL = 30  # Wait time in seconds between checks

        with tracer.start_as_current_span("run_job_name") as run_job_span:
            start_time = datetime.utcnow()
            start_time = start_time - timedelta(minutes=3)
            trace_id_hex = "not_set"
            child_trace_id_hex = "not_set"
            application_insights_name = "not_set"
            full_job_name = f"{data_product_id}_{job_name}_{environment}"
            run_job_span.set_attribute("job_name", full_job_name)
            run_job_span.set_attribute("data_product_id", data_product_id)
            run_job_span.set_attribute("environment", environment)
            run_job_span.set_attribute("process_level", "child")

            try:
                trace_id = run_job_span.context.trace_id
                trace_id_hex = format(trace_id, '032x')
                azure_trace_exporter = TracerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).azure_trace_exporter

                instrumentation_key = TracerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).instrumentation_key

                obj_az_kql = AzKql()
                application_insights_name = obj_az_kql.get_application_name_from_api_key(config, data_product_id, environment)
                logger.info(f"application_insights_name: {application_insights_name}")
                logger.info(f"job_name: {job_name} started")
                
                # Run the job
                result = ""
                try:
                    # Get configuration details
                    ingress_folder_sps = config["ingress_folder_sps"].rstrip("/")
                    config_jobs_path = config.get("config_jobs_path", f"{ingress_folder_sps}/bronze_sps_config_jobs.csv")

                    import pandas as pd

                    # Read the CSV file into a DataFrame
                    df_jobs = pd.read_csv(config_jobs_path)

                    # Add a new 'job_name' column
                    df_jobs["job_name"] = df_jobs["job"]

                    # Filter the DataFrame based on the 'job_name' column
                    df_jobs_filtered = df_jobs[df_jobs["job_name"] == job_name]

                    if len(df_jobs_filtered) > 0:
                        # Convert the filtered DataFrame to a list of dictionaries and take the first one
                        array_jobs = df_jobs_filtered.to_dict(orient="records")
                        j_a = array_jobs[0]

                        # Extract job details
                        export_schema = j_a.get("export_schema_metrics", "default")
                        job_action = j_a.get("job_action")
                        filter_column_name = j_a.get("filter_column_name")
                        filter_value = j_a.get("filter_value")

                        # Execute the job action using the extracted details
                        result = cls.run_job_action(
                            obj_env,
                            spark,
                            config,
                            dbutils,
                            job_action,
                            export_schema,
                            filter_column_name,
                            filter_value,
                        )

                        result = f"Finished processing: {result}"
                        logger.info(result)

                    else:
                        logger.info(f"Could not find job to run for {job_name}")

                except Exception as job_ex:
                    logger.error(f"Error occurred while executing the job: {str(job_ex)}", exc_info=True)
                    raise


                # Export the current span
                trace_id = run_job_span.get_span_context().trace_id
                trace_id_hex = format(trace_id, '032x')
                logger.info(f"Trace ID for parent trigger job_name: {job_name}: {trace_id_hex}")
                run_job_span.set_status(Status(StatusCode.OK))
                run_job_span.end()
                result = azure_trace_exporter.export([run_job_span])

                logger.info(f"Tracing for parent process for job_name: {job_name} with trace id: {trace_id_hex} completed successfully: {str(result)}")
                logger.info(f"job_name: {job_name} completed")

                # Poll for the child dependency operation ID with timestamp check
                attempts = 0
                operation_id = None
                while attempts < MAX_ATTEMPTS:
                    try:
                        child_job_result = obj_az_kql.query_ai_most_recent_child_dependency_by_parent_job_name(
                            full_job_name, data_product_id, environment
                        )
                        # Assuming the last column is the timestamp
                        operation_id = child_job_result[0][0]  # Extract operation ID
                        timestamp_str = child_job_result[0][-1]  # Extract the timestamp from the last column
                        operation_timestamp = datetime.strptime(timestamp_str,"%Y-%m-%dT%H:%M:%S.%fZ")  # Convert to datetime

                        # Check if the timestamp is greater than the function's start time
                        if operation_timestamp > start_time:
                            child_trace_id_hex = operation_id
                            break  # Exit loop once a valid operation_id is found with a correct timestamp

                        logger.info(f"Attempt {attempts + 1}: Found operation_id but timestamp:{operation_timestamp} is not greater than start time:{start_time}. Retrying...")

                    except Exception as ex:
                        logger.warning(f"Attempt {attempts + 1}: Failed to get child operation_id or timestamp. Retrying...")

                    # Wait before retrying
                    time.sleep(WAIT_INTERVAL)
                    attempts += 1

                if operation_id is None:
                    logger.error(f"Failed to get child operation_id with a valid timestamp after {MAX_ATTEMPTS} attempts.")
                    raise Exception("Child operation_id not found with a valid timestamp")

                return result, child_trace_id_hex

            except Exception as ex:
                logger.error(f"job_name: {job_name} failed", exc_info=True)
                error_msg = f"Error occurred while processing job '{job_name}': {str(ex)}"
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, sys.exc_info())

                run_job_span.set_status(Status(StatusCode.ERROR))
                run_job_span.end()
                if azure_trace_exporter is not None:
                    azure_trace_exporter.export([run_job_span])

                raise

            finally:
                # Log KQL queries
                kql_query = f"""
                KQL to query the parent trace in Application Insights
                App {application_insights_name}:
                dependencies
                | where operation_Id == "{trace_id_hex}"
                """
                logger.info(kql_query)

                kql_query = f"""
                KQL to query the child trace in Application Insights
                App {application_insights_name}:
                dependencies
                | where operation_Id == "{child_trace_id_hex}"
                """
                logger.info(kql_query)

                logger.info(f"job_name: {job_name} finished.")


    @classmethod
    def run_job_action(
        cls,
        obj_env,
        spark,
        config: dict,
        dbutils,
        action,
        export_schema,
        filter_column_name="",
        filter_value="",
    ) -> str:
        """Runs job action step based on job metadata configuration. Jobs can contain multiple steps/actions.

        Args:
            cls (class): The class object.
            obj_env (object): The object environment.
            spark (object): The Spark object.
            config (dict): The configuration dictionary.
            dbutils (object): The dbutils object.
            action (str): The action to be performed.
            export_schema (object): The export schema.
            filter_column_name (str, optional): The name of the filter column. Defaults to empty string.
            filter_value (str, optional): The value of the filter. Defaults to empty string.

        Returns:
            str: The results status message.
        """

        data_product_id = config["data_product_id"]
        environment = config["environment"]

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_job_action"):
            try:
                import pandas as pd

                if pd.isna(filter_column_name):
                    filter_column_name = None

                if filter_column_name is not None:
                    filter_column_name = filter_column_name.strip()

                if filter_value is not None and pd.notna(filter_value):
                    filter_value = filter_value.strip()

                if action == "install_cluster_library":
                    results = cls.install_cluster_library(config)
                elif action == "get_cluster_library_status":
                    results = cls.get_cluster_library_status(config)
                elif action == "setup_project_mount":
                    results = cls.setup_project_mount(
                        config, spark, dbutils, data_product_id, environment
                    )
                elif action == "trigger_pull_request":
                    results = cls.trigger_pull_request(
                        config, dbutils, data_product_id, environment
                    )
                elif action == "run_pull_request":
                    results = cls.run_pull_request(config, data_product_id, environment)
                elif action == "run_publish_release":
                    results = cls.run_publish_release(config)
                elif action == "run_publish_config":
                    results = cls.run_publish_config(
                        config, spark, dbutils, data_product_id, environment
                    )
                elif action == "run_ingress_processing":
                    results = cls.run_ingress_processing(
                        obj_env,
                        config,
                        spark,
                        dbutils,
                        filter_column_name,
                        filter_value,
                        data_product_id,
                        environment,
                    )
                elif action == "run_data_processing":
                    results = cls.run_data_processing(
                        obj_env,
                        config,
                        spark,
                        dbutils,
                        export_schema,
                        filter_column_name,
                        filter_value,
                        data_product_id,
                        environment,
                    )
                elif action == "run_analytics_processing":
                    results = cls.run_analytics_processing(
                        obj_env,
                        config,
                        spark,
                        dbutils,
                        export_schema,
                        filter_column_name,
                        filter_value,
                        data_product_id,
                        environment,
                    )
                elif action == "download_config":
                    results = cls.download_config(
                        config, dbutils, data_product_id, environment
                    )
                else:
                    results = "unimplemented action"

                logger.info(f"action:{action}:results:{results}")

                return results

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise ex

    @classmethod
    def run_job_action_list(
        cls,
        config: dict,
        job_action_list: list,
        obj_env_metadata: lava_env_metadata.EnvironmentMetaData,
        spark: object,
        dbutils: object,
        data_product_id: str,
        environment: str,
    ):
        """Run a list of actions for a project configured for the specified job name

        Args:
            data_product_id (str)): LAVA two part project id: example: ddt_ops
            environment (str): Environment name: example: dev
            job_action_list (list): List of actions to run
            obj_env (str): LAVA EnvironmentCore object
            spark (object): Configured SparkSession
            dbutils (object)): Delta.io dbutils object
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_job_action_list"):
            try:
                for j_a in job_action_list:
                    export_schema = j_a.get("export_schema")
                    if export_schema is None or export_schema == "":
                        export_schema = "default"

                    cls.run_job_action(
                        obj_env_metadata,
                        spark,
                        config,
                        dbutils,
                        j_a.get("action"),
                        export_schema,
                        j_a.get("filter_column_name"),
                        j_a.get("filter_value"),
                    )

                    logger.info(f"action:{j_a.get('action')} completed")
                    return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def run_ingress_processing(
        obj_env_metadata: lava_env_metadata.EnvironmentMetaData,
        config,
        spark,
        dbutils,
        filter_column_name,
        filter_value,
        data_product_id,
        environment,
    ) -> str:
        """Runs ingress processing: This is the first step in the 5-step (IDEAS) process.

        Args:
            obj_env_metadata (lava_env_metadata.EnvironmentMetaData): The environment metadata object.
            config: The configuration object.
            spark: The Spark session object.
            dbutils: The DBUtils object.
            filter_column_name: The name of the column to filter on.
            filter_value: The value to filter on.

        Returns:
            str: Ingress processing status message.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_ingress_processing"):
            try:
                data_product_id = config["data_product_id"]
                running_local = config["running_local"]
                logger.info(f"running_local:{running_local}")

                # setup database
                df_datasets = obj_env_metadata.get_dataset_list(
                    config, spark, data_product_id, environment
                )
                df_datasets = df_datasets.withColumn(
                    "is_active_standardized", F.lower(F.col("is_active").cast("string"))
                )

                import pandas as pd

                # Check if filter_column_name is NaN and set it to an empty string if it is
                if pd.isna(filter_column_name):
                    filter_column_name = None

                # In the future, make sure to
                # apply table filters to the columns dataframe
                if (
                    filter_column_name is not None
                    and filter_column_name != "all"
                    and filter_column_name.strip() != ""
                ):
                    filter_text = f"(data_product_id == '{data_product_id}') "
                    filter_text = (
                        filter_text + f" and {filter_column_name} == '{filter_value}'"
                    )
                    filter_text = (
                        filter_text
                        + " and is_active_standardized not in ('false', '0')"
                    )
                    df_datasets = df_datasets.filter(filter_text)
                    # filter for current project
                    count_string = str(df_datasets.count())
                    if count_string == "0":
                        logger.warning("No datasets to process")
                    else:
                        msg = f"df_datasets count:{count_string}"
                        logger.info(msg)
                    msg = f"filter_text:{filter_text}"
                    logger.info(msg)
                    msg = f"dataset_name:{df_datasets}"
                    logger.info(msg)

                # TODO add is_active filter logic for when there is not a filter_column_name

                # Remove the 'is_active_standardized' column
                df_datasets = df_datasets.drop("is_active_standardized")

                data_collect = df_datasets.collect()

                for dataset_metadata in data_collect:
                    obj_dataset = lava_ds_metadata.DataSetMetaData()
                    config_dataset = obj_dataset.get_configuration_for_dataset(
                        config, dataset_metadata, data_product_id, environment
                    )

                    file_format = config_dataset.get("file_format")
                    
                    if config_dataset.get("source_dataset_name"):
                        if file_format == "youtube":
                            return_text = obj_dataset.copy_youtube_file(
                                config, config_dataset, data_product_id, environment
                            )                            
                        else:
                            return_text = obj_dataset.copy_ingress_file(
                                config, config_dataset, data_product_id, environment
                            )
                    else:
                        return_text = "Skipping Ingress processing. Source_dataset_name is not configured/empty"

                    logger.info(return_text)

                return "Success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
