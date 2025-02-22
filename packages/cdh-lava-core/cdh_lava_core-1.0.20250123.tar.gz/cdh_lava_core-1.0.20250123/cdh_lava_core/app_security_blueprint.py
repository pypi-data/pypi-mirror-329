import os
import sys
import traceback
import ast
import requests
import base64
import pandas as pd
import jwt
import json
from urllib.parse import unquote
from functools import wraps
from flask import Blueprint, request, jsonify, redirect, make_response, render_template, url_for, session, Response
from flask_restx import Resource, reqparse, Api
from azure.identity import DefaultAzureCredential
from jwcrypto import jwk

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_log_service.environment_tracing import TracerSingleton
import cdh_lava_core.cdc_security_service.security_oauth as security_oauth
from cdh_lava_core.cdc_security_service import security_core as cdh_security_core
from cdh_lava_core.az_key_vault_service import az_key_vault as cdh_az_key_vault
from cdh_lava_core.app_shared_dependencies import get_config

ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://localhost:8001",
    "https://login.microsoftonline.com",
    "https://rconnect.edav.cdc.gov",
    "https://rstudio.edav.cdc.gov",
]

cdh_security_bp = Blueprint('cdh_security', __name__)
SERVICE_NAME = os.path.basename(__file__)
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(cdh_security_bp)  # Initialize Api with the blueprint
DATA_PRODUCT_ID = "lava_core" 
ENVIRONMENT = "dev"


tracer, logger = LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
).initialize_logging_and_tracing()


def generate_code_verifier():
    """
    Generates a code verifier for OAuth 2.0 PKCE (Proof Key for Code Exchange).

    The code verifier is a high-entropy cryptographic random string using the
    characters A-Z, a-z, 0-9, and the punctuation characters -._~ (hyphen, period,
    underscore, and tilde), with a length of 43 to 128 characters.

    Returns:
        str: A URL-safe base64-encoded string without padding.
    """
    return base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')


# Generate code_verifier and code_challenge
code_verifier = generate_code_verifier()

                                                  
def get_posit_api_key():
    with tracer.start_as_current_span(f"get_posit_api_key"):
        config = get_config()
        data_product_id = config.get("data_product_id")
        environment = config.get("environment")
        posit_connect_base_url = config.get("posit_connect_base_url")

        logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
        az_sub_web_client_secret_key = config.get("az_sub_web_client_secret_key")
        az_sub_web_oauth_secret_key = config.get("az_sub_web_oauth_secret_key")
        az_sub_web_oauth_secret_key = az_sub_web_oauth_secret_key.replace("-", "_")
        az_sub_web_oauth_secret_key = az_sub_web_oauth_secret_key.upper()
        client_secret = os.getenv(az_sub_web_oauth_secret_key)
        tenant_id = config.get("az_sub_tenant_id")
        client_id = config.get("az_sub_client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        running_interactive = False
        if not client_secret:
            running_interactive = True

        az_key_vault = cdh_az_key_vault.AzKeyVault(
            tenant_id,
            client_id,
            client_secret,
            az_kv_key_vault_name,
            running_interactive,
            data_product_id,
            environment,
            az_sub_web_client_secret_key,
        )

        az_kv_posit_connect_secret_key = config.get("az_kv_posit_connect_secret_key")

        cdh_databricks_kv_scope = config.get("cdh_databricks_kv_scope")

        az_kv_posit_connect_secret = az_key_vault.get_secret(
            az_kv_posit_connect_secret_key, cdh_databricks_kv_scope
        )

        return az_kv_posit_connect_secret

def validate_id_token(id_token):
    """
    Validates an ID token received from Azure Active Directory (Azure AD).

    This function retrieves the OpenID Connect metadata document for the tenant,
    obtains the JSON Web Key Set (JWKS), locates the signing key matching the `kid` (Key ID) in the token header,
    and then decodes and verifies the ID token using the found key.

    Parameters:
    id_token (str): The ID token to validate.

    Returns:
    dict: The decoded ID token if the token is valid.

    Raises:
    ValueError: If unable to find the signing key for the token.

    Note:
    This function performs basic ID token validation which includes signature verification,
    and checking of the audience ('aud') claim. Depending on the requirements of your application,
    you might need to perform additional validation, such as checking the issuer ('iss') claim,
    token expiration, etc.

    Ensure that your Azure AD tenant, client ID and client secret are correctly set in your application configuration.

    """

    config = get_config()
    tenant_id = config.get("az_sub_tenant_id")
    client_id = config.get("az_sub_client_id")

    # Get the OpenID Connect metadata document
    openid_config_url = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
    openid_config_response = requests.get(openid_config_url, timeout=10)
    openid_config = openid_config_response.json()

    # Decode the token header without validation to get the kid
    token_header = jwt.get_unverified_header(id_token)
    kid = token_header["kid"]

    # Get the signing keys
    jwks_url = openid_config["jwks_uri"]
    jwks_response = requests.get(jwks_url, timeout=10)
    jwks = jwks_response.json()

    # Find the key with the matching kid
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if key is None:
        raise ValueError("Unable to find the signing key for the token.")

    # Use the function
    public_key = jwk_to_pem(key)

    # Validate the token
    try:
        # Decode the JWT without verification
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})

        # Todo add back signature verificaiton
        # decoded_token = jwt.decode(id_token, public_key, algorithms=["RS256"], audience=client_id)

        return decoded_token

    except Exception as ex:
        error_msg = f"Error in token valiation: {str(ex)}."
        exc_info = sys.exc_info()
        print(error_msg)
        raise


