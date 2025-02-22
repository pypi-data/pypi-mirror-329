from smb.SMBConnection import SMBConnection
import os
import sys

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class SMBStorageFile:
    @staticmethod
    def copy_file(source_path, destination_path, smb_connection, data_product_id, environment):
        """
        Copy a file from the source path to the destination path using the SMB connection.

        Args:
            source_path (str): The path of the source file.
            destination_path (str): The path where the file will be copied to.
            smb_connection (SMBConnection): The SMB connection object.
            data_product_id (str): The ID of the data product.
            environment (str): The environment name.

        Raises:
            Exception: If an error occurs during the file copy process.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("create_virtual_environment"):
            try:
                with open(source_path, 'rb') as f:
                    smb_connection.storeFile(smb_connection.server_name,
                                             destination_path,
                                             f)
                logger.info("File copied successfully!")
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
    @classmethod
    def list_directory(cls, directory_path, smb_connection, data_product_id, environment):
        """
        List the files in a directory using the SMB connection.

        Args:
            directory_path (str): The path of the directory to list.
            smb_connection (SMBConnection): The SMB connection object.
            data_product_id (str): The ID of the data product.
            environment (str): The environment name.

        Raises:
            Exception: If an error occurs while listing the directory.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("create_virtual_environment"):
            try:
                files = smb_connection.listPath(smb_connection.server_name, directory_path)
                logger.info("Files in directory:")
                for file in files:
                    logger.info(file.filename)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


 
