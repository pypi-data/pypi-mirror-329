"""
This module contains the startup code for the CDH LAVA Python application.
It imports necessary modules, defines functions for changing directories, retrieving environment variables,
creating the Flask API, and creating and configuring the Flask application instance.
"""

# Rest of the code...
from flask import Flask, Blueprint
from flask_restx import Api
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
from werkzeug.middleware.proxy_fix import ProxyFix
import importlib
import getpass 
import shutil
#from flask_wtf import CSRFProtect, FlaskForm
#from flask_wtf.csrf import generate_csrf

# Importing necessary modules from cdh_lava_core package
# These modules seem to be related to environment metadata, tracing and logging.
from cdh_lava_core.cdc_metadata_service import (
    environment_metadata as cdc_env_metadata,
)
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.az_key_vault_service.az_key_vault import AzKeyVault
from cdh_lava_core.app_shared_dependencies import set_config

# Constant indicating if the application is running inside Windows Subsystem for Linux (WSL)
RUNNING_IN_WSL = False
# Get the currently running file 
cdh_app_startup_bp = Blueprint('cdh_app_startup', __name__)
SERVICE_NAME = os.path.basename(__file__)
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(cdh_app_startup_bp)  # Ini
 
def change_to_root_directory():
    """
    Change the current working directory to the project root directory.
    """

    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Get the project root directory by going up one or more levels
    project_root = os.path.dirname(os.path.dirname(current_script_path))

    # Change the current working directory to the project root directory
    os.chdir(project_root)

def change_to_flask_directory():
    current_directory = os.getcwd()  # get current directory
    base_directory = os.path.basename(current_directory)  # get the base directory

    if base_directory != "cdh_lava_core":
        # path to the directory you want to change to
        new_directory = os.path.join(current_directory, "cdh-lava-core")

        # change to new directory
        os.chdir(new_directory)
        print(f"Directory changed to {os.getcwd()}")
    else:
        print("Current directory is already 'cdh_lava_core'")

    # Create the path to the child directory
    child_directory = os.path.join(current_directory, "cdh_lava_core")

    # Check if the child directory exists
    if os.path.exists(child_directory) and os.path.isdir(child_directory):
        new_directory = os.path.join(current_directory, "cdh_lava_core")
        # change to new directory
        os.chdir(new_directory)

def get_environment_name():
    """
    Retrieves the value of the 'POSIT_ENV_NAME' environment variable.

    Raises:
        ValueError: If the 'POSIT_ENV_NAME' environment variable is not set.

    Returns:
        str: The value of the 'POSIT_ENV_NAME' environment variable.
    """

    environment_name = os.environ.get("POSIT_ENV_NAME")
    if environment_name is None:
        environment_name = os.environ.get("FLASK_ENV")
        if environment_name is None:
            raise ValueError("The POSIT_ENV_NAME environment variable is not set.")
    if environment_name == "development":
        environment_name = "dev"
    if environment_name == "production":
        environment_name = "prod"
    return environment_name