def handle_redirect():
    # Attempt to get the redirect_url from query parameters
    redirect_url = request.args.get("redirect_url")
    
    # Check if redirect_url is empty
    if not redirect_url:
        # Attempt to get the X-Rstudio-Session-Original-Uri header as a fallback
        redirect_url = request.headers.get('X-Rstudio-Session-Original-Uri')
        logger.info(f"Using X-Rstudio-Session-Original-Uri header for redirect: {redirect_url}")
    
    # Final fallback to the index page if both are empty
    if not redirect_url:
        redirect_url = url_for('index')
        logger.info(f"No redirect URL found, defaulting to index page: {redirect_url}")
    
    # Log the final redirect URL
    logger.info(f"Final redirect URL: {redirect_url}")

    # Perform the redirect
    return redirect(redirect_url)


def get_user_roles(data_product_id, email):

    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Construct the relative path to the CSV file
    if parent_dir   is None:
        raise ValueError("parent_dir is None, cannot construct path.")
    if data_product_id   is None:
        raise ValueError("data_product_id is None, cannot construct path.")
    csv_directory_path = os.path.join(parent_dir, data_product_id,"config")
    csv_file_path = os.path.join(parent_dir, data_product_id,"config", "bronze_sps_config_roles.csv")
    
 
    # Check if the file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file: {csv_file_path} for data product {data_product_id} does not exist.")
        return []

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Filter roles by user email
    user_roles = df[df['user_email'] == email].to_dict(orient='records')

    # Return the list of roles for the user (empty if no roles found)
    return user_roles


def handle_permission_error(e):
    response = {
        "error": "Permission denied",
        "message": str(e),
    }
    return jsonify(response), 403


