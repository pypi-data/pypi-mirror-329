import requests
from bs4 import BeautifulSoup

import os
import sys

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import sys
import re

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

import pandas as pd
import requests

class AltmetricDownloader:
    """
    A class that provides methods for updating an Excel file with Altmetric scores and citation counts based on altmetric IDs,
    as well as downloading Altmetric data for a given Altmetric ID.
    """

    @classmethod
    def update_excel_file(cls, excel_path, output_path, data_product_id, environment):
        """
        Updates an Excel file with Altmetric scores and citation counts based on altmetric IDs.

        Args:
            excel_path (str): The path to the input Excel file.
            output_path (str): The path where the updated Excel file will be saved.
            data_product_id (str): The ID of the data product, for logging purposes.
            environment (str): The environment in which the function is executed.
        """
        df = pd.read_excel(excel_path)

        # Ensure necessary columns exist
        if 'Altmetric Score' not in df.columns:
            df['Altmetric Score'] = None
        if 'Citation Count' not in df.columns:
            df['Citation Count'] = None

        # Iterate over DataFrame rows and update with altmetric data
        for index, row in df.iterrows():
            altmetric_id = row['altmetric_id']
            data = cls.download_altmetric_data(altmetric_id, data_product_id, environment)
            if data:
                df.at[index, 'Altmetric Score'] = data.get('Altmetric Score', None)
                df.at[index, 'Citation Count'] = data.get('Citation Count', None)

        # Save the updated DataFrame to a new Excel file
        df.to_excel(output_path, index=False)
        print("Updated Excel file has been saved.")

    @staticmethod
    def download_altmetric_data(altmetric_id, data_product_id, environment):
        """
        Downloads Altmetric data for a given Altmetric ID.

        Args:
            altmetric_id (str): The Altmetric ID for the publication.
            data_product_id (str): The ID of the data product.
            environment (str): The environment in which the function is being executed.

        Returns:
            dict: A dictionary containing the Altmetric Score and Citation Count for the publication.
                If the data cannot be downloaded or an error occurs, None is returned.
        """
        # Code for downloading Altmetric data

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("__init__"):
            try:

                if altmetric_id is None:
                    raise ValueError("altmetric_id cannot be None.")

                logger.info(f'altmetric_id: {altmetric_id}')

                url = f"https://cdc.altmetric.com/details/{altmetric_id}"
    
                logger.info(f'Downloading data from: {url}')

                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
        
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code

                # For debugging: print the entire HTML
                html_content = response.text
                logger.info(f'HTML Content: {html_content}')  # This will print the entire HTML to the log

                soup = BeautifulSoup(response.content, 'html.parser')

                # Initialize the results dictionary
                results = {
                    'Altmetric Score': 'Not found',
                    'Citation Count': 'Not found'
                }

                # Find the Altmetric score using regex to search within the 'style' attribute
                score_style = soup.find('div', style=re.compile(r'score=\d+'))
                if score_style:
                    score = re.search(r'score=(\d+)', score_style['style'])
                    if score:
                        results['Altmetric Score'] = score.group(1)

                # Find the number of citations, again using regex for the 'strong' tag
                
                # Find the <strong> tag within the <dd> tag that contains the citation count
                citation_count_strong_tag = soup.find('dl', class_='scholarly-citation-counts').find('dd').find('strong')

                # Extract the text from the <strong> tag to get the citation count')
                if citation_count_strong_tag:
                    results['Citation Count'] = citation_count_strong_tag.text.strip()
 
                
                # Parse the HTML with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract the title
                title_tag = soup.find('div', class_='document-header').find('h1')
                title = title_tag.get_text(strip=True) if title_tag else "Title not found"

                # Extract the journal
                journal_info = soup.find('th', text='Published in').find_next_sibling('td')
                journal = journal_info.get_text(strip=True) if journal_info else "Journal not found"

                # Extract the authors
                authors_list = soup.find('th', text='Authors').find_next_sibling('td').find('p')
                authors = authors_list.get_text(strip=True) if authors_list else "Authors not found"

                # Extract the DOI
                doi_tag = soup.find('th', text='DOI').find_next_sibling('td').find('a')
                doi = doi_tag.get_text(strip=True) if doi_tag else "DOI not found"

                # Attempt to extract the year from the journal info or DOI
                # This example assumes the year might be part of the journal text or the DOI section.
                # Adjust as necessary based on the actual HTML structure and available information.
                year_match = re.search(r'(\d{4})', journal_info.get_text() if journal_info else "")
                year = year_match.group(1) if year_match else "Year not found"

                # Extract the Publisher's Site URL
                publisher_site_tag = soup.find('a', class_='publisher button')
                publisher_site_url = publisher_site_tag['href'] if publisher_site_tag else "Publisher's site URL not found"

                # Update the results dictionary to include title, journal, and authors
                results.update({
                    'Title': title,
                    'Journal': journal,
                    'Authors': authors,
                    'Year': year,
                    'DOI': doi,
                    'Publisher Site URL': publisher_site_url
                })

                return results
            except requests.HTTPError as e:
                logger.error(f'HTTP Error occurred: {e}')
                return None
            except requests.RequestException as e:
                logger.error(f'Request exception occurred: {e}')
                return None
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise