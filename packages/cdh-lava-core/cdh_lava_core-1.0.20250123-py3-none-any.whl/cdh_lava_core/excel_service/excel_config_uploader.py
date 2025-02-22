import os
import sys
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import cdh_lava_core.cdc_tech_environment_service.environment_file as cdc_env_file  # Assuming cdc_env_file.EnvironmentFile is defined elsewhere

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class ExcelConfigUploader:

    @staticmethod
    def get_excel_config_file_path(repository_path, data_product_id, environment, user_id):
        """
        Get the file path for the 'get_excel_excel_config_file_path.xlsx' file associated with the specified environment.

        This method constructs the file path for the 'excel_excel_configsx' file based on the provided
        repository_path and environment. The file is expected to be located in the schema directory of the specified environment.

        Args:
            repository_path (str): The path to the repository containing the schema directories.
            environment (str): The name of the environment to which the schema belongs.

        Returns:
            str: The file path for the 'excel_excel_config_for_tables_sql.xlsx' file.

        Raises:
            Exception: If any error occurs during the file path construction.

        Note:
            This method assumes that the 'excel_excel_config_for_tables_sql.xlsx' file is located within the schema directory
            of the specified environment.

        Example:
            repository_path = '/path/to/repository'
            environment = 'dev'
            excel_excel_config_file_path = get_excel_excel_config_file_path(repository_path, environment)
            print(excel_excel_config_file_path)
            # Output: '/path/to/repository/dev_excel_configs/excel_excel_config_for_tables_sql.xlsx'
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_excel_config_file_path"):
            try:
                obj_file = cdc_env_file.EnvironmentFile()
                excel_config_path = os.path.join(
                    repository_path, data_product_id.lower(), "data", "local", "xlsx", user_id.lower()
                )

                logger.info(f"excel_config_path: {excel_config_path}")
                #os.makedirs(excel_config_path, exist_ok=True)

                logger.info("excel_config_path: " + excel_config_path)
                excel_config_xls_file =  data_product_id.lower() + "_analysis_config.xlsx"

                # Join the directory path with the filename
                excel_excel_config_file_path = os.path.join(
                    excel_config_path, excel_config_xls_file
                )

                logger.info(
                    f"excel_excel_config_file_path: {excel_excel_config_file_path}"
                )

                return excel_excel_config_file_path
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
