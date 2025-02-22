from azure.identity import DefaultAzureCredential
from azure.storage.fileshare import ShareServiceClient, ShareFileClient
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import os
import sys

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class AzShareFile:
    
    @classmethod
    def get_file_client(cls, account_url, file_share_name, file_path, data_product_id, environment):
        """
        Returns a file client for the specified file path in the Azure Storage Share.

        Args:
            account_url (str): The URL of the Azure Storage account.
            file_share_name (str): The name of the file share.
            file_path (str): The path to the file.
            data_product_id (str): The ID of the data product.
            environment (str): The environment (e.g., development, production).

        Returns:
            azure.storage.fileshare.FileClient: The file client for the specified file path.

        Raises:
            Exception: If there is an error copying the file.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_file_to_smb"):
            try:
                credential = DefaultAzureCredential()
                service_client = ShareServiceClient(account_url, credential)
                file_share_client = service_client.get_share_client(file_share_name)
                return file_share_client.get_file_client(file_path)

            except Exception as ex:
                error_msg = f"Error copying file: {ex}"
                logger.exception(error_msg)
                raise Exception(error_msg) from ex
            
  
    @classmethod
    def list_directory(cls, account_url, file_share_name, directory_path, data_product_id, environment):
        """
        Lists all files and directories in a specified directory of the Azure File Share.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("list_directory"):
            try:
                credential = DefaultAzureCredential()
                service_client = ShareServiceClient(account_url, credential, token_intent="backup")
                directory_client = service_client.get_share_directory_client(file_share_name, directory_path)
                items = list(directory_client.list_directories_and_files(token_intent="read"))
                logger.info(f"Listed {len(items)} items in {directory_path}")
                return items
            except Exception as ex:
                error_msg = f"Error listing directory: {ex}"
                logger.exception(error_msg)
                raise Exception(error_msg) from ex
            
    @classmethod
    def upload_file(cls, file_share_name, file_path, file_content, data_product_id, environment):
        """
        Uploads a file to the specified file share.

        Args:
            file_share_name (str): The name of the file share.
            file_path (str): The path of the file within the file share.
            file_content (bytes): The content of the file to be uploaded.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the upload is performed.

        Raises:
            Exception: If an error occurs during the file upload.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_file_to_smb"):
            try:
                file_client = cls.get_file_client(file_share_name, file_path, data_product_id, environment)
                file_client.upload_file(file_content)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def download_file(cls, file_server_name, file_share_name, file_path, destination_path, data_product_id, environment):
        """
        Downloads a file from the specified file share and saves it to the destination path.

        Args:
            file_share_name (str): The name of the file share.
            file_path (str): The path of the file to download.
            destination_path (str): The path where the downloaded file will be saved.
            data_product_id (str): The ID of the data product.
            environment (str): The environment.

        Raises:
            Exception: If an error occurs during the file download.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_file_to_smb"):
            try:
                file_client = cls.get_file_client(file_share_name, file_path)
                download = file_client.download_file()
                with open(destination_path, "wb") as file:
                    file.write(download.readall())
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
    @staticmethod
    def upload_file_from_path(file_path, local_path, data_product_id, environment):
        """
        Uploads a file from the local path to the specified file path in the Azure storage share.

        Args:
            file_path (str): The destination file path in the Azure storage share.
            local_path (str): The local path of the file to be uploaded.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the upload is performed.

        Raises:
            Exception: If an error occurs during the file upload.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_file_to_smb"):
            try:
                with open(local_path, 'rb') as local_file:
                    AzShareFile.upload_file(file_path, local_file)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
 