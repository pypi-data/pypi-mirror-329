from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from typing import List, Optional
import logging
import requests
import time
import pandas as pd
import os
import sys
from math import ceil
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.youtube_service.youtube_downloader import YouTubeDownloader
import shutil

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

# AI Prompts
# AI Prompts
# summarize in smart brevity style in markdown format and include title. provide result in mardown
# create a mermaid mindmap for this article in markdown format and include title provide result in markdown
    
class DataBootCampScraper:

    @staticmethod
    def setup_driver(data_product_id, environment):
        """
        Sets up the Selenium WebDriver with headless mode.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()
        
        with tracer.start_as_current_span("setup_driver"):
            try:

                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = "/home/developer/chrome/opt/google/chrome/google-chrome"  # Update this path
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--window-size=1920,1080")  # Set window size
                chrome_options.add_argument("--disable-extensions")  # Disable extensions

                chromedriver_path = os.path.expanduser("~/chrome/chromedriver")  # Adjust based on your Makefile CHROMEDRIVER_DIR
                service = Service(executable_path=chromedriver_path)  # Replace with the path to chromedriver
                driver = webdriver.Chrome(service=service, options=chrome_options)
                return driver

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

 
  

    @staticmethod
    def extend_filename(original_filename: str) -> str:
        """
        Static method to convert original filename to extended filename.
        
        Args:
            original_filename (str): The original filename in format like 'filename.mp4'
            
        Returns:
            str: Extended filename in format like 'filename_extended.mp4'
        """
        
        filename = original_filename.lower()
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
    
        # Replace spaces with underscores
        filename = filename.replace('-', '_')
            
        # Remove special characters 
        # Keep only alphanumeric, underscore, and hyphen
        import re
        filename = re.sub(r'[^a-z0-9_-]', '', filename)
        
        # Remove multiple consecutive underscores
        filename = re.sub(r'_+', '_', filename)
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        # Add .mp4 extension
        filename = f"{filename}.mp4"
        
        return filename
    
    
    @classmethod
    def enrich_file_names(cls, input_file: str, output_file: str, data_product_id, environment):
        """
        Process CSV file to add extended filenames column
        
        Args:
            input_file (str): Path to input CSV file
            output_file (str): Path to output CSV file
        """
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Add extended filename column
        df['extended_file_name'] = df['Title'].apply(cls.extend_filename)

        # Convert column names to lowercase
        df.columns = df.columns.str.lower()
                
        # Save to new CSV file
        df.to_csv(output_file, index=False)

    @classmethod
    def download_youtube_videos(cls, input_file: str, output_dir: str, data_product_id, environment):
        # Read the CSV file
        df = pd.read_csv(input_file)
        successful_downloads = []
        failed_downloads = []
        
        # Loop through each row
        for index, row in df.iterrows():
            try:
                # Get YouTube link from video_url column
                link = row.get('video url', '')
                            
                if not pd.isna(link) and link:  # Check if link exists and is not empty
                    # Download the YouTube video
                    filename = YouTubeDownloader.download_youtube(
                        link,
                        data_product_id,
                        environment,
                        output_dir=output_dir
                    )

                    if filename:
                        # Define the new file name (use the full path)
                        new_file_name = os.path.join(output_dir, row['extended_file_name'])
                        
                        # Rename the file if the download was successful
                        try:
                            original_file_path = os.path.join(output_dir, filename)
                            shutil.move(original_file_path, new_file_name)  # Use shutil.move to rename
                            successful_downloads.append({
                                'original_file': row['extended_file_name'],
                                'downloaded_file': new_file_name,
                                'url': link
                            })
                        except Exception as e:
                            failed_downloads.append({
                                'original_file': row['extended_file_name'],
                                'url': link,
                                'error': f"Renaming failed: {str(e)}"
                            })
                    else:
                        failed_downloads.append({
                            'original_file': row['extended_file_name'],
                            'url': link,
                            'error': 'Download failed'
                        })
                else:
                    print(f"Skipping row {index + 1}: No video URL found")
                    
            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                failed_downloads.append({
                    'original_file': row['extended_file_name'],
                    'url': link if 'link' in locals() else 'Unknown',
                    'error': str(e)
                })
        
        # Create summary report
        print("\nDownload Summary:")
        print(f"Total rows processed: {len(df)}")
        print(f"Successful downloads: {len(successful_downloads)}")
        print(f"Failed downloads: {len(failed_downloads)}")
        
        # Save download results to CSV files
        if successful_downloads:
            success_df = pd.DataFrame(successful_downloads)
            success_df.to_csv(os.path.join(output_dir, 'successful_downloads.csv'), index=False)
            
        if failed_downloads:
            failed_df = pd.DataFrame(failed_downloads)
            failed_df.to_csv(os.path.join(output_dir, 'failed_downloads.csv'), index=False)
        
        return successful_downloads, failed_downloads


    @classmethod
    def download_youtube_captions(cls, input_file: str, output_dir: str, data_product_id, environment):
        # Read the CSV file
        df = pd.read_csv(input_file)
        successful_downloads = []
        failed_downloads = []
        
        # Loop through each row
        for index, row in df.iterrows():
            try:
                # Get YouTube link from video_url column
                link = row.get('video url', '')
                            
                if not pd.isna(link) and link:  # Check if link exists and is not empty
                    # Download the YouTube video
                    filename = YouTubeDownloader.download_youtube_captions(
                        link,
                        data_product_id,
                        environment,
                        output_dir=output_dir
                    )

                    if filename:
                        # Define the new file name (use the full path)
                        new_file_name = os.path.join(output_dir, row['extended_file_name'])
                        new_file_name = os.path.splitext(new_file_name)[0] + ".vtt"

                        # Rename the file if the download was successful
                        try:
                            original_file_path = os.path.join(output_dir, filename)
                            shutil.move(original_file_path, new_file_name)  # Use shutil.move to rename
                            successful_downloads.append({
                                'original_file': row['extended_file_name'],
                                'downloaded_file': new_file_name,
                                'url': link
                            })
                        except Exception as e:
                            failed_downloads.append({
                                'original_file': row['extended_file_name'],
                                'url': link,
                                'error': f"Renaming failed: {str(e)}"
                            })
                    else:
                        failed_downloads.append({
                            'original_file': row['extended_file_name'],
                            'url': link,
                            'error': 'Download failed'
                        })
                else:
                    print(f"Skipping row {index + 1}: No video URL found")
                    
            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                failed_downloads.append({
                    'original_file': row['extended_file_name'],
                    'url': link if 'link' in locals() else 'Unknown',
                    'error': str(e)
                })
        
        # Create summary report
        print("\nDownload Summary:")
        print(f"Total rows processed: {len(df)}")
        print(f"Successful downloads: {len(successful_downloads)}")
        print(f"Failed downloads: {len(failed_downloads)}")
        
        # Save download results to CSV files
        if successful_downloads:
            success_df = pd.DataFrame(successful_downloads)
            success_df.to_csv(os.path.join(output_dir, 'successful_downloads.csv'), index=False)
            
        if failed_downloads:
            failed_df = pd.DataFrame(failed_downloads)
            failed_df.to_csv(os.path.join(output_dir, 'failed_downloads.csv'), index=False)
        
        return successful_downloads, failed_downloads

            
    @classmethod
    def enrich_video_details(cls, input_csv, output_csv, data_product_id, environment):
        """
        Reads the sessions CSV and enriches it with video and slides URLs.
        """
        # Read the CSV file
        df = pd.read_csv(input_csv)
        
        # Initialize the WebDriver
        driver = cls.setup_driver(data_product_id, environment)
        
        try:
            # Initialize empty lists for each field
            video_ids = []
            titles = []
            channel_ids = []
            channels = []
            view_counts = []
            like_counts = []
            comment_counts = []
            durations = []
            upload_dates = []
            descriptions = []
            tags_list = []
            categories_list = []
            webpage_urls = []
            average_ratings = []

            # Process each session
            total_sessions = len(df)
            for idx, row in df.iterrows():
                video_url = row['video url']
                print(f"Processing session {idx + 1} of {total_sessions}: {video_url}")
                
                if video_url:
                    video_info = YouTubeDownloader.get_video_info(video_url)
                    if video_info:
                        video_ids.append(video_info.get('video_id', ''))
                        titles.append(video_info.get('title', ''))
                        channel_ids.append(video_info.get('channel_id', ''))
                        channels.append(video_info.get('channel', ''))
                        view_counts.append(video_info.get('view_count', 0))
                        like_counts.append(video_info.get('like_count', 0))
                        comment_counts.append(video_info.get('comment_count', 0))
                        durations.append(video_info.get('duration', 0))
                        upload_dates.append(video_info.get('upload_date', ''))
                        descriptions.append(video_info.get('description', ''))
                        tags_list.append(video_info.get('tags', ''))
                        categories_list.append(video_info.get('categories', ''))
                        webpage_urls.append(video_info.get('webpage_url', ''))
                        average_ratings.append(video_info.get('average_rating', 0))
                    else:
                        # Append empty/default values if video info not available
                        video_ids.append('')
                        titles.append('')
                        channel_ids.append('')
                        channels.append('')
                        view_counts.append(0)
                        like_counts.append(0)
                        comment_counts.append(0)
                        durations.append(0)
                        upload_dates.append('')
                        descriptions.append('')
                        tags_list.append('')
                        categories_list.append('')
                        webpage_urls.append('')
                        average_ratings.append(0)
                else:
                    # Append empty/default values if no video URL
                    video_ids.append('')
                    titles.append('')
                    channel_ids.append('')
                    channels.append('')
                    view_counts.append(0)
                    like_counts.append(0)
                    comment_counts.append(0)
                    durations.append(0)
                    upload_dates.append('')
                    descriptions.append('')
                    tags_list.append('')
                    categories_list.append('')
                    webpage_urls.append('')
                    average_ratings.append(0)
            
            # Add new columns to the DataFrame
            # Add new columns to the DataFrame
            df['video_id'] = pd.Series(video_ids).astype(str)
            df['title'] = pd.Series(titles).astype(str)
            df['channel_id'] = pd.Series(channel_ids).astype(str)
            df['channel'] = pd.Series(channels).astype(str)
            df['view_count'] = pd.to_numeric(pd.Series(view_counts), errors='coerce').fillna(0).astype(int)
            df['like_count'] = pd.to_numeric(pd.Series(like_counts), errors='coerce').fillna(0).astype(int)
            df['comment_count'] = pd.to_numeric(pd.Series(comment_counts), errors='coerce').fillna(0).astype(int)
            df['duration'] = pd.to_numeric(pd.Series(durations), errors='coerce').fillna(0).astype(int)
            df['upload_date'] = pd.to_datetime(pd.Series(upload_dates), format='%Y%m%d', errors='coerce')
            df['description'] = pd.Series(descriptions).astype(str)
            df['tags'] = pd.Series(tags_list).astype(str)
            df['categories'] = pd.Series(categories_list).astype(str)
            df['webpage_url'] = pd.Series(webpage_urls).astype(str)
            df['average_rating'] = pd.to_numeric(pd.Series(average_ratings), errors='coerce').fillna(0.0).astype(float)
            
            # Save the enriched data
            df.to_csv(output_csv, index=False)
            print(f"Enriched data saved to {output_csv}")
            
        finally:
            driver.quit()
            print("Browser closed")
            
            
    @staticmethod
    def convert_enriched_to_dataset_format(input_file: str, output_file: str,  data_product_id, environment):
        """
        Convert input CSV to the specified format with predefined columns and values.
        
        Args:
            input_file (str): Path to input CSV file
            output_file (str): Path to output CSV file
        """
        # Read the input CSV
        df = pd.read_csv(input_file)
        
        # Create new DataFrame with specified columns
        new_df = pd.DataFrame(columns=[
            '__meta_ingress_file_path', 'data_product_id', 'database', 'dataset_name',
            'file_name', 'folder_name', 'folder_name_source', 'format', 'row_id_keys',
            'column_ordinal_sort', 'dataset_friendly_name', 'dataset_description',
            'dataset_notes', 'expected_row_count_min', 'expected_row_count_max',
            'expected_values', 'expected_values_source', 'column_header_skip_rows',
            'compare_filter', 'compare_table', 'compare_row_id_keys', 'crdy_domain',
            'crdy_is_sa_dataset', 'crdy_maximum_latency_hours', 'crdy_subdomain',
            'crdy_subdomain2', 'edc_access_level', 'edc_alation_datasource_id',
            'edc_alation_datasource_identifier', 'edc_alation_schema_id',
            'edc_applicability_end_date', 'edc_applicability_start_date',
            'edc_citation', 'edc_conform_to_standard', 'edc_homepage_ur',
            'edc_identifier', 'edc_is_containing_pii', 'edc_language', 'edc_license',
            'edc_pii_comments', 'edc_pii_fields', 'edc_reference', 'edc_referenced_by',
            'edc_release_date', 'edc_size', 'edc_submitting_user', 'edc_tags',
            'edc_update_frequency', 'encoding', 'entity', 'excluded_environments',
            'frequency', 'incremental', 'is_active', 'is_export_schema_required',
            'is_multiline', 'is_refreshed', 'is_required_for_power_bi',
            'optimize_columns', 'optimize_type', 'pii_columns', 'workflow_batch_group',
            'remove_columns_with_no_metadata', 'row_id_core_columns',
            'use_liquid_clustering', 'partition_by', 'sheet_name',
            'source_abbreviation', 'source_dataset_name', 'source_json_path'
        ])
        
        # For each row in input DataFrame, create a new row with default values
        for _, row in df.iterrows():
            new_row = {
                '__meta_ingress_file_path': row['extended_file_name'],
                'data_product_id': 'lava_video',
                'database': 'edav_prd_cdh.cdh_lava_dev',
                'dataset_name': row['extended_file_name'],
                'file_name': row['extended_file_name'],
                'folder_name': 'abfss://cdh@edavcdhproddlmprd.dfs.core.windows.net/raw/lava/lava_video/data/youtube/',
                'folder_name_source': 'use_folder_name_column',
                'format': 'youtube',
                'row_id_keys': '',
                'column_ordinal_sort': 'alpha',
                'crdy_is_sa_dataset': 'TRUE',
                'encoding': 'UTF-8',
                'frequency': 'weekly',
                'incremental': 'incremental_with_purge',
                'is_active': 'TRUE',
                'is_export_schema_required': 'TRUE',
                'is_multiline': 'TRUE',
                'is_refreshed': 'TRUE',
                'is_required_for_power_bi': 'FALSE',
                'optimize_columns': 'FALSE',
                'workflow_batch_group': '5',
                'remove_columns_with_no_metadata': 'FALSE',
                'use_liquid_clustering': 'TRUE',
                'partition_by': '',
                'sheet_name': '0',
                'source_abbreviation': 'youtube',
                'source_dataset_name': row['video url'] if pd.notna(row['video url']) else '',
                'source_json_path': ''
            }
            new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save to CSV
        new_df.to_csv(output_file, index=False)