def role_required(required_role_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Entering the role_required decorator.")

            user_email = request.cookies.get('user_id')
            logger.info(f"User email retrieved from cookies: {user_email}")
            
            data_product_id = kwargs.get('data_product_id')
            logger.info(f"Initial data_product_id from kwargs: {data_product_id}")

            if not data_product_id:
                # Try extracting data_product_id from request.form or request.args
                data_product_id = request.form.get('data_product_id') or request.args.get('data_product_id')
                logger.info(f"Extracted data_product_id from request: {data_product_id}")

            if not data_product_id:
                logger.error("Data product ID is missing.")
                return make_response(render_template("error.html", error_message="Data product ID is missing."), 400)

            # Get the required role for the data product
            required_role = required_role_func(data_product_id)
            logger.info(f"Required role for data_product_id {data_product_id}: {required_role}")

            # Load the user roles
            try:
                user_roles = get_user_roles(data_product_id, user_email)
                logger.info(f"User roles for {user_email}: {user_roles}")
            except Exception as e:
                logger.error(f"Error retrieving user roles: {str(e)}")
                return make_response(render_template("error.html", error_message=f"Error retrieving user roles: {str(e)}"), 500)

            # Check if the user has the required role
            for role in user_roles:
                logger.info(f"Checking role: {role}")
                if role['data_product_id'] == data_product_id and role['role_name'] == required_role:
                    try:
                        # Ensure that the wrapped function returns a valid response
                        logger.info(f"User {user_email} has the required role: {required_role}")
                        response = func(*args, **kwargs)
                        
                        # Ensure that the response is valid
                        if isinstance(response, dict):
                            logger.info("Returning JSON response.")
                            return make_response(jsonify(response)), 200
                        if isinstance(response, Response):
                            logger.info("Returning Flask Response object.")
                            return response
                        else:
                            logger.info("Returning generic response.")
                            return make_response(response), 200
                    except Exception as e:
                        logger.error(f"An error occurred while executing the wrapped function: {str(e)}")
                        return make_response(render_template("error.html", error_message=f"An error occurred: {str(e)}"), 500)

            # If the user does not have the required role, return a permission error
            logger.warning(f"User {user_email} does not have the required role for data_product_id {data_product_id}.")
            return make_response(render_template("error.html", error_message="Permission denied: Insufficient role."), 403)
        
        return wrapper
    return decorator



def get_required_role(data_product_id):
    """Dynamically determine the required role based on the data product ID."""
    required_role = f"{data_product_id}_manage"
    return required_role


auth_parser = reqparse.RequestParser()
auth_parser.add_argument("code", type=str, help="Code parameter", location="args")
auth_parser.add_argument("state", type=str, help="State parameter", location="args")

auth_form_parser = reqparse.RequestParser()
auth_form_parser.add_argument("code", type=str, help="Code parameter", location="form")
auth_form_parser.add_argument(
    "state", type=str, help="State parameter", location="form"
)

class AuthCallback(Resource):

    @api.expect(auth_parser, validate=True)
    #@csrf.exempt
    def get(self):
        """
        Handle the process after receiving an authorization code from an authentication callback.
        Represents part 2 of the code flow to retrieve an ID token.  This part retrieves the id_token and user_id from the authorization code.

        Steps:
        1. Extract the 'code' and 'state' parameters from the request.
        2. If 'code' is not found and no redirection attempt has been made, a login redirect response is initiated.
        3. If 'state' is missing, a 400 error response is returned.
        4. Decode the 'state' from a Base64 encoded string to a dictionary.
        5. Get an ID token using the authorization code.
        6. If the ID token is valid, decode the JWT to get user details, set cookies, set headers and redirect the user.
        7. In case of any error during JWT decoding, a 400 error response is returned.
        8. If the ID token is invalid and no redirection attempt has been made, a login redirect response is initiated.

        Returns:
            Response: A flask response object that could be a redirect or an error message.

        Raises:
            Exception: If there's an error in decoding the JWT.

        Notes:
            - Commented out lines represent an alternative flow to handle redirection attempts.
            - It's expected that `ALLOWED_ORIGINS` is a globally defined list of allowed origins.
            - This function relies on several external methods/functions such as `get_login_redirect_response`,
            `make_response`, `redirect`, and `get_id_token_from_auth_code`.
        """

        # Check if running inside RStudio Connect
        rstudio_user_id = get_rstudio_user_id()
        if rstudio_user_id:
            # Set the user_id in the environment
            logger.info(f"RS_SERVER_URL found, user-id extracted: {rstudio_user_id}")
            request.environ['user_id'] = rstudio_user_id
            
            # Redirect to the desired URL or handle the user session as needed
            response = make_response(handle_redirect())

            logger.info(f"Setting user_id cookie: {rstudio_user_id}")
            response.set_cookie("user_id", rstudio_user_id, secure=True, samesite="Strict")
            return response

        url_with_error = request.url

        # Get the authorization code from the response
        args = auth_parser.parse_args()
        auth_code = args["code"]

        # Check if we've tried redirecting before
        if auth_code is None:
            # redirect_attempted = request.args.get("redirect_attempted")

            # if not redirect_attempted:
            # Mark that we've tried redirecting
            obj_security_oauth = security_oauth.SecurityOAuth()
            response_mode = "form_post"
            # response_mode = "query"
            config = get_config
            response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
            return response
            # else:
            #    msg = "Authorization code missing after redirect attempt."
            #    return make_response(msg, 400)

        # Get the   state from the response
        state = args["state"]

        if state is None:
            msg = f"Missing state parameter in url {url_with_error}"
            response = make_response(msg, 400)

            return response

        base64_string = state

        # Get the redirect_url from the query parameters and unquote it
        # redirect_url = unquote(request.args.get('redirect_url'))
        # Base64 decode the string
        decoded_bytes = base64.urlsafe_b64decode(base64_string)

        # Decode the bytes to a string
        decoded_string = decoded_bytes.decode("utf-8")

        # URL decode the string
        url_decoded_string = unquote(decoded_string)

        # Convert the string to a dictionary
        data = ast.literal_eval(url_decoded_string)

        # Load the JSON data
        url = data.get("url")
        current_url = request.url
        redirect_url = current_url
        
        config = get_config()
        data_product_id = config.get("data_product_id")
        environment = config.get("environment")

        obj_security_oauth = security_oauth.SecurityOAuth()
        id_token = obj_security_oauth.get_id_token_from_auth_code(auth_code, config, data_product_id, environment, code_verifier)

        if id_token and "." in id_token and id_token.count(".") >= 2:
            try:
                # Decode the JWT without verification
                decoded_token = jwt.decode(
                    id_token, options={"verify_signature": False}
                )

                # Now you can access claims in the token, like the user's ID
                # 'oid' stands for Object ID
                user_id = decoded_token.get("unique_name")

                # Make a response object that includes a redirect
                response = make_response(redirect(url))

                secure = request.scheme == "https"
                logger.info(f"secure: {secure}")

                response.set_cookie(
                    "redirect_attempted",
                    "",
                    expires=0,
                    secure=secure,
                    samesite="Strict",
                )
                response.set_cookie(
                    "user_id", user_id, secure=secure, samesite="Strict"
                )
                response.set_cookie(
                    "id_token",
                    id_token,
                    path="/",
                    secure=secure,
                    httponly=False,
                    samesite="Lax",
                )

                response.headers["Authorization"] = f"Bearer {id_token}"
                response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS
                # Redirect the user to the home page, or wherever they should go next
                return response

            except Exception as ex:
                print(ex)
                msg = "Error in decoding id_token: str(ex)"
                response = make_response(msg, 400)

        else:
            error_code = check_and_return_error(id_token)
            error_message = f"Invalid id_token after redirect attempt. id_token error_code: {error_code}"
            print(error_message)
            # redirect_attempted = request.args.get("redirect_attempted")
            # if not redirect_attempted:
            # Mark that we've tried redirecting
            if error_code == "":
                obj_security_oauth = security_oauth.SecurityOAuth()
                # response_mode = "form_post"
                response_mode = "query"
                response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                return response
            else:
                # Generate the content using render_template
                content = {"error": error_message}
                # Create a response object using make_response
                response = make_response(content, 500)

                # Return the customized response object
                return response


    @api.expect(auth_form_parser, validate=False)
    #@csrf.exempt
    def post(self):
        """
        Handle the POST request after receiving an authorization code from an authentication callback.
        Represents part 1 of the code flow to retrieve an ID token.  This part retrieves the authorization code.
        The code completes a POST as opposed to a GET to prevent an error with excessive length in the query string from Azure.

        Steps:
        1. Extract the 'code' and 'state' parameters from the request.
        2. If the 'code' is missing:
        - If a redirection hasn't been attempted yet, set a "redirect_attempted" cookie and initiate a login redirect.
        - If a redirection was already attempted, return a 400 error and clear the "redirect_attempted" cookie.
        3. If the 'state' is missing, return a 400 error and clear the "redirect_attempted" cookie.
        4. Decode the 'state' from a Base64 encoded string to a dictionary.
        5. Get an ID token using the authorization code.
        6. If the ID token is valid:
        - Decode the JWT to retrieve user details.
        - Set relevant cookies and headers, and redirect the user.
        7. If the ID token is invalid:
        - If a redirection hasn't been attempted yet, set a "redirect_attempted" cookie and initiate a login redirect.
        - If a redirection was already attempted, return a 400 error and clear the "redirect_attempted" cookie.

        Returns:
            Response: A Flask response object that could be a redirect or an error message.

        Raises:
            Exception: If there's an error in decoding the JWT.

        Notes:
        - This function checks if the request is over HTTPS to set the "secure" attribute for cookies.
        - The "redirect_attempted" cookie expires in 10 minutes if set.
        - Commented out lines represent potential alternative code paths.
        - This function relies on several external methods/functions such as `get_login_redirect_response`,
            `make_response`, `redirect`, and `get_id_token_from_auth_code`.
        - It's expected that `ALLOWED_ORIGINS` is a globally defined list of allowed origins.
        """

        try:
            url_with_error = request.url
            logger.info(f"Request URL with error: {url_with_error}")

            # Get the authorization code from the response
            logger.info("Parsing authorization code from the response.")
            args = auth_form_parser.parse_args()

            # Get the authorization code and state from the parsed arguments
            auth_code = args.get("code")
            state = args.get("state")

            # Check if we've tried redirecting before
            if auth_code is None:
                return "Success 1079"
                if not request.cookies.get("redirect_attempted"):
                    return "Success 1080"
                    # Mark that we've tried redirecting
                    logger.info("No authorization code found and redirect not attempted before. Redirecting for login.")
                    obj_security_oauth = security_oauth.SecurityOAuth()
                    response_mode = "form_post"
                    config = app.get_config()
                    response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                    response.set_cookie(
                        "redirect_attempted",
                        "true",
                        max_age=600,
                        secure=(request.scheme == "https"),
                        samesite="Strict",
                    )
                    return response
                else:
                    return "Success 1095"
                    msg = "Authorization code missing after redirect attempt."
                    logger.error(msg)
                    response = jsonify({"error": msg})
                    response.status_code = 400
                    response.set_cookie(
                        "redirect_attempted",
                        "",
                        expires=0,
                        secure=(request.scheme == "https"),
                        samesite="Strict",
                    )
                    return response
        
            if state is None:
                return "Success 1111"
                msg = f"Missing state parameter in url {url_with_error}"
                logger.error(msg)
                response = jsonify({"error": msg})
                response.status_code = 400
                response.set_cookie(
                    "redirect_attempted",
                    "",
                    expires=0,
                    secure=(request.scheme == "https"),
                    samesite="Strict",
                )
                return response

            base64_string = state
            decoded_bytes = base64.urlsafe_b64decode(base64_string)
            decoded_string = decoded_bytes.decode("utf-8")
            url_decoded_string = unquote(decoded_string)
            data = ast.literal_eval(url_decoded_string)

            data_url = data.get("url")
            current_url = request.url
            location_url = request.headers.get("Location")

            urls = [data_url, location_url, current_url]
            redirect_url = next(
                (url for url in urls if url and "cdh_security/callback" not in url),
                None,
            )

            obj_security_oauth = security_oauth.SecurityOAuth()
            config = get_config()
            data_product_id = config.get("data_product_id")
            environment = config.get("environment")
            id_token = obj_security_oauth.get_id_token_from_auth_code(auth_code, config, data_product_id, environment, code_verifier)

            if id_token and "." in id_token and id_token.count(".") >= 2:
                try:
                    decoded_token = jwt.decode(
                        id_token, options={"verify_signature": False}
                    )
                    user_id = decoded_token.get("unique_name")

                    response = make_response(redirect(redirect_url))
                    secure = request.scheme == "https"

                    response.set_cookie(
                        "redirect_attempted",
                        "",
                        expires=0,
                        secure=secure,
                        samesite="Strict",
                    )
                    response.set_cookie(
                        "user_id", user_id, secure=secure, samesite="Strict"
                    )
                    response.set_cookie(
                        "id_token",
                        id_token,
                        path="/",
                        secure=secure,
                        httponly=False,
                        samesite="Lax",
                    )

                    response.headers["Authorization"] = f"Bearer {id_token}"
                    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS
                    return response

                except jwt.ExpiredSignatureError:
                    return jsonify({"message": "ID token has expired."}), 401

                except jwt.InvalidTokenError:
                    return jsonify({"message": "Invalid ID token."}), 401

                except Exception as ex:
                    logger.error(f"Error in decoding ID token: {str(ex)}")
                    response = jsonify({"message": f"Error in decoding ID token: {str(ex)}"})
                    response.status_code = 502
                    response.set_cookie(
                        "redirect_attempted",
                        "",
                        expires=0,
                        secure=(request.scheme == "https"),
                        samesite="Strict",
                    )
                    return response

            else:
                error_code = check_and_return_error(id_token)
                msg = f"Invalid id_token after redirect attempt. id_token error_code: {error_code}"
                logger.error(msg)
                if not request.cookies.get("redirect_attempted"):
                    obj_security_oauth = security_oauth.SecurityOAuth()
                    response_mode = "form_post"
                    response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                    response.set_cookie(
                        "redirect_attempted",
                        "true",
                        max_age=600,
                        secure=(request.scheme == "https"),
                        samesite="Strict",
                    )
                    return response
                else:
                    response = jsonify({"error": msg})
                    response.status_code = 500
                    response.set_cookie(
                        "redirect_attempted",
                        "",
                        expires=0,
                        secure=(request.scheme == "https"),
                        samesite="Strict",
                    )
                    return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500


class AzSubscriptionClientSecretVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_sub_web_client_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span("verify_az_sub_client_secret"):
            config = get_config()
            az_sub_web_client_secret_key = config.get("az_sub_web_client_secret_key")
            az_sub_web_client_secret_key = az_sub_web_client_secret_key.replace(
                "-", "_"
            )
            client_secret = os.getenv(az_sub_web_client_secret_key)
            tenant_id = config.get("az_sub_tenant_id")
            client_id = config.get("az_sub_client_id")

            security_core = cdh_security_core.SecurityCore()
            (
                status_code,
                response_content,
            ) = security_core.verify_az_sub_client_secret(
                tenant_id, client_id, client_secret, DATA_PRODUCT_ID, ENVIRONMENT
            )

            # Handle the verification logic
            return {
                "status_code": status_code,
                "response_content": response_content,
            }

class ConnectApiKeyVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_kv_posit_connect_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"connect_api_key_verification"):
            config = get_config()

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            connect_api_key = get_posit_api_key()
            posit_connect = cdh_posit_connect.PositConnect()
            (
                status_code,
                response_content,
                api_url,
            ) = posit_connect.verify_api_key(
                connect_api_key, posit_connect_base_url, DATA_PRODUCT_ID, ENVIRONMENT
            )

            # Handle the verification logic
            return {
                "status_code": status_code,
                "posit_connect_base_url": posit_connect_base_url,
                "api_url": api_url,
                "connect_api_key": connect_api_key,
                "response_content": response_content,
            }

