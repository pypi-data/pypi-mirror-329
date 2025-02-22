import pandas as pd
import os
import sys
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class GeoZipMerger:
    """
    A class to handle the loading, processing, and saving of geographic data related to ZIP codes.
    """

    @staticmethod
    def load_postal_code_data(file_path: str, data_product_id, environment) -> pd.DataFrame:
        """
        Load the Geonames postal code data from a file into a pandas DataFrame.

        Args:
            file_path (str): The path to the file containing the postal code data.

        Returns:
            pd.DataFrame: A DataFrame containing the postal code data.

        Raises:
            Exception: If there is an error while reading the file.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("load_postal_code_data"):
            try:                            
                dtype = {
                    'country_code': str,
                    'postal_code': str,
                    'place_name': str,
                    'admin_name1': str,
                    'admin_code1': str,
                    'admin_name2': str,
                    'admin_code2': str,
                    'admin_name3': str,
                    'admin_code3': str,
                    'latitude': float,
                    'longitude': float,
                    'accuracy': float  
                }
                df = pd.read_csv(file_path, sep='\t', header=None, names=[
                    'country_code', 'postal_code', 'place_name', 'admin_name1',
                    'admin_code1', 'admin_name2', 'admin_code2', 'admin_name3',
                    'admin_code3', 'latitude', 'longitude', 'accuracy'
                ], dtype=dtype)
                return df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def extract_three_digit_zip(df: pd.DataFrame, data_product_id, environment) -> pd.DataFrame:
        """
        Extract 3-digit ZIP codes and compute the average latitude and longitude for each.

        Args:
            df (pd.DataFrame): A DataFrame containing the postal code data.

        Returns:
            pd.DataFrame: A DataFrame with 3-digit ZIP codes and their corresponding average coordinates.

        Raises:
            Exception: If there is an error while processing the data.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("extract_three_digit_zip"):
            try: 
                df['zip3'] = df['postal_code'].astype(str).str[:3]
                zip3_coords = df.groupby('zip3')[['latitude', 'longitude']].mean().reset_index()
                return zip3_coords
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def save_to_csv(df: pd.DataFrame, output_file: str, data_product_id, environment):
        """
        Save the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_file (str): The path to the output CSV file.

        Raises:
            Exception: If there is an error while saving the file.
        """
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("save_to_csv"):
            try: 
                df.to_csv(output_file, index=False)
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
 