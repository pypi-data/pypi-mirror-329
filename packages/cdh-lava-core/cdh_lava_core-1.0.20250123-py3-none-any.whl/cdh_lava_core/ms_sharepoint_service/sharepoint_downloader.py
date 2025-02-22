from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import os
import sys

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class SharePointDownloader:

    @staticmethod
    def download_file_from_sharepoint(url, username, password, file_url, download_path, data_product_id, environment):
        """
        Downloads a file from SharePoint.

        Args:
            url (str): The URL of the SharePoint site.
            username (str): The username for authentication.
            password (str): The password for authentication.
            file_url (str): The server-relative URL of the file to download.
            download_path (str): The local path where the file will be downloaded.
            data_product_id (str): The ID of the data product.
            environment (str): The environment name.

        Raises:
            Exception: If an error occurs during the download process.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("download_file_from_sharepoint"):
            try:
                ctx_auth = AuthenticationContext(url)
                if ctx_auth.acquire_token_for_user(username, password):
                    ctx = ClientContext(url, ctx_auth)
                    web = ctx.web
                    ctx.load(web)
                    ctx.execute_query()
                    logger.info(f"Authentication successful: {web.properties['Title']}")

                    download_file = ctx.web.get_file_by_server_relative_url(file_url)
                    ctx.load(download_file)
                    ctx.execute_query()

                    with open(download_path, 'wb') as local_file:
                        local_file.write(download_file.read())
                    logger.info(f"File has been downloaded to {download_path}")

                else:
                    logger.info("Authentication failed")

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