def create_api(app, api_description):
    """
    Creates and initializes an API and its namespaces for a given app.

        Args:
            app (Flask): The Flask application instance for which the API will be created.

        Returns:
            api (FlaskRestful.Api): An instance of the Flask-Restful Api that has been initialized for the given app.

            ns_welcome (flask_restplus.Namespace): A namespace for handling welcome-related routes.

            ns_alation (flask_restplus.Namespace): A namespace for handling alation-related routes.

            ns_jira (flask_restplus.Namespace): A namespace for handling Jira-related routes.

            ns_posit (flask_restplus.Namespace): A namespace for handling Posit-related routes.

    """

    api = Api(
        app,
        version="1.0",
        title="CDC Data Hub LAVA Flask API",
        description=api_description,
        doc="/api/swagger",
        url="/api/swagger",
        api_docs="/api/swagger"
    )

    ns_welcome = api.namespace(
        "welcome", description="Welcome to the CDC Data Hub LAVA API"
    )

    TECH_ENVIRONMENT_DESCRIPTION = (
        "The tech-environment service manages the technical environment in which "
        "the data products and associated services are developed, deployed, and "
        "managed. This package contains datasets that provide critical information "
        "for understanding the technical architecture, components, and "
        "resources used to support the data products and associated services."
    )

    ns_tech_environment = api.namespace(
        "tech_environment",
        description=TECH_ENVIRONMENT_DESCRIPTION,
    )


    GREAT_EXPECTATIONS_DESCRIPTION = (
        "The Great Expectations service ensures the confidentiality, integrity, and availability of CDC Data Hub (CDC Data Hub LAVA) "
        "data products and associated services. It manages quality control measures required to "
        "safeguard sensitive public health data while delivering the necessary datasets and services to uphold robust quality assurance."
    )

    ns_great_expectations = api.namespace(
        "great_expectations",
        description=GREAT_EXPECTATIONS_DESCRIPTION,
    )

    CDH_SECURITY_DESCRIPTION = (
        "The security service ensures the confidentiality, integrity, and availability of CDC Data Hub (CDC Data Hub LAVA) "
        "data products and associated services. It manages access control, encryption, audit logging, and other security "
        "measures to protect sensitive public health data, while providing the necessary datasets and services to maintain a robust security posture."
    )

    ns_cdh_security = api.namespace(
        "cdh_security",
        description=CDH_SECURITY_DESCRIPTION,
    )

    CDH_ORCHESTRATION_DESCRIPTION = (
        "The CDC Data Hub Lifecycle, Analysis, and Visualization Accelerator (CDC Data Hub LAVA) "
        "streamlines the orchestration of building and deploying data products, making these processes "
        "more efficient and reliable by standardizing public health data workflows and technologies."
    )

    ns_cdh_orchestration = api.namespace(
        "cdh_orchestration",
        description=CDH_ORCHESTRATION_DESCRIPTION,
    )

    CDH_CONFIGURATION_DESCRIPTION = (
        "The CDC Data Hub Lifecycle, Analysis, and Visualization Accelerator (CDC Data Hub LAVA) "
        "facilitates efficient configuration management for data products by standardizing configuration "
        "practices, ensuring consistency and reducing errors in the deployment of public health data solutions."
    )

    ns_cdh_configuration = api.namespace(
        "cdh_configuration",
        description=CDH_CONFIGURATION_DESCRIPTION,
    )

    CDH_OBSERVABILITY_DESCRIPTION = (
        "The CDC Data Hub Lifecycle, Analysis, and Visualization Accelerator (CDC Data Hub LAVA) "
        "provides enhanced observability into the health and performance of data pipelines and products, "
        "ensuring transparency and reliability through standardized monitoring and diagnostics."
    )

    ns_cdh_observability = api.namespace(
        "cdh_observability",
        description=CDH_OBSERVABILITY_DESCRIPTION,
    )

 
    BUSINESS_DESCRIPTION = (
        "The business service manages the business context and meaning of the data "
        "products and associated services. This package contains datasets that "
        "provide critical information for understanding the business context, "
        "meaning, and usage of the data products and associated services."
    )

    ns_business = api.namespace(
        "business",
        description=BUSINESS_DESCRIPTION,
    )

    CDC_ADMIN_DESCRIPTION = (
        "The admin service manages and monitors data products and associated logs. "
        "This package contains datasets that provide critical information for "
        "ensuring the availability, performance, and quality of the data products "
        "and related services."
    )

    ns_cdc_admin = api.namespace(
        "cdc_admin",
        description=CDC_ADMIN_DESCRIPTION,
    )

    ALATION_DESCRIPTION = "The Alation service manages and monitors Alation."
    ns_alation = api.namespace("alation", description=ALATION_DESCRIPTION)

    JIRA_DESCRIPTION = (
        "The JIRA service provides read-only reporting and query services for JIRA."
    )

    ns_jira = api.namespace(
        "jira",
        description=JIRA_DESCRIPTION,
    )

    POSIT_DESCRIPTION = (
        "The POSIT service provides read-only reporting and query services for "
        "POSIT.  It also provides methods for automated app creation and publication "
        "of web applications via ManifestJson files."
    )

    ns_posit = api.namespace(
        "posit",
        description=POSIT_DESCRIPTION,
    )
    
    ALTMETRIC_DESCRIPTION = (
        "The ALTMETRIC service provides read-only reporting and query services for "
        "ALTMETRIC. This service is tailored to provide users with comprehensive insights "
        "into the altmetric scores and the broader impact of scholarly work beyond traditional "
        " citation metrics. "
    )

    ns_altmetric = api.namespace(
        "altmetric",
        description=ALTMETRIC_DESCRIPTION,
    )
    
    api.add_namespace(ns_welcome)
    api.add_namespace(ns_tech_environment)
    api.add_namespace(ns_cdh_security)
    api.add_namespace(ns_business)
    api.add_namespace(ns_cdc_admin)
    api.add_namespace(ns_jira)
    api.add_namespace(ns_alation)
    api.add_namespace(ns_posit)
    api.add_namespace(ns_altmetric)
    api.add_namespace(ns_cdh_orchestration)
    api.add_namespace(ns_cdh_configuration)
    api.add_namespace(ns_cdh_observability)
    api.add_namespace(ns_great_expectations)

    return (
        api,
        ns_welcome,
        ns_alation,
        ns_jira,
        ns_posit,
        ns_cdc_admin,
        ns_cdh_security,
        ns_altmetric,
        ns_cdh_orchestration,
        ns_cdh_configuration,
        ns_cdh_observability,
        ns_great_expectations
    )


