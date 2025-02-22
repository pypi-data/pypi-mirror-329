import os
import uuid
from smbprotocol.connection import Connection, Dialects
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open, CreateOptions, FilePipePrinterAccessMask, ImpersonationLevel, ShareAccess
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import sys

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class SMBStorageFileCore:
    @staticmethod
    def setup_smb_connection(server, username, password, domain):
        connection = Connection(uuid.uuid4(), server, 445)
        connection.connect(Dialects.SMB_3_1_1)
        session = Session(connection, username, password, domain)
        session.connect()
        return session

    @staticmethod
    def copy_file(source_path, destination_path, session, share_name, data_product_id, environment):
        """
        Copy a file from the source path to the destination path using the SMB session.

        Args:
            source_path (str): The path of the source file.
            destination_path (str): The path where the file will be copied to.
            session (Session): The SMB session object.
            share_name (str): The name of the SMB share.
            data_product_id (str): The ID of the data product.
            environment (str): The environment name.

        Raises:
            Exception: If an error occurs during the file copy process.

        Returns:
            None
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("copy_file_to_smb"):
            try:

                tree_connect = TreeConnect(session, r"\\{}\{}".format(session.connection.server_name, share_name))
                tree_connect.connect()
                
                # Open the source file
                source_file = Open(tree_connect, source_path)
                source_file.create(ImpersonationLevel.Impersonation, FilePipePrinterAccessMask.GENERIC_READ, ShareAccess.FILE_SHARE_READ)
                file_data = source_file.read(0, source_file.end_of_file)

                # Create and write to the destination file
                destination_file = Open(tree_connect, destination_path)
                destination_file.create(ImpersonationLevel.Impersonation, FilePipePrinterAccessMask.GENERIC_WRITE, ShareAccess.FILE_SHARE_READ, CreateOptions.FILE_NON_DIRECTORY_FILE, None)
                destination_file.write(0, file_data)

                # Close files
                source_file.close()
                destination_file.close()
                logger.info("File copied successfully!")
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise



    @classmethod
    def list_directory(cls, directory_path, session, share_name, data_product_id, environment):
        """
        List the files in a directory using the SMB session.

        Args:
            directory_path (str): The path of the directory to list.
            session (Session): The SMB session object.
            share_name (str): The name of the SMB share.
            data_product_id (str): The ID of the data product.
            environment (str): The environment name.

        Raises:
            Exception: If an error occurs while listing the directory.

        Returns:
            None
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        tree_connect = TreeConnect(session, r"\\{}\{}".format(session.connection.server_name, share_name))
        tree_connect.connect()

        with tracer.start_as_current_span("list_directory_smb"):
            try:
                directory = Open(tree_connect, directory_path)
                directory.create(ImpersonationLevel.Impersonation, FilePipePrinterAccessMask.FILE_LIST_DIRECTORY, ShareAccess.FILE_SHARE_READ, CreateOptions.FILE_DIRECTORY_FILE)
                files = directory.query_directory("*")
                logger.info("Files in directory:")
                for file_info in files:
                    logger.info(file_info.file_name)
                directory.close()
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

