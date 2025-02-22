"""
This module contains functions for installing and setting up the CDH LAVA Python library.

"""

import sys
import os
import subprocess
import importlib.util
import pandas as pd

print("cwd:" + os.getcwd())
try:
    import cdh_lava_core
except ImportError:
    import cdh_lava_core_lib.cdh_lava_core as cdh_lava_core


# Now you can use cdh_lava_core to refer to cdh_lava_core_lib.cdh_lava_core

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


def is_package_installed(package_name: str = "cdh_lava_core"):
    """Check if a package is installed.

    Args:
        package_name (str): The name of the package to check. Defaults to "cdh_lava_core".

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None


def get_initial_script_dir():
    """
    Returns the directory path of the initial script.

    If '__file__' is defined in the global namespace, it returns the directory
    path of the script containing this function. Otherwise, it returns the
    current working directory.

    Returns:
        str: The directory path of the initial script.
    """
    if "__file__" in globals():
        script_directory = os.path.dirname(os.path.abspath(__file__))
    else:
        # If '__file__' is not defined, use the current working directory
        script_directory = os.getcwd()

    return script_directory


def install_requirements(requirements_dir):
    """
    Install the Python packages specified in the requirements file.

    Args:
        requirements_dir (str): The path to the directory containing the requirements file.

    Raises:
        subprocess.CalledProcessError: If the installation command exits with a non-zero status.

    Returns:
        None
    """

    requirements_path = os.path.join(requirements_dir, "requirements.txt")
    print(f"requirements_path:{requirements_path}")

    cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_path]
    try:
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode != 0:
                print(
                    f"Error: pip install command failed with exit code {proc.returncode}",
                    file=sys.stderr,
                )
                if stdout:
                    print(f"STDOUT:\n{stdout.decode('utf-8')}", file=sys.stderr)
                if stderr:
                    print(f"STDERR:\n{stderr.decode('utf-8')}", file=sys.stderr)
                    sys.exit(1)
            else:
                print(f"Installed requirements successfully from {requirements_path}")
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_library(running_local: bool, package_name: str, script_directory: str):
    """
    Set up the CDH LAVA Python library by adding the library path to sys.path and installing the package.

    Args:
        running_local (bool): Indicates whether the setup is being performed locally or on a remote server.
        package_name (str): The name of the package to install.

    Returns:
        None
    """

    print(f"script_directory:{script_directory}")
    # Change the current working directory to the script directory
    os.chdir(script_directory)

    if not is_package_installed("opentelemetry"):
        print("Package opentelemetry is not installed. Installing package...")

        requirements_dir = (
            os.path.dirname(os.path.abspath(__file__))
            if "__file__" in globals()
            else os.getcwd()
        )
        print(f"installing requirements.txt in requirements_dir:{requirements_dir}")
        install_requirements(requirements_dir)

    if not is_package_installed(package_name):
        print(f"Package {package_name} is not installed. Installing package...")
    else:
        print(f"Package {package_name} is already installed.")
        return

    initial_working_dir = os.path.join(os.getcwd())
    print(f"initial_working_dir:{initial_working_dir}")
    # Get Libary Path and add to sys.path
    path_parts = script_directory.split(os.sep)
    # Try to find the index of "cdh_lava_core"
    try:
        index = path_parts.index("cdh_lava_core")
        print(f"Index of 'cdh_lava_core': {index}")
        library_path = os.sep.join(path_parts[:index])
        sys.path.append(library_path)
    except ValueError:
        library_path =  os.getcwd() 
        print("'cdh_lava_core' not found in the path")
        

    try:
        if running_local is True:
            install_package_editable_client(library_path)
        else:
            destination_path = os.path.join(library_path, "requirements.txt")
            install_package_editable_server(destination_path)

        # Confirm that the package was installed
        if not is_package_installed(package_name):
            error_msg = f"Package {package_name} failed to install installed."
            raise ValueError(error_msg)

    except Exception as ex_pip_install:
        print(f"Error executing install: {ex_pip_install}")

    os.chdir(initial_working_dir)

    return


def install_package_editable_server(requirements_path):
    """
    Install a package in editable mode using pip.

    Args:
        requirements_path (str): The path to the requirements file.

    Returns:
        bool: True if the installation was successful, False otherwise.
    """
    try:
        if requirements_path:
            os.environ["CDH_REQUIREMENTS_PATH"] = os.path.abspath(requirements_path)

            try:
                process = subprocess.Popen(
                    ["pip", "install", "-r", os.environ["CDH_REQUIREMENTS_PATH"]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )

                # Print the output as it occurs
                for line in process.stdout:
                    print(line, end="")

                # Wait for the process to complete and capture the return code
                return_code = process.wait()

                # Check if the installation was successful
                if return_code == 0:
                    print("Requirements installation completed successfully.")
                else:
                    print(f"Error executing pip install. Return code: {return_code}")
                    for line in process.stderr:
                        print(line, end="")

            except Exception as ex_pip:
                print(f"Error executing pip install: {ex_pip}")
        else:
            print("CDH_REQUIREMENTS_PATH ENVIRONMENT variable is not set.")

        return True
    except subprocess.CalledProcessError as e:
        print("Failed to install package in editable mode:", e)


def install_package_editable_client(library_path):
    """
    Installs a package in editable mode using pip.

    Args:
        library_path (str): The path to the package's directory.

    Raises:
        subprocess.CalledProcessError: If the 'pip install -e .' command fails.

    """
    initial_path = os.getcwd()
    try:
        os.chdir(library_path)
        print(f"library_path: {library_path}")

        # Run 'pip install -e .' command
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("Package installed in editable mode successfully.")
        os.chdir(initial_path)

    except subprocess.CalledProcessError as e:
        os.chdir(initial_path)
        print(f"error: {e}")


def get_jobs_list(script_directory):
    """
    Retrieves the list of jobs from the bronze_sps_config_jobs.csv file.

    Returns:
    - job_names (list): A list of unique job names.
    """

    # Get Jobs List
    relative_path = "./config/bronze_sps_config_jobs.csv"
    jobs_csv_file_path = os.path.join(script_directory, relative_path)
    df_jobs = pd.read_csv(jobs_csv_file_path)
    df_jobs["job_name"] = df_jobs["job"]
    job_names = df_jobs["job_name"].unique()
    # Convert to absolute path for Spark code
    config_jobs_path = os.path.abspath(jobs_csv_file_path)
    print(f"absolute_path: {config_jobs_path}")
    return df_jobs, job_names, config_jobs_path


def secure_connect_spark_adls(spark, config):
    from cdh_lava_core.az_key_vault_service.az_key_vault import AzKeyVault

    client_secret = os.environ.get("AZURE_CLIENT_SECRET")
    tenant_id = config.get("az_sub_tenant_id")
    client_id = config.get("az_sub_client_id")
    vault_name = config.get("az_kv_key_vault_name")
    data_product_id = config.get("data_product_id")
    az_sub_client_secret_key = config.get("az_sub_client_secret_key")
    environment = config.get("environment")
    running_interactive = True

    from cdh_lava_core import constants

    obj_key_vault = AzKeyVault(
        tenant_id,
        client_id,
        client_secret,
        vault_name,
        running_interactive,
        data_product_id,
        environment,
        az_sub_client_secret_key
    )

    secret_scope = constants.get_secret_scope()
    # Application (Client) ID
    applicationId = dbutils.secrets.get(scope=secret_scope, key="cdh-adb-client-id")
    # Application (Client) Secret Key
    authenticationKey = dbutils.secrets.get(
        scope=secret_scope, key="cdh-adb-client-secret"
    )

    # Directory (Tenant) ID
    tenantId = dbutils.secrets.get(scope=secret_scope, key="cdh-adb-tenant-id")

    endpoint = "https://login.microsoftonline.com/" + tenantId + "/oauth2/token"

    # Connecting using Service Principal secrets and OAuth
    configs = {
        "fs.azure.account.auth.type": "OAuth",
        "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        "fs.azure.account.oauth2.client.id": client_id,
        "fs.azure.account.oauth2.client.secret": client_secret,
        "fs.azure.account.oauth2.client.endpoint": endpoint,
    }

    spark.conf.set("fs.azure.account.auth.type", "OAuth")
    spark.conf.set(
        "fs.azure.account.oauth.provider.type",
        "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    )
    spark.conf.set("fs.azure.account.oauth2.client.id", applicationId)
    spark.conf.set("fs.azure.account.oauth2.client.secret", authenticationKey)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint", endpoint)


def get_spark_connect(running_local, spark, data_product_id, environment):
    """
    Get the Spark session for running CDH LAVA Python code.

    Parameters:
    running_local (bool): Flag indicating whether the code is running locally or on Databricks.
    spark (pyspark.sql.SparkSession): The existing Spark session, if available.
    data_product_id (str): The ID of the data product.
    environment (str): The environment in which the code is running.

    Returns:
    pyspark.sql.SparkSession: The Spark session to be used for running CDH LAVA Python code.

    Raises:
    ValueError: If the Spark session is not defined or None.
    """

    if running_local:
        import getpass

        from databricks.connect import DatabricksSession
        from databricks.sdk.core import Config

        databricks_profile = f"{data_product_id}_{environment}"
        databricks_profile = databricks_profile.upper()

        user_name = os.environ.get("USER") or os.environ.get("USERNAME")
        if user_name is None:
            user_name = getpass.getuser()

        # Check if the username is 4 characters long and process it
        # if len(user_name) == 4:
        #     user_name = f"{user_name.lower()}@cdc.gov"
        # else:
        #    user_name = user_name.lower()
            

        if user_name is None:
            raise ValueError("USER or USERNAME environment variable is not set.")
        
        # os.environ["USER_ID"] = user_name
        config = Config(profile=databricks_profile)
        if spark is None:
            spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()

    if spark is None:
        raise ValueError("Spark session is not defined or None.")
    else:
        return spark


def setup_widgets(default_job_name, job_names, dbutils):
    """
    Sets up the widgets for selecting a job to run.

    Args:
        default_job_name (str): The default job name.
        job_names (list): A list of job names.
        dbutils: The dbutils object for interacting with widgets.

    Returns:
        str: The selected job name.

    Raises:
        Exception: If there is an error while setting up the widget.
    """

    try:
        # Try to get the current value of the widget
        job_name = dbutils.widgets.get("job_name")

        # If JOB_NAME is None or empty, set it to the default job name
        if not job_name:
            job_name = default_job_name

        return job_name

    except Exception as e:
        # If the widget does not exist, define it
        dbutils.widgets.dropdown(
            "job_name", "Select job to run", ["Select job to run"] + list(job_names)
        )
        job_name = default_job_name
        print(f"error: {e}")


def setup_config_core(
    running_local,
    obj_environment_metadata,
    obj_job_core,
    dbutils,
    data_product_id,
    environment,
):
    """
    Set up the configuration for the core components.

    Args:
        running_local (bool): Indicates whether the code is running locally.
        obj_environment_metadata: Object representing the environment metadata.
        obj_job_core: Object representing the core job.
        dbutils: Object representing the database utilities.
        environment: The environment to set up the configuration for.

    Returns:
        config: The configuration for the core components.
    """

    if running_local:
        dbutils_param = None
    else:
        if isinstance(dbutils, str):
            raise ValueError("dbutils is not an instance of DbUtils")

        dbutils_param = dbutils

    parameters = obj_job_core.get_standard_parameters(
        environment, dbutils_param, data_product_id
    )
    if parameters["data_product_id"] != data_product_id:
        print(
            "WARNING: data_product_id does not match virtual environment - consider changing virtual environment"
        )

    # Change virtual environment using workon command

    parameters["data_product_id"] = data_product_id
    parameters["data_product_root_id"] = data_product_id.split("_")[0]
    parameters["data_product_individual_id"] = data_product_id.replace(
        parameters["data_product_root_id"] + "_", ""
    )
    parameters["running_local"] = running_local
    parameters["environment"] = environment
    print(f"parameters: {str(parameters)}")

    config = obj_environment_metadata.get_configuration_common(
        parameters, dbutils, data_product_id, environment
    )

    return config


def setup_config(
    running_local,
    obj_environment_metadata,
    obj_job_metadata,
    dbutils,
    spark,
    config_jobs_path,
    environment,
    data_product_id,
):
    """
    Set up the configuration for the CDH LAVA Python project.

    Args:
        running_local (bool): Indicates whether the code is running locally or not.
        package_name (str): The name of the package.
        default_job_name (str): The default name of the job.
        obj_environment_metadata (object): An object containing environment metadata.
        obj_job_metadata (object): An object containing job metadata.
        environment (str, optional): The environment to use. Defaults to "dev".

    Returns:
        dict: The configuration for the CDH LAVA Python project.
    """
    if running_local:
        dbutils_param = None
    else:
        dbutils_param = dbutils

    parameters = obj_job_metadata.get_standard_parameters(
        environment,
        dbutils_param,
        spark,
        config_jobs_path,
        data_product_id,
    )

    parameters["data_product_id"] = data_product_id
    parameters["data_product_root_id"] = data_product_id.split("_")[0]
    parameters["data_product_individual_id"] = data_product_id.replace(
        parameters["data_product_root_id"] + "_", ""
    )
    parameters["running_local"] = running_local
    parameters["environment"] = environment.lower().strip()
    print(f"parameters: {str(parameters)}")

    config = obj_environment_metadata.get_configuration_common(
        parameters, dbutils, data_product_id, environment
    )
    if config.get("config_jobs_path") is None or config.get("config_jobs_path") == "":
        config["config_jobs_path"] = config_jobs_path

    # spark = secure_connect_spark_adls(spark, config)
    return config


def setup_core(
    running_local,
    initial_script_directory,
    dbutils,
    spark,
    data_product_id,
    environment,
    package_name="cdh_lava_core",
):
    """
    Set up the core components for CDH LAVA Python.

    Args:
        running_local (bool): Flag indicating if the code is running locally.
        initial_script_directory (str): The initial script directory.
        dbutils: The dbutils object.
        spark: The SparkSession object.
        data_product_id (str): The data product ID.
        environment (str): The environment.
        package_name (str, optional): The name of the package. Defaults to "cdh_lava_core".

    Returns:
        tuple: A tuple containing the SparkSession object, EnvironmentMetaData object, JobCore object, and config object.
    """

    print("initial_script_directory:", initial_script_directory)
    setup_library(running_local, package_name, initial_script_directory)

    from cdh_lava_core.cdc_log_service.environment_logging import (
        LoggerSingleton,
    )

    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
    ).initialize_logging_and_tracing()

    logger.info(f"tracer: {tracer}")

    with tracer.start_as_current_span("setup_core"):
        try:
            spark = get_spark_connect(
                running_local, spark, data_product_id, environment
            )
            import cdh_lava_core.cdc_metadata_service.environment_metadata as cdc_environment_metadata
            import cdh_lava_core.cdc_tech_environment_service.job_core as cdc_job_core

            obj_environment_metadata = cdc_environment_metadata.EnvironmentMetaData()
            obj_job_core = cdc_job_core.JobCore()

            config = setup_config_core(
                running_local,
                obj_environment_metadata,
                obj_job_core,
                dbutils,
                data_product_id,
                environment,
            )

            return (
                spark,
                obj_environment_metadata,
                obj_job_core,
                config,
            )

        except Exception as ex:
            error_msg = "Error: %s", ex
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                SERVICE_NAME, NAMESPACE_NAME, data_product_id, environment
            ).error_with_exception(error_msg, exc_info)
            raise


def extract_catalog_name(db_name):
    """
    Extracts the catalog name from the given database name.

    Args:
        db_name (str): The name of the database.

    Returns:
        str: The catalog name extracted from the database name.
    """
    return db_name.split(".")[0] if "." in db_name else None


def setup_job(
    running_local,
    package_name,
    default_job_name,
    initial_script_directory,
    dbutils,
    spark,
    environment,
    data_product_id,
):
    """
    Set up the job by performing various initialization tasks.

    Args:
        running_local (bool): Indicates whether the job is running locally or not.
        package_name (str): The name of the package.
        default_job_name (str): The default name of the job.
        initial_script_directory (str): The initial script directory.
        dbutils: The dbutils object.
        spark: The spark object.
        environment: The environment configuration.

    Returns:
        tuple: A tuple containing the following elements:
            - spark: The spark object.
            - jobs_list: A list of jobs.
            - job_names: A list of job names.
            - obj_environment_metadata: An instance of the EnvironmentMetaData class.
            - obj_job_metadata: An instance of the JobMetaData class.
            - config: The configuration object.
            - job_name: The name of the job.
    """

    print("initial_script_directory:", initial_script_directory)
    setup_library(running_local, package_name, initial_script_directory)

    from cdh_lava_core.cdc_log_service.environment_logging import (
        LoggerSingleton,
    )

    tracer, logger = LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
    ).initialize_logging_and_tracing()

    logger.info(f"tracer: {tracer}")

    with tracer.start_as_current_span("setup_job"):
        try:
            spark = get_spark_connect(
                running_local, spark, data_product_id, environment
            )
            jobs_list, job_names, config_jobs_path = get_jobs_list(
                initial_script_directory
            )
            if not running_local:
                job_name = setup_widgets(default_job_name, job_names, dbutils)
            else:
                job_name = default_job_name

            import cdh_lava_core.cdc_metadata_service.environment_metadata as cdc_environment_metadata
            import cdh_lava_core.cdc_metadata_service.job_metadata as cdc_job_metadata

            obj_environment_metadata = cdc_environment_metadata.EnvironmentMetaData()
            obj_job_metadata = cdc_job_metadata.JobMetaData()

            config = setup_config(
                running_local,
                obj_environment_metadata,
                obj_job_metadata,
                dbutils,
                spark,
                config_jobs_path,
                environment,
                data_product_id,
            )

            cdh_database_name = config.get("cdh_database_name")
            catalog_name = extract_catalog_name(cdh_database_name)
            print(f"catalog_name: {catalog_name}")

            # can not set at run time
            # if catalog_name is not None:
            #    spark.conf.set("spark.sql.catalogImplementation", catalog_name)

            return (
                spark,
                jobs_list,
                job_names,
                obj_environment_metadata,
                obj_job_metadata,
                config,
                job_name,
            )

        except Exception as ex:
            error_msg = "Error: %s", ex
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).error_with_exception(error_msg, exc_info)
            raise


def get_wonder_script_dir():
    """
    Returns the path to the wonder_metadata directory.

    The path is determined based on the location of the current script file.
    If the script file is not available, the current working directory is used.

    Returns:
        str: The path to the wonder_metadata directory.
    """
    initial_script_dir = (
        os.path.dirname(os.path.abspath(__file__))
        if "__file__" in globals()
        else os.getcwd()
    )
    wonder_metadata_path = os.path.join(initial_script_dir, "wonder", "wonder_metadata")
    return wonder_metadata_path