# def get_connect_api_key(config, az_client_secret, running_interactive):
#     # Get the connect_api_key from the environment variable
#     connect_api_key = os.environ.get("LAVA_CORE_DEV_POSIT_CONNECT_SECRET")

#     tenant_id = config.get("az_sub_tenant_id")
#     client_id = config.get("az_sub_web_client_id")
#     az_kv_key_vault_name = config.get("az_kv_key_vault_name")


#     # If the environment variable is blank or not set, fetch the secret from Azure Key Vault
#     if not connect_api_key:
#         print("Could not find enviornment variable LAVA_CORE_DEV_POSIT_CONNECT_SECRET")
#         connect_api_key = az_key_vault.get_secret(
#             "OCIO-CDH-DEV-POSIT-CONNECT-SECRET")

#     return connect_api_key


def create_app():
    """
    This function is used to create and configure a Flask application instance.

    Returns:
        app (flask.Flask): The Flask application instance.

    Example:
        app = create_app()

    Note:
        This function currently has no functionality. You should add Flask app creation and configuration logic inside it.

    """
    # Add your Flask app creation and configuration logic here

    # Get the path to the .env file

    CURRENT_USER_NAME = os.getenv("USERNAME") or os.getenv("USER") or getpass.getuser()
    API_PATH = "/cdh-lava-core/cdh_lava_core"

    peer_lava_core_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lava_core')
    # Define the path to the .env file within the peer lava_core directory
    dotenv_path = os.path.join(peer_lava_core_dir, ".env")

    if not os.path.exists(dotenv_path):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    # Load the .env file
    load_dotenv(dotenv_path)

    # set_key(dotenv_path, "PYARROW_IGNORE_TIMEZONE",
    #        "1")
    # set_key(dotenv_path, "APPLICATIONINSIGHTS_CONNECTION_STRING",
    #        f"InstrumentationKey={instrumentation_key};IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/")
    # set_key(dotenv_path, "APPINSIGHTS_INSTRUMENTATIONKEY",
    #        instrumentation_key)
    # Reload the updated .env file
    # load_dotenv(dotenv_path)

    environment = get_environment_name()
    data_product_id = "lava_core"
    data_product_id_root = "lava"
    data_product_id_individual = "core"

    # try:
    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
    ).initialize_logging_and_tracing()

    app = None

    try:
        with tracer.start_as_current_span("create_app"):
            # Get the absolute path of the directory of the current script
            dir_path = os.path.dirname(os.path.realpath(__file__))

            # Add this path to PYTHONPATH
            sys.path.insert(0, dir_path)

            logger.info("ran create_app")

            obj_env_metadata = cdc_env_metadata.EnvironmentMetaData()

            running_local = True
            change_to_root_directory()
            path = Path(os.getcwd())
            repository_path_default = str(path)

            logger.info(f"repository_path_default:{repository_path_default}")

            parameters = {
                "data_product_id": data_product_id,
                "data_product_id_root": data_product_id_root,
                "data_product_id_individual": data_product_id_individual,
                "environment": environment,
                "repository_path": repository_path_default,
                "running_local": running_local,
            }
            config = obj_env_metadata.get_configuration_common(
                parameters, None, data_product_id, environment
            )

            logger.info(f"config_length:{len(config)}")

            app = Flask(__name__)

            app.wsgi_app = ProxyFix(
                app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
            )

            app.env = "development"
            app.debug = True  # Enable debug mode

            set_config(config)
            app.cdc_config = config
            env_file_path = config.get("env_file_path")
            env_file_path = env_file_path.replace("//", "/")
            source_file = os.path.join(app.root_path, '.env')

            # Check if the root path exists and is a directory
            if os.path.exists(source_file):
                # Copy the file
                try:
                    shutil.copy(source_file, env_file_path)
                    print(f"File copied from {source_file} to {env_file_path}")
                except FileNotFoundError:
                    print(f"Source file {source_file} not found.")
                except PermissionError:
                    print(f"Permission denied while copying to {env_file_path}.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f"Root path {source_file} does not exist.")

            load_dotenv(env_file_path)

            az_sub_web_oauth_secret_key = config.get("az_sub_web_oauth_secret_key")
            az_sub_web_oauth_secret_key = az_sub_web_oauth_secret_key.replace(
                "-", "_"
            ).upper()
            
            tenant_id = config.get("az_sub_tenant_id")
            client_id = config.get("az_sub_client_id")
            vault_url = config.get("az_kv_key_vault_name")

            if not vault_url:
                raise ValueError("vault_url from az_kv_key_vault_name in config is empty")

            az_sub_web_oauth_secret_key = config.get("az_sub_web_oauth_secret_key")
            if not az_sub_web_oauth_secret_key:
                raise ValueError("az_sub_web_oauth_secret_key in config is empty")

            converted_string = az_sub_web_oauth_secret_key.upper().replace("-", "_")
            client_secret = os.getenv(converted_string)
            if not client_secret:
                client_secret = None


            az_sub_web_spn_secret_key = config.get("az_sub_web_client_secret_key")

            if not az_sub_web_spn_secret_key:
                raise ValueError("az_sub_web_spn_secret_key in config is empty")

            if client_secret is None:            
                obj_key_vault_interactive = AzKeyVault(
                    tenant_id,
                    client_id,
                    client_secret,
                    vault_url,
                    True,
                    data_product_id,
                    environment,
                    az_sub_web_spn_secret_key
                )
                
                client_secret = obj_key_vault_interactive.get_secret(az_sub_web_oauth_secret_key)
            
                logger.info(
                    f"az_sub_web_oauth_secret_key:{az_sub_web_oauth_secret_key}"
                )

            if not client_secret:
                raise ValueError(f"client_secret:{az_sub_web_oauth_secret_key} is empty or has a length of 0")
            
            logger.info(f"client_secret length:{len(str(client_secret))}")
            app.secret_key = client_secret

            # SET THE MICROSOFT REQUIRED ENVIRONMENT VARIABLE FOR SECRET
            os.environ["AZURE_CLIENT_SECRET"] = client_secret

            # Set the new value
            # set_key(dotenv_path, "FLASK_DEBUG", "1")
            # set_key(dotenv_path, "PYARROW_IGNORE_TIMEZONE", "1")

            # Reload the updated .env file
            # load_dotenv(dotenv_path)

            # Trim leading and trailing whitespace from client_secret
            if client_secret is None:
                logger.warning("client_secret is None")
            else:
                client_secret = client_secret.strip()

            # Check if the client_secret is None or a zero-length string
            if not client_secret:
                running_interactive = True

            # set_key(dotenv_path, az_sub_web_client_secret_key, client_secret)
            # set_key(dotenv_path, "CONNECT_API_KEY", connect_api_key)

            logger.info(f"env_file_path:{env_file_path}")

            try:
                importlib.import_module("cdh_lava_core")
                logger.info("cdh_lava_core is module in pythonpath")
            except ImportError:
                logger.warning("cdh_lava_core is not a module in pythonpath")

            if RUNNING_IN_WSL is True:
                sys.path.append(f"/home/{CURRENT_USER_NAME}{API_PATH}")
                logger.info(f"RUNNING_IN_WSL: {RUNNING_IN_WSL}")
                logger.info(f"/home/{CURRENT_USER_NAME}{API_PATH}")
            else:
                sys.path.append(os.path.abspath(__file__ + "/../../../cdh_lava_core/"))
                logger.info(f"RUNNING_IN_WSL: {RUNNING_IN_WSL}")
                logger.info(os.path.abspath(__file__ + "/../../../cdh_lava_core/"))

            app.tracer = tracer
            app.logger = logger

            # Initialize CSRF protection
            #csrf = CSRFProtect()
            #csrf.init_app(app)

            return app
    except Exception as ex:
        if app is not None:
            error_msg = "Error: %s", ex
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).error_with_exception(error_msg, exc_info)

        raise

