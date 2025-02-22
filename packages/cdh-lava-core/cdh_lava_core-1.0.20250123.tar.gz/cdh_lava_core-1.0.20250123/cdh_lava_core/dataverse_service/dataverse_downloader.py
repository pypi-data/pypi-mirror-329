
import requests
from msal import PublicClientApplication

class DataverseDownloader:
    """
    Static class for Dataverse API requests using OAuth 2.0 interactive authentication.
    """
    client_id = None
    tenant_id = None
    resource = None
    redirect_uri = "http://localhost"  # Redirect URI for interactive login

    @staticmethod
    def configure(client_id: str, tenant_id: str, resource: str):
        """
        Configure the static class with Dataverse credentials.
        """
        DataverseDownloader.client_id = client_id
        DataverseDownloader.tenant_id = tenant_id
        DataverseDownloader.resource = resource

    @staticmethod
    def get_access_token() -> str:
        """
        Acquire an access token using MSAL public client (interactive login).
        """
        if not all([DataverseDownloader.client_id, DataverseDownloader.tenant_id, DataverseDownloader.resource]):
            raise ValueError("Dataverse credentials are not configured.")

        # Create the MSAL public client application
        app = PublicClientApplication(
            DataverseDownloader.client_id,
            authority=f"https://login.microsoftonline.com/{DataverseDownloader.tenant_id}"
        )

        # Attempt silent login (token cache)
        accounts = app.get_accounts()
        if accounts:
            token_response = app.acquire_token_silent([f"{DataverseDownloader.resource}/.default"], account=accounts[0])
        else:
            token_response = None

        # Interactive login if no cached token
        if not token_response:
            print("No cached token found. Launching interactive login...")
            token_response = app.acquire_token_interactive(
                scopes=[f"{DataverseDownloader.resource}/.default"],
                redirect_uri=DataverseDownloader.redirect_uri
            )

        if "access_token" not in token_response:
            raise Exception(f"Failed to acquire token: {token_response.get('error_description', 'No error description')}")

        return token_response["access_token"]

    @staticmethod
    def get_entity_data(entity_name: str) -> dict:
        """
        Perform a GET request to the specified Dataverse entity (e.g., 'contacts').
        """
        token = DataverseDownloader.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        api_url = f"{DataverseDownloader.resource}/api/data/v9.1/{entity_name}"
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
        
        return response.json()

# Example usage:
if __name__ == "__main__":
    # Configure with your credentials
    DataverseDownloader.configure(
        client_id="YOUR_CLIENT_ID",  # Client ID of the registered app (must be a "public" app)
        tenant_id="YOUR_TENANT_ID",
        resource="https://cdhrs.crm9.dynamics.com"
    )

    # Fetch contacts
    contacts_data = DataverseDownloader.get_entity_data("contacts")
    print(contacts_data)
