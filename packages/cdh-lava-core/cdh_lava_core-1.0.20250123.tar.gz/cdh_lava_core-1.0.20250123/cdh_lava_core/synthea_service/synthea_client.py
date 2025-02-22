import subprocess
import sys
import os
import shutil  # Import shutil for high-level file operations like removing directories
import pandas as pd
 
from cdh_lava_core.github_service.github_repo import GitHubRepo

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton


class SyntheaClient:

    @staticmethod
    def combine_csv_files(root_directory, target_filenames, data_product_id, environment):
        """
        Combines multiple CSV files into a single file.

        Args:
            root_directory (str): The root directory where the CSV files are located.
            target_filenames (list): A list of target CSV filenames to be combined.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the data is being processed.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("combine_csv_files"):
            try:
                # Ensure all filenames have the '.csv' extension
                target_filenames = [filename if filename.endswith('.csv') else filename + '.csv' for filename in target_filenames]

                # Create the directory for combined CSV files
                combined_dir = os.path.join(root_directory, '_combined')
                os.makedirs(combined_dir, exist_ok=True)

                # Walk through the directory
                for subdir, dirs, files in os.walk(root_directory):
                    # Skip the root directory
                    if subdir == root_directory:
                        continue
                    
                    # Construct the path to the 'csv' subfolder
                    csv_subfolder = os.path.join(subdir, 'csv')
                    # Check if the csv subfolder exists
                    if os.path.exists(csv_subfolder):
                        for filename in target_filenames:
                            # Initialize an empty DataFrame for each target file
                            combined_df = pd.DataFrame()
                            for file in os.listdir(csv_subfolder):
                                if file == filename:
                                    file_path = os.path.join(csv_subfolder, file)
                                    # Append to the DataFrame
                                    df = pd.read_csv(file_path)
                                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                            
                            # Save the combined dataframe to the new directory after processing each file
                            if not combined_df.empty:
                                output_file_path = os.path.join(combined_dir, filename)
                                combined_df.to_csv(output_file_path, index=False)
                                logger.info(f"Combined file written: {output_file_path}")

                        
                    return "Successfully combined Synthea files."
                                    
            except FileNotFoundError as e:
                # FileNotFoundError is raised when the command is not found
                logger.error("Command not found: %s", e.filename)
                logger.error("Full error: %s", e)
                logger.error("Current PATH: %s", os.environ.get("PATH"))
            except Exception as e:
                # Generic exception handling for any other exceptions
                logger.error("An error occurred: %s", e)


    @staticmethod
    def log_directory_contents(directory, data_product_id, environment):
        """
        Log the contents of a directory.

        Args:
            directory (str): The path to the directory.
            data_product_id (str): The ID of the data product.
            environment (str): The environment.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("log_directory_contents"):
            try:
                # List all files and directories in the given directory
                contents = os.listdir(directory)
                logger.info(f"Contents of {directory}:")
                for item in contents:
                    logger.info(item)
            except Exception as e:
                logger.error(f"Error reading directory {directory}: {e}")

    @staticmethod
    def run_synthea(module_path, us_population_size, state_population_sizes, output_directory, data_product_id, environment):
        """
        Run Synthea with the specified module.

        Args:
            module_path (str): The path to the Synthea module JSON file.
            us_population_size (int): The population size for generating synthetic patients.
            state_population_sizes (dict): A dictionary mapping state names to their population sizes in millions.
            output_directory (str): The directory where the output files will be saved.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the service is running.

        Returns:
            None

        Example:
            run_synthea(
                module_path="/home/developer/projects/cdh-lava-demo/cdh_hls_readmission/synthea/rsv_geriatrics.json",
                us_population_size=20000,
                state_population_sizes={
                    "Alabama": 1.48,
                    "Alaska": 0.23,
                    # add other states as necessary
                }
                output_directory="/home/developer/projects/synthea/data",
                location="United States",
                data_product_id="hls_readmission",
                environment="dev",

            )
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("run_synthea"):
            try:
                module_name = os.path.basename(module_path).replace('.json', '')
                synth_out = f"{output_directory}/{module_name}"
                
                logger.info(f"Module Path: {module_path}")
                logger.info(f"Output Directory: {synth_out}")
                
                # Ensure the output directory exists
                os.makedirs(synth_out, exist_ok=True)
                
                # Set JAVA_HOME environment variable after checking its existence
                java_home = os.environ.get("JAVA_HOME", "/usr/lib/jvm/java-11-openjdk-amd64")
                logger.info(f"JAVA_HOME is set to: {java_home}")

                if not os.path.exists(java_home):
                    logger.error(f"JAVA_HOME directory does not exist: {java_home}")
                    raise FileNotFoundError(f"JAVA_HOME directory does not exist: {java_home}")
                
                # Define the directory where Synthea will be cloned and built
                base_dir = os.path.expanduser("~/developer")
                projects_dir = os.path.join(base_dir, "projects")
                synthea_dir = os.path.join(projects_dir, "synthea")
                
                # Change to the Synthea directory
                os.chdir(synthea_dir)
            
                for state, percentage in state_population_sizes.items():
                    # Calculate population size for this state
                    state_population_size = int(us_population_size * (percentage / 100))
                    state_output_dir = os.path.join(synth_out, state).lower()
                    
                    logger.info(f"Running Synthea for {state} with population size {state_population_size}")
                    
                    # Ensure the state output directory exists
                    if not os.path.exists(state_output_dir):
                        os.makedirs(state_output_dir)
                        logger.info(f"Directory created: {state_output_dir}")
                    else:
                        shutil.rmtree(state_output_dir)
                        os.makedirs(state_output_dir)
                        logger.info(f"Directory re-created: {state_output_dir}")
                    
                    # Setup environment variables for the subprocess
                    env = os.environ.copy()
                    env["GRADLE_OPTS"] = "-Xmx4g"
                    
                    result = subprocess.run(
                        ["./run_synthea", state, "-p", str(state_population_size), '--exporter.baseDirectory', state_output_dir, '--exporter.fhir.export', 'false', '--exporter.csv.export', 'true', '--exporter.csv.folder_per_run', 'false', '--generate.log_patients.detail', 'none', '--exporter.clinical_note.export', 'false', '--m', module_path],
                        check=True,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )              

                    logger.info(f"Standard Output: {result.stdout}")
                    if result.stderr:
                        logger.warning(f"Error for {state}: {result.stderr}")

                    if result.returncode != 0:
                        raise ValueError("Error running Synthea with the specified module.")

                return "Successfully ran Synthea."

            except subprocess.CalledProcessError as ex:
                logger.error(f"Gradle build failed with return code {ex.returncode}")
                logger.error(f"stdout: {ex.stdout}")
                logger.error(f"stderr: {ex.stderr}")
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            except FileNotFoundError as e:
                # FileNotFoundError is raised when the command is not found
                logger.error("Command not found: %s", e.filename)
                logger.error("Full error: %s", e)
                logger.error("Current PATH: %s", os.environ.get("PATH"))
            except Exception as e:
                # Generic exception handling for any other exceptions
                logger.error("An error occurred: %s", e)
                 
    @classmethod
    def setup_synthea(cls, data_product_id, environment):
        """
        Set up the Synthea environment by cloning the Synthea repository, building it using Gradle,
        and generating synthetic patients.

        Args:
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the setup is being performed.

        Returns:
            str: A success message indicating that Synthea has been set up successfully.

        Raises:
            subprocess.CalledProcessError: If the Gradle build fails.
            FileNotFoundError: If a command is not found.
            Exception: For any other generic exceptions.
        """
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("setup_synthea"):
            try:
                # Define the directory where Synthea will be cloned and built
                base_dir = os.path.expanduser("~/developer")
                projects_dir = os.path.join(base_dir, "projects")
                synthea_dir = os.path.join(projects_dir, "synthea")

                # Check if the directory exists and delete it if it does
                if os.path.exists(synthea_dir):
                    logger.info("Synthea directory exists. Deleting and re-cloning...")
                    shutil.rmtree(synthea_dir)

                # Recreate the directory
                os.makedirs(synthea_dir, exist_ok=True)
                logger.info("Directory created: " + synthea_dir)

                # Clone the Synthea repository if not already cloned
                if not os.listdir(synthea_dir):  # Check if directory is empty
                    logger.info("Cloning Synthea repository...")
                    obj_repo = GitHubRepo()
                    result = obj_repo.clone_repo(
                        "synthetichealth",
                        "synthea",
                        "master",
                        projects_dir,
                        data_product_id,
                        environment,
                    )
                    logger.info("clone: " + result)
                else:
                    logger.info("Repository already cloned.")

                # Change to the Synthea directory
                os.chdir(synthea_dir)

                cls.log_directory_contents(synthea_dir, data_product_id, environment)

                # Setup environment variables for the subprocess
                env = os.environ.copy()
                env["GRADLE_OPTS"] = "-Xmx4g"
                
                # Set JAVA_HOME environment variable after checking its existence
                if "JAVA_HOME" not in os.environ or os.environ["JAVA_HOME"] == "":
                    # Set JAVA_HOME if it's not set
                    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

                java_home = os.environ["JAVA_HOME"] 
                # Now you can use JAVA_HOME as needed
                logger.info(f"JAVA_HOME is set to: {java_home}")

                if not os.path.exists(java_home):
                    logger.error(f"JAVA_HOME directory does not exist: {java_home}")
                    raise FileNotFoundError(
                        f"JAVA_HOME directory does not exist: {java_home}"
                    )

                # Build Synthea using Gradle with the specified options
                result = subprocess.run(
                    [
                        "./gradlew",
                        "build",
                        "check",
                        "-x",
                        "test",
                        "-Dorg.gradle.java.home=" + java_home,
                    ],
                    check=True,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                # Generate a few synthetic patients (example command)
                subprocess.run(["./run_synthea", "-p", "10"], check=True)

                return "Successfully setup Synthea."
            except subprocess.CalledProcessError as ex:
                logger.error(f"Gradle build failed with return code {ex.returncode}")
                logger.error(f"stdout: {ex.stdout}")
                logger.error(f"stderr: {ex.stderr}")
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            except FileNotFoundError as e:
                # FileNotFoundError is raised when the command is not found
                logger.error("Command not found: %s", e.filename)
                logger.error("Full error: %s", e)
                logger.error("Current PATH: %s", os.environ.get("PATH"))
            except Exception as e:
                # Generic exception handling for any other exceptions
                logger.error("An error occurred: %s", e)
