from cdh_lava_core.databricks_service.dbx_db_rest import RestClient
from cdh_lava_core.databricks_service.dbx_rest.common import ApiContainer

import requests
import subprocess
import json

class TokenManagementClient(ApiContainer):
    def __init__(self, client: RestClient):
        self.client = client
        self.base_url = f"{self.client.endpoint}/api/2.0/token-management"

    def create_on_behalf_of_service_principal(
        self, application_id: str, comment: str, lifetime_seconds: int
    ):
        params = {
            "application_id": application_id,
            "comment": comment,
            "lifetime_seconds": lifetime_seconds,
        }
        return self.client.execute_post_json(
            f"{self.base_url}/on-behalf-of/tokens", params=params
        )

    def list(self):
        results = self.client.execute_get_json(url=f"{self.base_url}/tokens")
        return results.get("token_infos", [])

    def delete_by_id(self, token_id):
        return self.client.execute_delete_json(url=f"{self.base_url}/tokens/{token_id}")

    def get_by_id(self, token_id):
        return self.client.execute_get_json(url=f"{self.base_url}/tokens/{token_id}")


    def create_using_ad(self, resource_id, databricks_host, token_lifetime_seconds=3600, comment="Generated token"):
        """
        Create a Databricks token using Azure Active Directory (AAD) authentication.

        Parameters:
        - resource_id: The specific resource ID for Databricks in Azure.
        - databricks_host: The URL of the Databricks workspace.
        - token_lifetime_seconds: Lifetime of the generated token in seconds.
        - comment: A comment to associate with the generated token.

        Returns:
        - A dictionary with the token response from Databricks.
        """
        
        # Acquire AAD token using Azure CLI
        cmd_get_token = f"az account get-access-token --resource={resource_id}"
        result = subprocess.run(cmd_get_token, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        aad_token = json.loads(result.stdout)['accessToken']
        
        # Set the headers for the request to Databricks
        headers = {
            "Authorization": f"Bearer {aad_token}"
        }

        # Set the payload for the POST request
        data = {
            "lifetime_seconds": token_lifetime_seconds,
            "comment": comment
        }

        # Make the POST request to create a Databricks token
        response = requests.post(f"{databricks_host}/api/2.0/token/create", json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            token_response = response.json()
            return token_response
        else:
            # Handle errors (e.g., by throwing an exception or returning an error message)
            return {"error": "Failed to create Databricks token", "status_code": response.status_code}

