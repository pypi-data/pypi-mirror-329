""" Module with a variety of create, read, update and delete
functions for Spark data frames. """

import sys  # don't remove required for error handling
import os

# libraries
from importlib import util
from delta.tables import DeltaTable

# spark / data
import uuid
from pyspark.sql import SparkSession
import pyspark.sql.utils
from pyspark.sql.functions import col, lit, concat_ws, udf
from pyspark.sql.types import StructType, StructField, LongType, StringType

# CDH
import cdh_lava_core.databricks_service.dataset_core as cdh_ds_core
import cdh_lava_core.cdc_tech_environment_service.environment_file as cdc_env_file


# Get the grandparent directory path
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

# Add the grandparent directory to the system path
sys.path.append(grandparent_dir)

uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton


class DataSetCrud:
    """DataSetCrud class for Spark Datasets handling create, read, update and delete operations"""

    @classmethod
    def upsert(
        cls,
        spark,
        config,
        dbutils,
        df_crud,
        full_dataset_name,
        dataset_file_path,
        is_using_dataset_folder_path_override,
        file_format,
        ingress_file_path,
        is_drop,
        partition_by,
        incremental,
        data_product_id,
        environment,
    ):
        """
        Upserts a record in the Delta dataset. If the path is empty, it creates a new dataset.
        If the dataset already exists, it merges the data.

        Args:
            spark (SparkSession): The Spark session.
            config (dict): The configuration parameters.
            dbutils: The Databricks utilities.
            df_crud (DataFrame): The DataFrame to upsert.
            full_dataset_name (str): The full name of the dataset.
            dataset_file_path (str): The file path of the dataset.
            is_using_dataset_folder_path_override (bool): Indicates whether to use the dataset folder path override.
            file_format (str): The file format of the dataset.
            ingress_file_path (str): The ingress file path.
            is_drop (bool, optional): Indicates whether to drop the existing dataset. Defaults to False.
            partition_by (str, optional): The column to partition the dataset by. Defaults to None.
            incremental (str, optional): The incremental refresh mode. Defaults to None.

        Returns:
            DataFrame: The upserted DataFrame.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span(f"upsert: {full_dataset_name}"):
            try:
                cdh_folder_database = config.get("cdh_folder_database")
                logger.info(f"{full_dataset_name} partition_by:{partition_by}")
                logger.info(f"{full_dataset_name} incremental:{incremental}")
                logger.info(f"{full_dataset_name} is_drop:{is_drop}")

                (
                    schema_name,
                    dataset_name,
                    is_managed_internal_dataset,
                    use_liquid_clustering,
                    cdh_databricks_owner_group,
                    catalog_name,
                ) = cls.get_upsert_parameters(
                    config,
                    dataset_file_path,
                    file_format,
                    is_using_dataset_folder_path_override,
                    full_dataset_name,
                    cdh_folder_database,
                    data_product_id,
                    environment,
                )

                # dataset is parquet internal to database directory and incremental refresh
                logger.info(
                    f"is_managed_internal_dataset:{is_managed_internal_dataset}"
                )
                logger.info(f"incremental:{incremental}")

                if (
                    is_managed_internal_dataset is False
                    and file_format == "parquet_delta"
                ):
                    cls.process_external_delta_dataset(
                        config,
                        logger,
                        spark,
                        full_dataset_name,
                        dataset_file_path,
                        dbutils,
                        use_liquid_clustering,
                        partition_by,
                        data_product_id,
                        environment,
                    )
                else:
                    process_results = cls.process_internal_managed_delta_dataset(
                        spark,
                        dataset_name,
                        schema_name,
                        incremental,
                        file_format,
                        ingress_file_path,
                        dataset_file_path,
                        partition_by,
                        df_crud,
                        use_liquid_clustering,
                        cdh_databricks_owner_group,
                        catalog_name,
                        data_product_id,
                        environment,
                    )
                    logger.info(f"process_results:{process_results}")
                
                return "success"
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def process_external_delta_dataset(
        config,
        logger,
        spark,
        full_dataset_name,
        dataset_file_path,
        dbutils,
        use_liquid_clustering,
        partition_by,
        data_product_id,
        environment,
    ):
        """
        Checks if a dataset file exists and drops and recreates a Delta table using the file.

        Args:
            config (dict): The configuration dictionary.
            logger (Logger): The logger object for logging messages.
            spark (SparkSession): The Spark session object.
            full_dataset_name (str): The name of the Delta dataset to be created.
            dataset_file_path (str): The file path of the dataset.
            dbutils (DbUtils): The DbUtils object for interacting with the file system.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("process_external_delta_dataset"):
            try:
                running_local = config.get("running_local")
                client_id = config.get("az_sub_client_id")
                client_secret = config.get("client_secret")
                tenant_id = config.get("az_sub_tenant_id")
                obj_env_file = cdc_env_file.EnvironmentFile()
                if obj_env_file.file_exists(
                    running_local,
                    dataset_file_path,
                    data_product_id,
                    environment,
                    dbutils,
                    client_id,
                    client_secret,
                    tenant_id,
                ):
                    sql_command = "DROP TABLE IF EXISTS " + full_dataset_name
                    spark.sql(sql_command)
                    if use_liquid_clustering and len(str(partition_by) > 0):
                        sql_command = f"CREATE TABLE  {full_dataset_name}  USING DELTA CLUSTER BY ({partition_by})"
                    else:
                        sql_command = f"CREATE TABLE  {full_dataset_name}  USING DELTA"
                    # Don't specify location to make the table managed
                    logger.info(f"attempting sql_command:{sql_command}")
                    spark.sql(sql_command)
                    logger.info(f"created Delta dataset {full_dataset_name}:")
                    logger.info(f"at {dataset_file_path}")
                else:
                    logger.error(
                        "error attempting to load a dataset file that does not exist"
                    )
                    logger.error(f"or is internal: {dataset_file_path}")

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_upsert_parameters(
        config,
        dataset_file_path,
        file_format,
        is_using_dataset_folder_path_override,
        full_dataset_name,
        cdh_folder_database,
        data_product_id,
        environment,
    ):
        """
        Get the upsert parameters based on the configuration.

        Args:
            config (dict): The configuration parameters.
            dbutils: The Databricks utilities.
            dataset_file_path (str): The file path of the dataset.
            file_format (str): The file format of the dataset.
            is_using_dataset_folder_path_override (bool): Indicates whether to use the dataset folder path override.

        Returns:
            tuple: The upsert parameters.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_upsert_parameters"):
            try:
                yyyy_param = config["yyyy"]
                mm_param = config["mm"]
                dd_param = config["dd"]

                if yyyy_param is None:
                    yyyy_param = ""

                if mm_param is None:
                    mm_param = ""

                if dd_param is None:
                    dd_param = ""

                catalog_name = None

                dataset_name_list = full_dataset_name.split(".")
                if len(dataset_name_list) == 2:
                    schema_name = dataset_name_list[0]
                    dataset_name = dataset_name_list[1]
                elif len(dataset_name_list) > 2:
                    catalog_name = dataset_name_list[0]
                    schema_name = dataset_name_list[1]
                    dataset_name = dataset_name_list[-1]
                else:
                    schema_name = None
                    dataset_name = None

                if file_format == "delta":
                    file_format = "parquet_delta"

                is_managed_internal_dataset = True
                not_found = -1

                if dataset_file_path.find(cdh_folder_database) is not_found:
                    is_using_dataset_folder_path_override = True
                    is_managed_internal_dataset = False
                elif (
                    is_using_dataset_folder_path_override is True
                    and file_format == "parquet_delta"
                ):
                    is_managed_internal_dataset = False

                partition_by = config.get("partition_by")
                if partition_by is not None and len(partition_by) > 0:
                    use_liquid_clustering = config.get("use_liquid_clustering")
                    if use_liquid_clustering is None:
                        use_liquid_clustering = False
                else:
                    use_liquid_clustering = True

                logger.info(f"schema_name:{schema_name} dataset_name:{dataset_name}")
                logger.info(f"cdh_folder_database:{cdh_folder_database}")
                logger.info(f"test if dataset exists:{dataset_name}")
                logger.info(
                    f"is_managed_internal_dataset:{is_managed_internal_dataset}"
                )
                logger.info(f"file_format:{file_format}")

                cdh_databricks_owner_group = config.get("cdh_databricks_owner_group")

                return (
                    schema_name,
                    dataset_name,
                    is_managed_internal_dataset,
                    use_liquid_clustering,
                    cdh_databricks_owner_group,
                    catalog_name,
                )

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def upsert_dataset(
        spark, df_crud, full_dataset_name, partition_by, data_product_id, environment
    ):
        """
        Upserts a dataset by writing the DataFrame `df_crud` to the specified `full_dataset_name` table in Delta format.

        Args:
            spark (pyspark.sql.SparkSession): The Spark session.
            df_crud (pyspark.sql.DataFrame): The DataFrame to be written.
            full_dataset_name (str): The name of the table to upsert the DataFrame into.
            partition_by (str): The column(s) to partition the table by. If None, the table will be unpartitioned.

        Raises:
            Exception: If any error occurs during the upsert process.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("upsert_dataset"):
            try:
                obj_ds_core = cdh_ds_core.DataSetCore()
                logger.info(f"upsert for dataset: {full_dataset_name}")
                logger.info("upsert partition_by: " + str(partition_by))
                # Consider adding delete option later but will need to support schema
                # changes and will most likely have a performance hit
                # Delete will slow down code and increase maintenance but may provide better schema change logging
                # sql_command = f"DROP TABLE IF EXISTS {full_dataset_name}"
                # sql_command = f"DELETE FROM  {full_dataset_name}"
                # spark.sql(sql_command)
                # Consider adding delete option later but will need to support schema
                # changes and will most likely have a performance hit
                # Delete will slow down code and increase maintenance but may provide better schema change logging
                # sql_command = f"DELETE FROM  {full_dataset_name}"

                # if file_format != "parquet_delta":
                # print("not parquet")


                
                    # Define the columns that should be moved to the end
                meta_columns = [
                    'meta_ingress_file_path',
                    'meta_yyyy',
                    '__meta_sheet_name',
                    'meta_dd',
                    'meta_mm',
                    'row_id'
                ]

                # Ensure columns are at the end if they exist
                all_columns = list(df_crud.columns)
                end_columns = [col for col in meta_columns if col in all_columns]
                remaining_columns = [col for col in all_columns if col not in meta_columns]

                # Reorder the columns
                final_columns = remaining_columns + end_columns
                df_crud = df_crud.select(*final_columns)

                if partition_by is not None:
                    partition_by_array = partition_by.split(",")
                    logger.info(f"writing {full_dataset_name} to")
                    logger.info(f"by {partition_by}")
                    one = 1
                    # don't merge schema for replace
                    # .option( "mergeSchema", "true")
                    if len(partition_by_array) is one:
                        logger.info(
                            "paritioned (1) parquet saveastable : managed folder"
                        )
                        partition_by = partition_by_array[0].strip()
                        df_crud.write.mode("overwrite").format("delta").partitionBy(
                            partition_by
                        ).saveAsTable(full_dataset_name)
                    else:
                        if len(partition_by_array) > one:
                            p_by_0 = partition_by_array[0].strip()
                            p_by_1 = partition_by_array[1].strip()
                            df_crud.write.mode("overwrite").format("delta").partitionBy(
                                p_by_0
                            ).partitionBy(p_by_1).saveAsTable(full_dataset_name)
                        else:
                            # no partition
                            # don't merge schema for replace
                            # .option("mergeSchema", "true")
                            logger.info(
                                "paritioned (0) parquet saveastable : non managed folder override"
                            )
                            df_crud.write.mode("overwrite").format("delta").saveAsTable(
                                full_dataset_name
                            )
                else:
                    logger.info("unparitioned parquet saveastable : managed folder")
                    # .option("mergeSchema", "true")
                    try:
                        df_crud.write.mode("overwrite").format("delta").saveAsTable(
                            full_dataset_name
                        )
                    except (
                        pyspark.errors.exceptions.connect.SparkConnectGrpcException
                    ) as ex_spark_connect:
                        logger.error(f"ex_spark_connect:{ex_spark_connect}")
                        try:
                            # Get Spark context
                            if hasattr(spark, "sparkContext"):
                                sc = spark.sparkContext
                                # Get and log Spark configuration
                                spark_conf = sc.getConf()
                                for key, value in spark_conf.getAll():
                                    logger.info(f"{key} = {value}")
                            else:
                                # Handle the case where sparkContext is not implemented
                                # e.g., log an error, raise an exception, etc.
                                logger.info(
                                    "sparkContext is not implemented in the current Spark session."
                                )
                        except Exception as ex:
                            error_msg = "Error: %s", ex
                            exc_info = sys.exc_info()
                            LoggerSingleton.instance(
                                NAMESPACE_NAME,
                                SERVICE_NAME,
                                data_product_id,
                                environment,
                            ).error_with_exception(error_msg, exc_info)
                            raise ex
                    except pyspark.sql.utils.AnalysisException as ex_analysis:
                        logger.error(f"Error saving dataframe: {full_dataset_name}")
                        logger.error("An exception occurred: " + str(ex_analysis))
                        # rename and try again
                        # .option("mergeSchema", "true")
                        sql_command = f"DROP TABLE IF EXISTS {full_dataset_name}"
                        spark.sql(sql_command)

                        try:
                            df_crud.write.mode("overwrite").format("delta").saveAsTable(
                                full_dataset_name
                            )
                        except pyspark.sql.utils.AnalysisException as ex_analysis_1:
                            logger.error("Error saving dataframe: full_dataset_name")
                            logger.error("An exception occurred: " + str(ex_analysis_1))
                            for c_original in df_crud.columns:
                                c_renamed = obj_ds_core.scrub_object_name(
                                    c_original, data_product_id, environment
                                )
                                df_crud = df_crud.withColumnRenamed(
                                    c_original, c_renamed
                                )
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def process_internal_managed_delta_dataset(
        cls,
        spark,
        dataset_name,
        schema_name,
        incremental,
        file_format,
        ingress_file_path,
        dataset_file_path,
        partition_by,
        df_crud,
        use_liquid_clustering,
        cdh_databricks_owner_group,
        catalog_name,
        data_product_id,
        environment,
    ):
        """
        Process a dataset based on the given parameters.

        This function processes an internal managed Delta dataset based on various parameters provided.
        It performs checks to determine if the dataset is internal, managed, and incremental, and then
        handles the dataset accordingly by either performing an upsert operation on existing datasets
        or creating new Delta datasets if they do not exist.

        Args:
            cls (class): The class object.
            spark (SparkSession): The Spark session object.
            dataset_name (str): The name of the dataset.
            schema_name (str): The name of the database schema.
            incremental (bool): Flag indicating whether the dataset is incremental or not.
            file_format (str): The file format of the dataset.
            ingress_file_path (str): The path of the ingress file.
            dataset_file_path (str): The path of the dataset file.
            partition_by (str): The column to partition the dataset by.
            df_crud (DataFrame): The DataFrame object for CRUD operations.
            use_liquid_clustering (bool): Flag indicating whether to use liquid clustering.
            cdh_databricks_owner_group (str): The name of the group that owns the dataset.
            catalog_name (str): The name of the catalog.
            data_product_id (str): The data product ID.
            environment (str): The environment in which the dataset is processed.

        Returns:
            str: The result of the dataset processing. Possible values are "success".

        Raises:
            ValueError: If the table is not managed and internal but is incremental.
            Exception: If there is any other error during dataset processing.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("process_internal_managed_delta_dataset"):
            try:
                # Check if the dataset is internal and managed
                is_internal = cls.is_managed_internal_dataset(dataset_name)
                is_incremental = cls.is_incremental(incremental)

                obj_ds_core = cdh_ds_core.DataSetCore()

                # Determine the qualified schema name
                if schema_name:
                    qualified_schema_name = f"{catalog_name}.{schema_name}"
                else:
                    qualified_schema_name = schema_name

                logger.info(f"qualified_schema_name:{qualified_schema_name}")

                # Check if the table exists
                table_exists = obj_ds_core.table_exists(
                    spark,
                    dataset_name,
                    qualified_schema_name,
                    data_product_id,
                    environment,
                )

                # If the table exists and is managed
                if table_exists and is_internal and is_incremental:
                    logger.info("exists and is managed - run upsert")
                    is_delta_parquet_source = cls.is_delta_parquet(file_format, dataset_name)

                    cls.handle_existing_dataset(
                        spark,
                        dataset_name,
                        ingress_file_path,
                        qualified_schema_name,
                        file_format,
                        incremental,
                        df_crud,
                        data_product_id,
                        environment,
                    )
                           
                    # Change owner of the new table
                    table_name = f"{qualified_schema_name}.{dataset_name}"
                    cls.change_table_owner(table_name, cdh_databricks_owner_group)

                    logger.info("success")
                    return "success"

                # If the table does not exist, create a new delta parquet dataset
                elif not table_exists or not is_incremental:

                    if not is_incremental:
                        if table_exists and not is_incremental:
                            logger.info("table exists but is not internal - dropping table")
                            obj_ds_core.drop_table(
                                spark,
                                dataset_name,
                                qualified_schema_name,
                                data_product_id,
                                environment,
                            )
                            
                    logger.info("table does not exist")
                    cls.create_delta_dataset(
                        spark,
                        dataset_name,
                        schema_name,
                        file_format,
                        dataset_file_path,
                        partition_by,
                        df_crud,
                        use_liquid_clustering,
                        catalog_name,
                        data_product_id,
                        environment,
                    )

                    # Change owner of the new table
                    table_name = f"{qualified_schema_name}.{dataset_name}"
                    cls.change_table_owner(table_name, cdh_databricks_owner_group)

                    logger.info("success")
                    return "success"

                else:
                    return "table is not managed and internal and exists"

            except Exception as ex:
                error_msg = "Error: %s" % ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def is_managed_internal_dataset(dataset_name):
        """
        Check if a dataset is internal.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            bool: True if the dataset is internal, False otherwise.
        """
        return dataset_name != "bronze_clc_schema"

    @staticmethod
    def is_incremental(incremental):
        """
        Check if the given value is incremental.

        Args:
            incremental (str): The value to check.

        Returns:
            bool: True if the value is 'incremental' or 'incremental_with_purge', False otherwise.
        """
        return incremental in ["incremental", "incremental_with_purge"]

    @staticmethod
    def is_delta_parquet(file_format, dataset_name):
        """
        Check if the file format is is_delta_parquet or if the dataset name is 'bronze_clc_schema'.

        Args:
            file_format (str): The file format of the dataset.
            dataset_name (str): The name of the dataset.

        Returns:
            bool: True if the file format is non-parquet or the dataset name is 'bronze_clc_schema', False otherwise.
        """
        return file_format == "parquet_delta" or dataset_name == "bronze_clc_schema"

    @classmethod
    def handle_existing_dataset(
        cls,
        spark,
        dataset_name,
        ingress_file_path,
        qualified_schema_name,
        file_format,
        incremental,
        df_crud,
        data_product_id,
        environment,
    ):
        """
        Handles an existing dataset by modifying it with new data.

        Args:
            cls (class): The class object.
            spark (SparkSession): The Spark session.
            dataset_name (str): The name of the dataset.
            ingress_file_path (str): The file path of the data to be ingressed.
            qualified_schema_name (str):  
            file_format (str): The format of the data.
            incremental (str): The incremental mode.
            df_crud (DataFrame): The DataFrame containing the new data.

        Returns:
            bool: True if the dataset is successfully modified, False otherwise.

        Raises:
            ValueError: If there is a schema mismatch between the existing dataset and the new data.
            ValueError: If the schemas do not match.
            Exception: If there is an error during the merge operation.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("handle_existing_dataset"):
            try:

                dataset_name = f"{qualified_schema_name}.{dataset_name}"
                # purge if flag is set
                if (
                    incremental == "incremental_with_purge"
                    and dataset_name != "bronze_clc_schema"
                ):
                    cls.delete_rows(
                        spark,
                        dataset_name,
                        ingress_file_path,
                        data_product_id,
                        environment,
                    )

                logger.info(f"attempting to modify existing dataset:{dataset_name}")
                logger.info(
                    f"with data from {ingress_file_path} in format {file_format}"
                )
                 
                match_expr = (
                    "delta.row_id = updates.row_id and updates.row_id = delta.row_id"
                )
                delta_dataset = None

                # for debugging
                df_crud_pandas = df_crud.toPandas()

                try:
                    # delta_dataset = DeltaTable.forPath(spark, dataset_file_path)
                    delta_dataset = DeltaTable.forName(spark, dataset_name)
                    
                    delta_schema = delta_dataset.toDF().schema
                    crud_schema = df_crud.schema
                    diff = cls.schema_difference(
                        delta_schema,
                        crud_schema,
                        "delta",
                        "updates",
                        data_product_id,
                        environment,
                    )

                    delta_schema_count = len(delta_schema.fields)
                    crud_schema_count = len(crud_schema.fields)

                    if delta_schema_count != crud_schema_count:
                        error_message = (
                            f"Schema mismatch: delta_dataset has {delta_schema_count} columns, "
                            f"while df_crud has {crud_schema_count} columns."
                        )
                        logger.warning(error_message)
                        # raise ValueError(error_message)

                    if diff != "schemas_match":
                        logger.warning(f"Schemas do not match:\n{diff}")

                    delta_dataset.alias("delta").merge(
                        df_crud.alias("updates"), match_expr
                    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
                    return True

                except Exception as exception_check:
                    logger.error(
                        "merge request input of the following dataframe:"
                        + str(exception_check)
                    )

                    if delta_dataset is not None:
                        cls.log_dataframe_info(
                            delta_dataset.history(),
                            "df_crud_history",
                            data_product_id,
                            environment,
                        )
                        cls.log_dataframe_info(
                            delta_dataset.toDF(),
                            "df_delta_pandas",
                            data_product_id,
                            environment,
                        )
                        cls.log_dataframe_info(
                            df_crud,
                            "df_crud",
                            data_product_id,
                            environment,
                        )

                    raise exception_check
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def delete_rows(
        spark, dataset_name, ingress_file_path, data_product_id: str, environment: str
    ):
        """
        Deletes rows from the specified dataset based on the given ingress file path.

        Args:
            spark (SparkSession): The Spark session object.
            dataset_name (str): The name of the dataset to delete rows from.
            ingress_file_path (str): The ingress file path used to identify the rows to delete.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("delete_rows"):
            try:
                sql_command = f"DELETE FROM {dataset_name} where __meta_ingress_file_path = '{ingress_file_path}'"
                logger.info(f"attempting sql_command:{sql_command}")
                spark.sql(sql_command)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def change_table_owner(table_name, new_owner):
        """
        Change the owner of a table in Databricks.

        :param table_name: Name of the table.
        :param new_owner: Username of the new owner.
        """
        spark = SparkSession.builder.getOrCreate()
        sql_query = f"ALTER TABLE {table_name} OWNER TO `{new_owner}`"
        spark.sql(sql_query)
        print(f"Changed owner of table {table_name} to {new_owner}")


    @classmethod
    def create_delta_dataset(
        cls,
        spark,
        dataset_name,
        schema_name,
        file_format,
        dataset_file_path,
        partition_by,
        df_crud,
        use_liquid_clustering,
        catalog_name,
        data_product_id,
        environment,
    ):
        """
        Create a Delta dataset in Spark.

        Args:
            spark (SparkSession): The Spark session.
            dataset_name (str): The name of the dataset.
            schema_name (str): The name of the database.
            file_format (str): The file format of the dataset (either "parquet" or "delta").
            dataset_file_path (str): The file path of the dataset.
            partition_by (str): The column(s) to partition the dataset by.
            df_crud (DataFrame): The DataFrame containing the dataset.
            use_liquid_clustering (str):  Indicates if should use liquid clustering
            catalog_name (str): The name of the catalog.
            data_product_id (str): Data product identifier.
            environment (str): Environment name.

        Returns:
            None

        Raises:
            Exception: If an error occurs during dataset creation.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("create_delta_dataset"):
            try:
                obj_ds_core = cdh_ds_core.DataSetCore()
                if catalog_name is not None and len(catalog_name) > 0:
                    full_dataset_name = f"{catalog_name}.{schema_name}.{dataset_name}"
                else:
                    full_dataset_name = f"{schema_name}.{dataset_name}"

                is_managed_internal_dataset = cls.is_managed_internal_dataset(dataset_name)
                qualified_schema_name = f"{catalog_name}.{schema_name}"
                
                table_exists = obj_ds_core.table_exists(
                                spark,
                                dataset_name,
                                qualified_schema_name,
                                data_product_id,
                                environment,
                            )


                logger.info(
                    f"table_exists:{table_exists}"
                )
                logger.info(
                    f"is_managed_internal_dataset:{is_managed_internal_dataset} dataset_name:{dataset_name}"
                )
                logger.info(f"schema_name:{schema_name} file_format:{file_format}")
                logger.info("attempting to create Delta dataset")
                logger.info(f"{dataset_name}: at {dataset_file_path}")

                def remove_duplicate_columns(df):
                    columns = df.columns
                    unique_columns = []
                    for col in columns:
                        if col not in unique_columns:
                            unique_columns.append(col)
                    return df.select(*unique_columns)

                # Remove duplicate columns from DataFrame
                df_crud = remove_duplicate_columns(df_crud)

                if not is_managed_internal_dataset:
                    if file_format == "parquet":
                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} USING PARQUET LOCATION '{dataset_file_path}'"
                    else:
                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} "
                    spark.sql(sql_command)
                    logger.info(f"created Delta dataset {full_dataset_name} at {dataset_file_path}")
                else:
                    if file_format == "parquet":
                        logger.info("error attempting to load a parquet directory that does not exist: {dataset_file_path}")
                    else:
                        if partition_by is not None:
                            partition_by_array = partition_by.split(",")
                            logger.info(f"writing {full_dataset_name} to {dataset_file_path} with partition by {partition_by}")

                            if len(partition_by_array) == 1 and partition_by_array[0] != '':
                                logger.info(f"creating table {full_dataset_name} using Delta format")
                                if use_liquid_clustering:
                                    partition_by_clause = ", ".join([f"{col} string" for col in partition_by_array])
                                    sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} ({partition_by_clause}) USING DELTA CLUSTER BY ({', '.join(partition_by_array)})"
                                else:
                                    partition_by_clause = ", ".join([f"{col} string" for col in partition_by_array])
                                    sql_command = f"CREATE TABLE IF NOT EXISTS  {full_dataset_name} ({partition_by_clause}) USING DELTA PARTITIONED BY ({', '.join(partition_by_array)})"
                             
                                # Check if the table exists
                                if table_exists:
                                    # Load the existing schema
                                    existing_schema = spark.table(full_dataset_name).schema
                                    existing_columns = set(existing_schema.fieldNames())
                                else:
                                    existing_columns = set()
                                    
                                # Get the schema and column names from the DataFrame
                                df_schema = df_crud.schema
                                df_columns = df_schema.fieldNames()

                                # Convert to set for easy comparison
                                df_columns_set = set(df_columns)

                                # Identify new columns
                                new_columns = df_columns_set - existing_columns

                                # Create a list of columns to select, preserving the original order
                                # Initialize the list to store selected columns
                                selected_columns = []

                                # Add columns from df_crud that are in existing_columns or new_columns, maintaining original order
                                for col in df_columns:
                                    if col in existing_columns or col in new_columns:
                                        if col not in selected_columns:
                                            selected_columns.append(col)

                                # Select these columns from the DataFrame
                                df_crud_selected = df_crud.select(selected_columns)


                                # Define the columns that should be moved to the end
                                meta_columns = [
                                    '__meta_ingress_file_path',
                                    'meta_yyyy',
                                    '__meta_sheet_name',
                                    'meta_dd',
                                    'meta_mm',
                                    'row_id'
                                ]

                                # Ensure columns are at the end if they exist
                                all_columns = list(df_crud_selected.columns)
                                end_columns = [col for col in meta_columns if col in all_columns]
                                remaining_columns = [col for col in all_columns if col not in meta_columns]

                                # Reorder the columns
                                final_columns = remaining_columns + end_columns
                                df_crud_selected = df_crud_selected.select(*final_columns)

                                # Assuming sql_command is a string containing your SQL command
                                sql_command_preview = sql_command[:255]  # Extract the first 255 characters

                                # Logging the preview of the SQL command
                                logger.info(f"writing data to table {full_dataset_name}. SQL command preview: {sql_command_preview}")

                                # Execute the SQL command
                                spark.sql(sql_command)
                                logger.info(f"writing data to table {full_dataset_name}")

                                # Write the DataFrame to the Delta table with appropriate mode
                                if table_exists:
                                    # Table exists, use append mode
                                    df_crud_selected.write.format("delta").option("mergeSchema", "true").mode("append").saveAsTable(full_dataset_name)
                                else:
                                    # Table does not exist, create the table
                                    df_crud_selected.write.format("delta").option("mergeSchema", "true").mode("overwrite").saveAsTable(full_dataset_name)
                                    
                            else:
                                if len(partition_by_array) > 1:
                                    logger.info(f"creating table {full_dataset_name} using Delta format")
                                    partition_by_clause = ", ".join([f"{col.strip()}" for col in partition_by_array])
                                    column_clause = ", ".join([f"{col.strip()} string" for col in partition_by_array])

                                    if use_liquid_clustering:
                                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} ({column_clause}) USING DELTA CLUSTER BY ({partition_by_clause}) LOCATION '{dataset_file_path}'"
                                    else:
                                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} ({column_clause}) USING DELTA PARTITIONED BY ({partition_by_clause}) LOCATION '{dataset_file_path}'"

                                    # Assuming sql_command is a string containing your SQL command
                                    sql_command_preview = sql_command[:255]  # Extract the first 255 characters

                                    # Logging the preview of the SQL command
                                    logger.info(f"writing data to table {full_dataset_name}. SQL command preview: {sql_command_preview}")

                                    spark.sql(sql_command)
                                    logger.info(f"writing data to table {full_dataset_name}")
                                    df_crud.write.format("delta").option("mergeSchema", "true").insertInto(full_dataset_name)
                                else:
                                    logger.info(f"writing {full_dataset_name} without partition")
                                    message_text = f"df_crud.write.format('delta').saveAsTable({full_dataset_name})"
                                    logger.info(message_text)
                                    df_crud.write.format("delta").option("mergeSchema", "true").saveAsTable(full_dataset_name)
                        else:
                            logger.info(f"writing {full_dataset_name} to {dataset_file_path} without partition")
                            message_text = f"df_crud.write.format('delta').saveAsTable({full_dataset_name})"
                            logger.info(message_text)
                            df_crud.write.format("delta").option("mergeSchema", "true").saveAsTable(full_dataset_name)
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    @staticmethod
    def log_dataframe_info(dataframe, name, data_product_id, environment):
        """
        Logs information about a dataframe.

        Args:
            dataframe (pyspark.sql.DataFrame): The dataframe to log information about.
            name (str): The name of the dataframe.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("log_dataframe_info"):
            try:
                df_pandas = dataframe.toPandas()
                logger.info(f"{name} head:\n{df_pandas.head(5)}")
                logger.info(f"{name} describe:\n{df_pandas.describe()}")
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def are_schemas_compatible(schema1: StructType, schema2: StructType) -> bool:
        """
        Check if two schemas are compatible.

        Args:
            schema1 (pyspark.sql.types.StructType): The first schema.
            schema2 (pyspark.sql.types.StructType): The second schema.

        Returns:
            bool: True if the schemas are compatible, False otherwise.
        """
        return schema1 == schema2

    @staticmethod
    def schema_difference(
        schema1: StructType,
        schema2: StructType,
        schema1_name,
        schema2_name,
        data_product_id,
        environment,
    ) -> str:
        """
        Compares two StructType schemas and returns the differences between them.

        Args:
            schema1 (pyspark.sql.types.StructType): The first schema to compare.
            schema2 (pyspark.sql.types.StructType): The second schema to compare.

        Returns:
            str: A string representing the differences between the schemas. If there are no differences, it returns "schemas_match."
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("schema_difference"):
            try:
                logger.info(f"comparing {schema1_name} to {schema2_name}")
                diff = []
                schema1_fields = {f.name: f.dataType for f in schema1}
                schema2_fields = {f.name: f.dataType for f in schema2}

                for name, dtype in schema1_fields.items():
                    if name not in schema2_fields:
                        diff.append(f"Field '{name}' missing in {schema2_name}")
                    elif dtype != schema2_fields[name]:
                        diff.append(
                            f"Type mismatch for field '{name}': {schema1_name} has {dtype}, {schema2_name} has {schema2_fields[name]}"
                        )

                for name, dtype in schema2_fields.items():
                    if name not in schema1_fields:
                        diff.append(f"Field '{name}' missing in {schema1_name}")

                return "\n".join(diff) if diff else "schemas_match"
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_export_dataset_or_view_schema_config(
        cls,
        config,
        config_dataset_or_notebook,
        spark,
        sorted_df,
        view_or_schema,
        data_product_id,
        environment,
    ):
        """Save metata data of dataset of view to delta lake
        Creates metadata for every column on the dataframe
        Creates a summary row with the column name "all" to summary metrics for the entire dataframe

        Args:
            config (dict): Configuration dictionary
            config_dataset_or_notebook (str): Configuration dataset or notebook name
            spark (SparkSession): Spark session object
            dbutils (DbUtils): DbUtils object
            sorted_df (DataFrame): Sorted dataframe
            view_or_schema (str): View or schema name

        Returns:
            str: Success message
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_export_dataset_or_view_schema_config"):
            try:
                obj_ds_core = cdh_ds_core.DataSetCore()
                schema_dataset_file_path = config["schema_dataset_file_path"]
                row_id_column_names = ""
                cdh_folder_database = config.get("cdh_folder_database")

                is_using_dataset_folder_path_override = False

                if view_or_schema == "view":
                    dataset_name = config_dataset_or_notebook["view_name"]
                    full_dataset_name = config_dataset_or_notebook["full_view_name"]
                    dataset_file_path = "n_a"
                else:
                    dataset_name = config_dataset_or_notebook["dataset_name"]
                    full_dataset_name = config_dataset_or_notebook["full_dataset_name"]
                    dataset_file_path = config_dataset_or_notebook["dataset_file_path"]

                row_id_keys = config_dataset_or_notebook["row_id_keys"]
                sorted_df.createOrReplaceTempView("dataset_sorted_df")

                override = config["is_export_schema_required_override"]
                cdh_schema_name = config["cdh_database_name"]
                is_export_schema_required_override = override
                schema_full_dataset_name = f"{cdh_schema_name}.bronze_clc_schema"

                if is_export_schema_required_override != "force_off":
                    clc_dataset_name = "bronze_clc_schema"
                    if (
                        obj_ds_core.table_exists(
                            spark,
                            clc_dataset_name,
                            cdh_schema_name,
                            data_product_id,
                            environment,
                        )
                        is True
                    ):
                        # Get the schema of the table to count the number of columns
                        table_schema = spark.sql(f"DESCRIBE {cdh_schema_name}.bronze_clc_schema")
                        column_count = len(table_schema.collect())

                        # Check if the full_dataset_name column exists in the table
                        table_name = f"{cdh_schema_name}.bronze_clc_schema"
                        schema = spark.table(table_name).schema
                        column_names = [field.name for field in schema]

                        if "full_dataset_name" not in column_names:
                            # Alter the table to add the full_dataset_name column
                            alter_table_sql = f"ALTER TABLE {table_name} ADD COLUMNS (full_dataset_name STRING)"
                            logger.info(f"Altering table to add column: full_dataset_name")
                            spark.sql(alter_table_sql)
                            logger.info(f"Column full_dataset_name added to table {table_name}")
                            
                        # Proceed with the delete operation only if the column count is greater than 0
                        if column_count > 0:
                            logger.info(f"delete {full_dataset_name} from: {clc_dataset_name}")
                            delete_sql = f"DELETE FROM {cdh_schema_name}.bronze_clc_schema WHERE full_dataset_name = '{full_dataset_name}'"
                            spark.sql(delete_sql)
                            logger.info("deleted rows: " + str(column_count))
                        else:
                            logger.info(f"No rows to delete for {full_dataset_name} in {clc_dataset_name}")

                    logger.info(f"describe {full_dataset_name} for: bronze_clc_schema")
                    df_schema = spark.sql("Describe Table dataset_sorted_df")
                    df_schema = df_schema.distinct()
                    df_schema = df_schema.withColumn("dataset_name", lit(dataset_name))
                    df_schema = df_schema.withColumn(
                        "full_dataset_name", lit(full_dataset_name)
                    )
                    df_schema = df_schema.withColumn(
                        "dataset_file_path", lit(dataset_file_path)
                    )
                    df_schema = df_schema.withColumnRenamed("col_name", "column_name")
                    df_schema = df_schema.withColumnRenamed(
                        "data_type", "data_type_name"
                    )
                    row_id_keys_databricks = "col('dataset_name'),col('column_name')"
                    arg_list = [
                        eval(col_name.strip())
                        for col_name in row_id_keys_databricks.split(",")
                    ]
                    df_schema = df_schema.withColumn(
                        "row_id_databricks", concat_ws("-", *arg_list)
                    )
                    if row_id_keys is None:
                        row_id_keys = ""
                    col_list = [
                        ((x.strip().replace("col('", "").replace("')", "")))
                        for x in row_id_keys.split(",")
                    ]
                    row_id_column_names = str(",".join(col_list))
                    logger.info("row_id_column_names: " + row_id_column_names)
                    logger.info("updated databricks metadata for: schema_databricks_df")

                    merged_df = df_schema
                    merged_df = merged_df.withColumn("row_id", col("row_id_databricks"))
                    merged_df = merged_df.drop("row_id_databricks")
                    merged_df = merged_df.drop("row_id_koalas")
                    merged_df = merged_df.withColumn("unique_count", lit(0))
                    merged_df = merged_df.withColumn("null_count", lit(0))
                    merged_df = merged_df.withColumn("max_length", lit(0))
                    merged_df = merged_df.withColumn("min_length", lit(0))
                    merged_df = merged_df.withColumn("ingress_column_name", lit(""))
                    merged_df = merged_df.withColumn("ingress_column_format", lit(""))
                    merged_df = merged_df.withColumn("ingress_column_label", lit(""))
                    merged_df = merged_df.withColumn("unique_count_scrubbed", lit(0))
                    merged_df = merged_df.withColumn("scope", lit("column"))
                    merged_df = merged_df.withColumn(
                        "row_id_column", lit(row_id_column_names)
                    )
                    merged_df = merged_df.withColumn("row_count", lit(0))
                    merged_df = merged_df.withColumn("ingress_row_count", lit(0))
                    merged_df = merged_df.withColumn("ingress_ordinal_position", lit(0))
                    merged_df = merged_df.withColumn("ingress_column_length", lit(0))
                    merged_df = merged_df.withColumn("ingress_table_name", lit(0))

                    schema_fields = [
                        StructField("column_name", StringType(), False),
                        StructField("data_type_name", StringType(), False),
                        StructField("comment", StringType(), True),
                        StructField("dataset_name", StringType(), False),
                        StructField("full_dataset_name", StringType(), False),
                        StructField("dataset_file_path", StringType(), False),
                        StructField("row_id", StringType(), False),
                        StructField("unique_count", LongType(), True),
                        StructField("null_count", LongType(), True),
                        StructField("max_length", LongType(), True),
                        StructField("min_length", LongType(), True),
                        StructField("ingress_column_name", StringType(), True),
                        StructField("ingress_column_format", StringType(), True),
                        StructField("ingress_column_label", StringType(), True),
                        StructField("unique_count_scrubbed", LongType(), True),
                        StructField("scope", StringType(), True),
                        StructField("row_id_column", StringType(), True),
                        StructField("row_count", LongType(), True),
                        StructField("ingress_row_count", LongType(), True),
                        StructField("ingress_ordinal_position", LongType(), True),
                        StructField("ingress_column_length", LongType(), True),
                        StructField("ingress_table_name", StringType(), True),
                    ]

                    schema = StructType(schema_fields)

                    # display(merged_df)
                    # Apply the schema to the DataFrame
                    schema_column_df = merged_df.select(
                        [
                            col(field.name).cast(field.dataType).alias(field.name)
                            for field in schema_fields
                        ]
                    )

                    key = "is_using_dataset_folder_path_override"
                    is_using_dataset_folder_path_override = config[key]
                    schema_dataset_file_path = (
                        cdh_folder_database.rstrip("/") + "/bronze_clc_schema"
                    )
                    schema_dataset_file_path = schema_dataset_file_path.replace(
                        "dbfs:", ""
                    )
                    partitioned_by = "dataset_name"

                    empty = ""
                    row_id = full_dataset_name
                    scope = "dataset"
                    row_data = [
                        (
                            ("all_columns"),
                            "n_a",
                            "",
                            dataset_name,
                            full_dataset_name,
                            dataset_file_path,
                            row_id,
                            (0),
                            (0),
                            (0),
                            (0),
                            (empty),
                            (empty),
                            (empty),
                            (0),
                            (scope),
                            "full_dataset_name",
                            (0),
                            (0),
                            (0),
                            (0),
                            (0),
                        )
                    ]

                    logger.info("row_data: " + str(row_data))
                    schema_dataset_df = spark.createDataFrame(row_data, schema)
                else:
                    partitioned_by = ""
                    schema_column_df = None
                    schema_dataset_df = None

                config_schema = {
                    "schema_column_df": schema_column_df,
                    "schema_dataset_df": schema_dataset_df,
                    "schema_full_dataset_name": schema_full_dataset_name,
                    "schema_dataset_file_path": schema_dataset_file_path,
                    "partitioned_by": partitioned_by,
                    "is_using_dataset_folder_path_override": is_using_dataset_folder_path_override,
                }

                return config_schema

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