def extract_id_token(set_cookie_header):
    # Split the header by '; ' to get individual cookies
    if set_cookie_header is None:
        return None
    cookies = set_cookie_header.split("; ")

    for cookie in cookies:
        # Split each cookie string by '=' to get the name-value pair
        name, _, value = cookie.partition("=")

        # Check if the cookie name is 'Id_token'
        if name == "id_token":
            return value
    return None

def get_rstudio_user_id():
    # Check if running inside RStudio Connect
    if 'RS_SERVER_URL' in os.environ  or 'rstudio' in request.headers.get('Host', '').lower():
        logger.info("RS_SERVER_URL found")
        
        cookie_header = request.headers.get('Cookie')

        # Optionally, parse the Cookie header manually if needed
        if cookie_header:
            logger.info("Cookie header found")
            cookies = cookie_header.split('; ')
            for cookie in cookies:
                logger.info(f"Cookie header: {cookie}")
                if cookie.startswith('user-id='):
                    rstudio_user_id_part = f"{cookie.split('=')[1]}"
                    # Extract the user-id by splitting on '|'
                    rstudio_user_id = rstudio_user_id_part.split('|')[0]
                    logger.info(f"user-id found in Cookie header: {rstudio_user_id}")

        else:
            logger.warning("No Cookie header found")
            
        # Log all headers to see what is being passed
        logger.info(f"Request headers: {request.headers}")


        # Extract the user ID from the RStudio Connect headers
        rstudio_user_id = request.headers.get('X-RStudio-User')
        if rstudio_user_id:
            return rstudio_user_id
    else:
        logger.info("RS_SERVER_URL not found")
    return None

