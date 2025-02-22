import pandas as pd
import requests
import zipfile
import io
import os
import sys
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
class GeoZipDownloader:
    @staticmethod
    def download_zip_data(url: str, output_file: str):
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(output_file)
        else:
            raise Exception(f"Failed to download file from {url}")

    @staticmethod
    def process_zip_data(input_file: str) -> pd.DataFrame:
        df = pd.read_csv(input_file, sep='\t', header=None, names=[
            'country_code', 'postal_code', 'place_name', 'admin_name1',
            'admin_code1', 'admin_name2', 'admin_code2', 'admin_name3',
            'admin_code3', 'latitude', 'longitude', 'accuracy'
        ])
        
        df['zip3'] = df['postal_code'].astype(str).str[:3]
        zip3_coords = df.groupby('zip3')[['latitude', 'longitude']].mean().reset_index()
        return zip3_coords

    @staticmethod
    def save_to_csv(df: pd.DataFrame, output_file: str):
        df.to_csv(output_file, index=False)

# Example usage
if __name__ == "__main__":
    url = 'http://download.geonames.org/export/zip/US.zip'
    output_dir = 'data'
    input_file = f'{output_dir}/US.txt'
    output_file = 'zip3_coordinates.csv'

    # Download the data
    ZipCodeProcessor.download_zip_data(url, output_dir)
    
    # Process the data
    zip3_df = ZipCodeProcessor.process_zip_data(input_file)
    
    # Save the data to CSV
    ZipCodeProcessor.save_to_csv(zip3_df, output_file)
    
    print(f"3-digit ZIP code coordinates have been saved to {output_file}")
