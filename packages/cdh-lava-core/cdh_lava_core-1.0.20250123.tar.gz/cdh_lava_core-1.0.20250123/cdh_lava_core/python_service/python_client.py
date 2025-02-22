import importlib
import inspect
import os
import sys
import venv
import subprocess

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class PythonClient:
    """
    A class that provides various utility methods for working with Python modules and environments.
    """

    @staticmethod
    def list_classes(module_name):
        """
        Lists all classes in a given module.

        :param module_name: Name of the module to inspect.
        :return: List of class names.
        """
        try:
            module = importlib.import_module(module_name)
            classes = [
                name for name, obj in inspect.getmembers(module) if inspect.isclass(obj)
            ]
            return classes
        except ImportError:
            return f"Module '{module_name}' not found."

    @staticmethod
    def list_user_defined_classes(module_name):
        """
        Lists user-defined classes in a given module, ignoring special attributes.

        :param module_name: Name of the module to inspect.
        :return: List of user-defined class names.
        """
        try:
            module = importlib.import_module(module_name)
            class_list = []
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and not name.startswith("_"):
                    class_list.append(name)
            return class_list
        except ImportError:
            return f"Module '{module_name}' not found."

    @classmethod
    def create_virtual_environment(
        cls, virtual_environment_name, data_product_id, environment
    ):
        """
        Creates a virtual environment with the given name.

        :param virtual_environment_name: Name of the virtual environment to create.
        :return: A message indicating the success of the operation.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("create_virtual_environment"):
            home_dir = os.path.expanduser("~")  # Get the user's home directory
            virtual_environment_name = virtual_environment_name.upper()
            venv_root_dir = os.path.join(home_dir, ".virtualenv")
            venv_dir = os.path.join(
                home_dir, ".virtualenv", virtual_environment_name
            )  # Path to the virtual environment directory

            try:
                # Change directory to the specified venv_root_dir
                os.chdir(venv_root_dir)
                logger.info(f"Changed the current directory:{venv_root_dir}")

                logger.info("Create the virtual environment")
                venv.create(venv_dir, with_pip=True)
                logger.info(
                    "Activate the virtual environment. This is platform dependent"
                )

                if sys.platform == "win32":
                    # Windows
                    activate_script = os.path.join(venv_dir, "Scripts", "activate")
                else:
                    # Unix-like
                    activate_script = os.path.join(venv_dir, "bin", "activate")

                # The activation of a virtualenv is a shell-specific command,
                # which cannot be done from a Python script.
                # For the purposes of subprocesses within this script,
                # the path to the virtualenv Python interpreter can be used
                # directly to run subsequent Python scripts.
                # Example: /path/to/venv/bin/python script.py
                # To use the virtualenv outside of this script, one must
                # run 'source /path/to/venv/bin/activate' in the shell.
                logger.info("Virtual environment created successfully")
                return f"Virtual environment created successfully. Activate it with 'source {activate_script}'"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    @staticmethod
    def execute_python_file(path_to_execute, data_product_id, environment):
        # Retrieve the current Python interpreter path (from the virtual environment)
        current_python = sys.executable

        # Initialize logging and tracing
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        try:
            # Run the Python file using the Python interpreter from the current virtual environment
            result = subprocess.run(
                [current_python, path_to_execute],  # Use the current Python interpreter
                capture_output=True,                # Capture stdout and stderr
                text=True,                          # Return output as string (text)
                check=True                          # Raise exception on non-zero exit code
            )

            # If the file runs successfully
            logger.info("Execution output:")
            logger.info(result.stdout)

            return result

        except subprocess.CalledProcessError as e:
            # Capture any errors if the file execution fails
            logger.error(f"Error occurred while executing {path_to_execute}:")
            raise ValueError(e.stderr)
        except Exception as ex:
            error_msg = "Error: %s", ex
            exc_info = sys.exc_info()
            LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
            ).error_with_exception(error_msg, exc_info)
            raise