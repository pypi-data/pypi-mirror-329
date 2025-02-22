from msal import ConfidentialClientApplication
import requests
import os
import sys

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class OneDriveClient:
    class MSOneDriveClient:
        def __init__(self, client_id, client_secret, tenant_id, data_product_id, environment):
            """
            Initializes an instance of the MSOneDriveClient class.

            Args:
                client_id (str): The client ID for authentication.
                client_secret (str): The client secret for authentication.
                tenant_id (str): The ID of the tenant.
                data_product_id (str): The ID of the data product.
                environment (str): The environment for the client.

            Attributes:
                data_product_id (str): The ID of the data product.
                environment (str): The environment for the client.
                client_id (str): The client ID for authentication.
                client_secret (str): The client secret for authentication.
                tenant_id (str): The ID of the tenant.
                authority (str): The authority URL for authentication.
                graph_endpoint (str): The Microsoft Graph API endpoint.
                access_token (str): The access token for authentication.
            """
            self.data_product_id = data_product_id
            self.environment = environment
            self.client_id = client_id
            self.client_secret = client_secret
            self.tenant_id = tenant_id
            self.authority = f'https://login.microsoftonline.com/{self.tenant_id}'
            self.graph_endpoint = 'https://graph.microsoft.com/v1.0'
            self.access_token = None

    def authenticate(self, data_product_id, environment):
        """
        Authenticates the client application and acquires an access token for Microsoft Graph API.

        Args:
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the authentication is performed.

        Raises:
            Exception: If an error occurs during authentication.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("authenticate"):
            try:
                app = ConfidentialClientApplication(
                    self.client_id,
                    authority=self.authority,
                    client_credential=self.client_secret,
                )

                token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
                self.access_token = token_response['access_token']
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    def download_file(self, file_id, local_filename, data_product_id, environment):
            """
            Downloads a file from OneDrive.

            Args:
                file_id (str): The ID of the file to download.
                local_filename (str): The name of the file to save locally.
                data_product_id (str): The ID of the data product.
                environment (str): The environment (e.g., development, production).

            Raises:
                Exception: If an error occurs during the download process.

            Returns:
                None
            """
            
            tracer, logger = LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).initialize_logging_and_tracing()

            with tracer.start_as_current_span("authenticate"):
                try:
                    if self.access_token is None:
                        self.authenticate()
                    
                    response = requests.get(
                        f'{self.graph_endpoint}/me/drive/items/{file_id}/content', 
                        headers={'Authorization': f'Bearer {self.access_token}'}
                    )

                    if response.status_code == 200:
                        with open(local_filename, 'wb') as file:
                            file.write(response.content)
                        print(f"File downloaded successfully as {local_filename}")
                    else:
                        print(f"Failed to download file: {response.status_code} - {response.text}")
                except Exception as ex:
                    error_msg = "Error: %s", ex
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise
            
# Example usage
if __name__ == "__main__":
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    tenant_id = 'your_tenant_id'
    file_id = 'your_file_id'
    local_filename = 'local_filename.ext'

    one_drive_client = OneDriveClient(client_id, client_secret, tenant_id)
    one_drive_client.download_file(file_id, local_filename)
