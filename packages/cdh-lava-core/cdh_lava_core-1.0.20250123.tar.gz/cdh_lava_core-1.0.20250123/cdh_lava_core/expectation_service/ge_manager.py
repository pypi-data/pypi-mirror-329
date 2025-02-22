import sys
import os
import subprocess
import jupytext
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import shutil
import pkg_resources

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class GreatExpectationsManager:

    @staticmethod
    def run_command(command, directory, data_product_id, environment, capture_output=True):
        """Helper method to execute shell commands."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()
            
                
        if directory:
                logger.info(f"Changing working directory to: {directory}")
                os.chdir(directory)

        with tracer.start_as_current_span("run_command"):
            try:
                # Check if the command is available in the PATH
                command_name = command.split()[0]
                command_path = shutil.which(command_name)

                if not command_path:
                    logger.info(f"Command '{command_name}' not found in PATH. Trying to find it with pip.")

                    # Attempt to locate the package's installation path using pkg_resources
                    try:
                        package_location = pkg_resources.get_distribution(command_name).location

                        # Check standard locations first
                        command_full_path = os.path.join(
                            package_location, 
                            "Scripts" if os.name == 'nt' else "bin", 
                            command_name
                        )
                        
                        if not os.path.exists():
                            # If not found, search recursively in the package location
                            logger.info(f"'{command_name}' not found in standard directories. Searching in '{package_location}'.")
                            for root, dirs, files in os.walk(package_location):
                                if command_name in files:
                                    command_full_path = os.path.join(root, command_name)
                                    logger.info(f"Found '{command_name}' in '{root}'.")
                                    break
                            else:
                                raise FileNotFoundError(f"Executable '{command_name}' not found in '{package_location}' or its subdirectories.")

                        # Add the directory containing the command to the PATH
                        logger.info(f"Adding '{os.path.dirname(command_full_path)}' to PATH.")
                        os.environ["PATH"] += os.pathsep + os.path.dirname(command_full_path)
                        
                    except Exception as e:
                        error_msg = f"Unable to locate or add '{command_name}' to PATH: {e}"
                        exc_info = sys.exc_info()
                        LoggerSingleton.instance(
                            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                        ).error_with_exception(error_msg, exc_info)
                        raise


                # Don't capture output for interactive notebook sessions
                if not capture_output:
                    result = subprocess.run(command, shell=True, check=True)
                else:
                    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                    logger.info(result.stdout)
                return result
            except subprocess.CalledProcessError as ex:
                error_msg = f"Command failed with exit code {ex.returncode}: {ex.output}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            except Exception as ex:
                error_msg = f"Error: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
    @classmethod
    def create_suite(cls, suite_name, directory, data_product_id, environment):
        """Creates a new expectation suite and launches interactive notebook."""
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("create_suite"):
            try:
                # Change to the specified directory if provided
                if directory:
                    logger.info(f"Changing working directory to: {directory}")
                    os.chdir(directory)
                    
                # First create the suite
                command = f"great_expectations suite new {suite_name} --interactive"
                logger.info(f"Running command: {command}")
                
                # Run without capturing output to allow notebook interaction
                cls.run_command(command, directory, data_product_id, environment, capture_output=False)
                
                # Check if notebook was created
                expected_notebook = f"great_expectations/notebooks/edit_{suite_name}.ipynb"
                if not os.path.exists(expected_notebook):
                    raise FileNotFoundError(f"Expected notebook {expected_notebook} was not created")
                
                logger.info(f"Successfully created suite and notebook: {expected_notebook}")
            except Exception as ex:
                error_msg = f"Error creating suite: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
    @classmethod
    def edit_suite(cls, suite_name, directory, data_product_id, environment):
        """Edits an existing expectation suite in a Jupyter notebook."""
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("edit_suite"):
            try:
                # Change to the specified directory if provided
                if directory:
                    logger.info(f"Changing working directory to: {directory}")
                    os.chdir(directory)
                    
                # Use --jupyter flag to explicitly request notebook creation
                command = f"great_expectations suite edit {suite_name} --jupyter"
                logger.info(f"Running command: {command}")
                
                # Run without capturing output to allow notebook interaction
                cls.run_command(command, data_product_id, environment, capture_output=False)
                
                # Verify notebook exists
                expected_notebook = f"great_expectations/notebooks/edit_{suite_name}.ipynb"
                if not os.path.exists(expected_notebook):
                    raise FileNotFoundError(f"Expected notebook {expected_notebook} was not created")
                    
                logger.info(f"Successfully opened notebook: {expected_notebook}")
            except Exception as ex:
                error_msg = f"Error editing suite: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def check_great_expectations(cls, directory, data_product_id, environment):
        """Checks if great_expectations is installed and accessible."""
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("check_great_expectations"):
            try:
                command = "great_expectations --version"
                logger.info(f"Running command: {command}")
                result = cls.run_command(command, directory, data_product_id, environment)
                logger.info(f"Great Expectations version: {result.stdout.strip()}")
            except Exception as ex:
                error_msg = f"Great Expectations is not installed or not accessible: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

# Example usage:
# GreatExpectationsManager.create_suite("my_new_suite", "directory", "data_product_id", "dev")
# GreatExpectationsManager.edit_suite("my_new_suite", "directory", "data_product_id", "dev")
# GreatExpectationsManager.check_great_expectations("data_product_id", "dev")