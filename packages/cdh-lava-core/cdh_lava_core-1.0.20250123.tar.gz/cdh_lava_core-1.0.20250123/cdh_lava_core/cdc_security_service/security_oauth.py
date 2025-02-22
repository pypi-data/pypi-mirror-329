import json
import base64
import requests
import os
import sys
from urllib.parse import urlencode, quote_plus, urlparse, urlunparse
from flask import request, redirect, make_response
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import hashlib

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://localhost:8001",
    "https://login.microsoftonline.com",
    "https://rconnect.edav.cdc.gov",
    "https://rstudio.edav.cdc.gov",
]

class SecurityOAuth:



    @staticmethod
    def generate_code_challenge(code_verifier):
        code_challenge_digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(code_challenge_digest).decode('utf-8').rstrip('=')

    @classmethod
    def get_login_redirect_response(cls, config, response_mode, data_product_id, environment, code_verifier):
        # response_mode options are form_post and query
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_login_redirect_response"):
            try:
                tenant = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")

                # Define the base URL for Azure AD authorization
                base_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"

                current_url = request.url

                # Encode the current URL in the state parameter
                state = cls.encode_state(current_url)

                callback_url = cls.get_callback_url(data_product_id, environment)
                code_challenge = cls.generate_code_challenge(code_verifier)
                code_challenge_method = "S256"
                logger.info(f"code_verifier:{code_verifier}")
                params = {
                    "client_id": client_id,
                    "response_type": "code",
                    "redirect_uri": callback_url,
                    "response_mode": response_mode,
                    "scope": "openid profile email",
                    "state": state,
                    "code_challenge": code_challenge,
                    "code_challenge_method": code_challenge_method
                }

                # URL encode the parameters
                params_encoded = urlencode(params, quote_via=quote_plus)

                # Construct the full Azure AD authorization URL
                auth_url = f"{base_url}?{params_encoded}"

                response = make_response(redirect(auth_url))
                return response

            except Exception as ex:
                error_message = f"Error processing login redirect. Details: {str(ex)}."
                response = make_response({"error": error_message}, 500)
                cls.log_and_set_cookie(response, error_message, secure=request.scheme == "https")
                return response

    @staticmethod
    def encode_state(current_url):
        """Encodes the current URL to be used in the state parameter."""
        data = {"url": current_url}
        json_data = json.dumps(data)
        json_bytes = json_data.encode("utf-8")
        base64_data = base64.urlsafe_b64encode(json_bytes)
        return base64_data.decode("utf-8")

    @staticmethod
    def get_callback_url(data_product_id, environment):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_callback_url"):
            try:
                current_url = request.url
                url_parts = urlparse(current_url)
                directories = url_parts.path.split("/")[:-2]

                # TODO: FIX HACK - should be more generic
                # Remove 'cdh_configuration' if it's in the path
                if "cdh_configuration" in directories:
                    directories.remove("cdh_configuration")

                directories.append("cdh_security/callback")
                new_path = "/".join(directories)

                new_path = new_path.replace("127.0.0.1", "localhost")

                if os.name == "nt":
                    new_path = new_path.replace("127.0.0.1", "localhost")

                callback_url = urlunparse((url_parts.scheme, url_parts.netloc, new_path, None, None, None))
                return callback_url

            except Exception as ex:
                error_msg = f"Error constructing callback URL: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_access_token(tenant_id, client_id, client_secret, code, redirect_uri, data_product_id, environment):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_access_token"):
            try:
                token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

                data = {
                    'grant_type': 'authorization_code',
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'scope': 'openid profile email'
                }

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                logger.debug(f"Token URL: {token_url}")
                logger.debug(f"Data: {data}")
                logger.debug(f"Headers: {headers}")

                response = requests.post(token_url, headers=headers, data=data)
                response.raise_for_status()
                if response.status_code == 200:
                    tokens = response.json()
                    access_token = tokens.get('access_token')
                    id_token = tokens.get('id_token')
                    refresh_token = tokens.get('refresh_token')
                    logger.info(f'Access token length: {len(access_token) if access_token else "None"}')
                    logger.info(f'ID token length: {len(id_token) if id_token else "None"}')
                    logger.info(f'Refresh token length: {len(refresh_token) if refresh_token else "None"}')
                    if id_token:
                        return id_token
                    else:
                        raise ValueError(f"Failed to obtain ID token. Response: {tokens}")
                else:
                    raise ValueError(f"Failed to obtain ID token. Response: {response.json()}")

            except Exception as ex:
                error_msg = f"Error getting ID token: {str(ex)}"
                exc_info = sys.exc_info()
                logger.error(error_msg, exc_info=exc_info)
                raise

    @staticmethod
    def log_and_set_cookie(response, error_message, secure):
        LoggerSingleton.instance(NAMESPACE_NAME, SERVICE_NAME, "", "").error(error_message)
        response.set_cookie(
            "redirect_attempted",
            "",
            expires=0,
            secure=secure,
            samesite="Strict",
        )

    @classmethod
    def handle_callback(cls, config, data_product_id, environment):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("handle_callback"):
            try:
                code = request.form.get('code')
                state = request.form.get('state')
                client_id = config.get("az_sub_client_id")
                client_secret = config.get("az_sub_client_secret")
                tenant_id = config.get("az_sub_tenant_id")
                redirect_uri = cls.get_callback_url(data_product_id, environment)

                id_token = cls.get_access_token(tenant_id, client_id, client_secret, code, redirect_uri, data_product_id, environment)

                return id_token

            except Exception as ex:
                error_msg = f"Error handling callback: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_id_token_from_auth_code(cls, auth_code, config, data_product_id, environment, code_verifier):
        """
        Exchange an authorization code for an access token from Azure AD.

        This function sends a POST request to the Azure AD token endpoint with the
        provided authorization code and application's client ID, secret, and redirect URI.
        If the request is successful, the function returns the access token.

        Args:
            auth_code (str): The authorization code received from Azure AD.
            redirect_uri (str): The redirect URI of your application as registered in Azure AD.

        Returns:
            str: The access token if the request is successful; None otherwise.

        Example:
            access_token = get_id_token_from_auth_code(auth_code, redirect_uri)
            if access_token:
                print("Successfully received access token.")
            else:
                print("Failed to receive access token.")

        Note:
            Replace the "client_id", "client_secret", and "tenant_id" placeholders with your actual Azure AD client ID,
            client secret, and tenant ID. The redirect_uri must match exactly with the one used in the authorization
            request and the one configured in your Azure AD app registration.

            The function does not handle errors. In a production environment, you should add error handling code to
            deal with potential issues, like network errors or an invalid authorization code.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()


        with tracer.start_as_current_span("handle_callback"):
            try:
                        
                az_sub_client_secret_key = config.get("az_sub_client_secret_key","")
                if not az_sub_client_secret_key:
                    raise ValueError(f"Config az_sub_client_secret_key '{az_sub_client_secret_key}' is not set or is empty.")
 
                az_sub_client_secret_key = az_sub_client_secret_key.replace("-", "_").upper()
                logger.info(f"az_sub_client_secret_key: {az_sub_client_secret_key}")
                logger.info(f"az_sub_client_secret_key length: {len(az_sub_client_secret_key)}")
                
                client_secret = os.getenv(az_sub_client_secret_key)
                if not client_secret:
                    raise ValueError(f"Environment variable '{az_sub_client_secret_key}' is not set or is empty.")
                
                logger.info(f"client_secret length: {len(client_secret)}")
                tenant_id = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_client_id")

                # Azure AD token endpoint
                token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
                logger.info(f"token_url: {token_url}")
                 
                callback_url = cls.get_callback_url(data_product_id, environment)
                logger.info(f"callback_url: {callback_url}")

                # Data for the token request
                token_data = {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': auth_code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': callback_url,
                    'code_verifier': code_verifier,  # Use the verifier generated during authorization request
                    'scope': 'openid profile email'
                }

                # Log non-sensitive parts of token_data
                secure_token_data = token_data.copy()
                secure_token_data['client_secret'] = "*****"  # Mask the client secret
                logger.info("Token request data: %s", {k: v for k, v in secure_token_data.items() if k != 'client_secret'})

                # If the request was successful, return the access token
                try:
                    # Send a POST request to the token endpoint

                    response = requests.post(token_url, data=token_data)

                    # Log response for debugging
                    logger.info("Token response: %s", response.json())

                    # response.headers = CaseInsensitiveDict()
                    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS
                    response.raise_for_status()
                    return response.json()["access_token"]

                except Exception as ex:
                    msg = f"An unexpected error occurred: {str(ex)}"
                    if "response" in locals():  # Check if 'response' is defined
                        msg += f" Response text: {response.text}"
                    exc_info = sys.exc_info()
                    # logger_singleton.error_with_exception(msg, exc_info)
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).force_flush()
                    return {"error": f"An unexpected error occurred: {msg}"}
            except Exception as ex:
                error_msg = f"Error handling callback: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment).error_with_exception(error_msg, exc_info)
                raise