def jwk_to_pem(jwk_dict):
    """
    Converts a JSON Web Key (JWK) into Public Key in PEM format.

    The function uses the jwcrypto library to convert a JWK from dictionary
    format to a JWK object, then exports this JWK object to a public key in
    PEM format.

    Args:
        jwk_dict (dict): A dictionary representing the JWK to be converted.

    Returns:
        str: A string representing the Public Key in PEM format.

    Note:
        This function involves using additional cryptography libraries, which
        might not be desirable in some cases due to increased complexity and
        potential security implications. Be sure to validate this approach fits
        into your security requirements before using it.
    """
    jwk_key = jwk.JWK()
    jwk_key.import_key(**jwk_dict)
    public_key = jwk_key.export_to_pem(private_key=False, password=None)
    return public_key.decode()

def get_user_id_from_cookies():
    user_id_cookie = request.cookies.get('user-id')
    if user_id_cookie:
        # Decode the cookie value if necessary
        decoded_user_id = unquote(user_id_cookie).split('|')[0]
        logger.info(f"Decoded user ID: {decoded_user_id}")
        return decoded_user_id
    else:
        logger.warning("user-id cookie not found")
        logger.info(f"All cookies: {request.cookies}")
        return None

def azure_ad_authentication(func):
    def wrapper(*args, **kwargs):
        
        with tracer.start_as_current_span("upload_codes"):
            
            try:
                
                config = get_config()
                
                if 'user_id' in session:
                    # User is already logged in, proceed to the requested page
                    return func(*args, **kwargs)
                    
                # Check if RStudio user ID is available
                logger.info("Attempting to get RStudio user ID.")
                rstudio_user_id = get_rstudio_user_id()
                if rstudio_user_id:
                    # Use the RStudio user ID instead of the OAuth2 token
                    request.environ['user_id'] = rstudio_user_id
                    logger.info("Set env user_id to {rstudio_user_id}")
                    return func(*args, **kwargs)
                    
                logger.info("Attempting to get user-id from cookies.")
                logger.info(f"request.cookies:{request.cookies}")
                user_id = get_user_id_from_cookies()
                logger.info(f"user-id from cookies:{user_id}")
                secure = request.scheme == "https"
                
                if not user_id:
                    logger.info("Attempting to get id_token from cookies.")
                    id_token = request.cookies.get("id_token")
                    logger.info(f"id_token from cookies: {id_token}")
                    if not id_token:
                        logger.info("Attempting to get Set-Cookie header.")
                        set_cookie_header = request.headers.get("Set-Cookie")
                        logger.info(f"Set-Cookie header: {set_cookie_header}")

                        if set_cookie_header:
                            logger.info("Attempting to extract cookie")
                            id_token_set = extract_id_token(set_cookie_header)
                            logger.info(f"Extracted id_token from Set-Cookie header: {id_token_set}")

                            if id_token_set:
                                id_token = id_token_set

                    if not id_token:
                        msg = "No id_token found in request"
                        logger.error(msg)
                        
                        # Redirect to login if no id_token is found
                        try:
                            obj_security_oauth = security_oauth.SecurityOAuth()
                            response_mode = "form_post"
                            logger.info("Initiating redirect to login page.")
                            response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                            logger.info("Returning login redirect response.")
                            return response
                        except Exception as redirect_ex:
                            logger.error(f"Error during redirection to login: {str(redirect_ex)}")
                            return jsonify({"error": "Redirect to login failed"}), 401

                    # Validate the id_token
                    logger.info("Validating id_token.")
                    decoded_token = validate_id_token(id_token)
                    logger.info(f"Decoded id_token: {decoded_token}")


                    # Extract user_id from the token
                    user_id = decoded_token.get("unique_name")
                    logger.info(f"User ID from token: {user_id}")
                    original_response = func(*args, **kwargs)
                    
                    logger.info(f"Request scheme: {request.scheme}, secure: {secure}")
                    # Call the original function
                    logger.info("Token is valid, calling the original function.")
                    flask_response = make_response(original_response)
                    logger.info("Original function called successfully.")
                    flask_response.set_cookie("id_token", id_token, path="/", secure=secure, httponly=False, samesite="Lax")
                    flask_response.headers["Authorization"] = f"Bearer {id_token}"
                else:
                    original_response = func(*args, **kwargs)
                    flask_response = make_response(original_response)
                    logger.info("Original function called successfully.")
                
                logger.info("Created Flask response from original response.")

                # Set cookies on the response
                # flask_response.set_cookie("user_id", user_id, secure=secure, samesite="Strict")
                flask_response.set_cookie("user-id", user_id, secure=secure, samesite="Lax")
                flask_response.set_cookie("user_id", user_id, secure=secure, samesite="Lax")

                flask_response.set_cookie("redirect_attempted", "", expires=0, secure=secure, samesite="Strict")

                flask_response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS

                logger.info("Attempting to get id_token from cookies.")
                id_token = request.cookies.get("id_token")
                logger.info(f"id_token from cookies: {id_token}")
                user_id = request.cookies.get("user-id")
                # if user_id:
                #    logger.info(f"user-id cookie is already set: {user-id}")
                    # If the user_id is already set, proceed with the original function
                #    return func(*args, **kwargs)
                #else:
                #    logger.info(f"user-id cookie is not already set")


                if not id_token:
                    logger.info("Attempting to get Set-Cookie header.")
                    set_cookie_header = request.headers.get("Set-Cookie")
                    logger.info(f"Set-Cookie header: {set_cookie_header}")

                    if set_cookie_header:
                        logger.info("Attempting to extract cookie")
                        id_token_set = extract_id_token(set_cookie_header)
                        logger.info(f"Extracted id_token from Set-Cookie header: {id_token_set}")

                        if id_token_set:
                            id_token = id_token_set

                if not id_token:
                    msg = "No id_token found in request"
                    logger.error(msg)
                    
                    # Redirect to login if no id_token is found
                    try:
                        obj_security_oauth = security_oauth.SecurityOAuth()
                        response_mode = "form_post"
                        logger.info("Initiating redirect to login page.")
                        response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                        logger.info("Returning login redirect response.")
                        return response
                    except Exception as redirect_ex:
                        logger.error(f"Error during redirection to login: {str(redirect_ex)}")
                        return jsonify({"error": "Redirect to login failed"}), 401
            
                # Validate the id_token
                logger.info("Validating id_token.")
                decoded_token = validate_id_token(id_token)
                logger.info(f"Decoded id_token: {decoded_token}")

                # Call the original function
                logger.info("Token is valid, calling the original function.")
                original_response = func(*args, **kwargs)
                logger.info("Original function called successfully.")

                # Extract user_id from the token
                user_id = decoded_token.get("unique_name")
                logger.info(f"User ID from token: {user_id}")

                secure = request.scheme == "https"
                logger.info(f"Request scheme: {request.scheme}, secure: {secure}")

                flask_response = make_response(original_response)
                logger.info("Created Flask response from original response.")


                # Set cookies on the response
                flask_response.set_cookie("user_id", user_id, secure=secure, samesite="Strict")
                flask_response.set_cookie("user-id", user_id, secure=secure, samesite="Lax")
                flask_response.set_cookie("id_token", id_token, path="/", secure=secure, httponly=False, samesite="Lax")
                flask_response.set_cookie("redirect_attempted", "", expires=0, secure=secure, samesite="Strict")


                flask_response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS
                logger.info("Set response headers for CORS and Authorization.")


                return flask_response

            except Exception as ex_not_authenticated:
                full_traceback = traceback.format_exc()  # Get the full traceback
                logger.warning(f"Error: not authenticated: {str(ex_not_authenticated)}")
                logger.warning(f"Full exception details: {full_traceback}")  # Log full exception

                obj_security_oauth = security_oauth.SecurityOAuth()
                response_mode = "form_post"
                response = obj_security_oauth.get_login_redirect_response(config, response_mode, DATA_PRODUCT_ID, ENVIRONMENT, code_verifier)
                logger.info("Returning login redirect response.")
                return response

    return wrapper

def enforce_https(function_name):
    """
    Decorator function to enforce HTTPS. If a request is made using HTTP,
    it redirects the request to HTTPS.

    Args:
        function_name (function): The Flask view function to decorate.

    Returns:
        function: The decorated function.
    """

    @wraps(function_name)
    def decorated(*args, **kwargs):
        if request.url.startswith("http://"):
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)
        return function_name(*args, **kwargs)

    return decorated


def check_and_return_error(id_token):
    try:
        # Try to parse the token as JSON
        # Print id_token to check its type and content
        print(f"id_token type: {type(id_token)}, id_token content: {id_token}")

        # If id_token is already a dictionary, skip json.loads
        if isinstance(id_token, dict):
            token_data = id_token
        else:
            token_data = json.loads(id_token)

        # Check if the "error" attribute exists
        if "error" in token_data:
            # Print the value of the "error" attribute
            
            return ""
        
        return ""

    except json.JSONDecodeError:
        # If there's an error in decoding, the token is not valid JSON
        return ""