import pandas as pd
import os
import sys
import numpy as np

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class ExcelSheetCombiner:
    
    # Function to check if a column is blank
    @staticmethod
    def is_blank_column(col):
        # Correctly evaluates if column header is empty or NaN
        return (isinstance(col, str) and col.strip() == '') or str(col) == ''

    @staticmethod
    def extract_list_headers( file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("extract_list_headers"):
            try:                 
                # Load the 'lists' sheet into a DataFrame
                lists_df = pd.read_excel(file_path, sheet_name='lists', dtype=str)
                lists_df['code_type'] = "local_valueset"
                lists_df['valueset_code'] = "code_" + lists_df['list'].astype(str)
                return lists_df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

 
    @classmethod
    def is_blank_column(cls, col):
        # Handle non-string types
        if isinstance(col, str):
            return not col or col.strip() == ""
        return False

    @classmethod
    def combine_sheets(cls, file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("combine_sheets", attributes={"data_product_id": str(data_product_id), "environment": str(environment)}):
            try:
                # Load the Excel file
                xls = pd.ExcelFile(file_path)
                logger.info(f"Loaded Excel file: {file_path}")
                
                # Get details on expected list of sheets
                df_list_headers = cls.extract_list_headers(file_path, data_product_id, environment)

                # Retrieve all sheet names
                sheets = xls.sheet_names
                logger.info(f"Found sheets: {sheets}")
                
                # Find the first sheet that contains 'lists' in its name to determine the cutoff
                list_sheets = [sheet for sheet in sheets if 'lists' in sheet.lower()]
                if not list_sheets:
                    raise ValueError("No 'lists' tabs found in the Excel file.")
                
                logger.info(f"'Lists' sheets found: {list_sheets}")
                
                # Determine the index of the last 'lists' sheet
                last_list_index = max(sheets.index(sheet) for sheet in list_sheets)
                logger.info(f"Last 'lists' sheet index: {last_list_index}")

                # Define the new column names
                new_columns = ['data_product_id', 'code_type', 'valueset_code', 'feature_name', 'parent_valueset_code', 'parent_concept_code', 'concept_code', 'concept_name',  'concept_sort', 'description','category_valueset_code','category_concept_code', 'concept_category_sort','formula','visibility_valueset_code','visibility_concept_code', 'color', 'meta_yyyy', 'meta_mm', 'viz_app_code', 'concept_key', 'view_by_list','sheet_name']
                
                # Initialize an empty DataFrame to append df_sheet
                # Initialize an empty DataFrame to append df_sheet
                combined_data = pd.DataFrame(columns=new_columns)

                # Process each sheet past the last 'lists' sheet
                for sheet in sheets[last_list_index + 1:]:
                    
                    df_single_sheet = pd.read_excel(file_path, sheet_name=sheet, header=0, dtype=str)

                
                    # Filter rows where 'item_code' is not empty or blank
                    if 'item_code' in df_single_sheet.columns:
                        df_single_sheet['item_code'] = df_single_sheet['item_code'].astype(str)
                        df_single_sheet = df_single_sheet[df_single_sheet['item_code'].notna() & (df_single_sheet['item_code'].str.strip() != '')]
                    else:
                        logger.warning(f"'item_code' column not found in sheet: {sheet}")
                        continue
                    
                    df_list_headers['list'] = df_list_headers['list'].fillna('').astype(str)
                    df_single_sheet['list'] = df_single_sheet['list'].fillna('').astype(str)

                    # Ensure 'list' column in df_list_headers contains only strings before applying string operations
                    if 'list' in df_list_headers.columns:
                        df_list_headers['list'] = df_list_headers['list'].apply(
                            lambda x: x.lower().strip() if isinstance(x, str) else x
                        )

                    # Ensure 'list' column in df_single_sheet contains only strings before applying string operations
                    if 'list' in df_single_sheet.columns:
                        df_single_sheet['list'] = df_single_sheet['list'].apply(
                            lambda x: x.lower().strip() if isinstance(x, str) else x
                        )

                    logger.info(f"List headers (processed): {df_list_headers.head()}")
                    logger.info(f"Single sheet (processed): {df_single_sheet.head()}")

                    # Rename columns using a dictionary
                    df_single_sheet = df_single_sheet.rename(columns={'item_name': 'concept_name', 'item_code': 'concept_code'})

                    df_sheet = pd.merge(df_list_headers, df_single_sheet, on='list', how='left')

                    logger.info(f"Post-merge DataFrame shape: {df_sheet.shape}")
                    logger.info(f"Post-merge DataFrame sample: {df_sheet[['list',  'concept_code']].head()}")

                    logger.info(f"Processing sheet: {sheet}, Number of rows: {df_sheet.shape[0]}, Number of columns: {df_sheet.shape[1]}")

 

                    # Strip and lowercase column names
                    df_sheet.columns = [col.strip().lower() for col in df_sheet.columns]

                    # Align the columns with the predefined set of columns
                    for col in new_columns:
                        if col not in df_sheet.columns:
                            # Populate missing columns based on conditions
                            if col == 'code_type':
                                df_sheet[col] = 'local_valueset'
                            elif col == 'valueset_code':
                                df_sheet[col] = 'code_' + df_sheet['list'].astype(str)
                            elif col == 'feature_name':
                                df_sheet[col] = df_sheet['list'].astype(str)
                            elif col == 'parent_valueset_code':
                                df_sheet[col] = df_sheet['ancestor_list'].astype(str) if 'ancestor_list' in df_sheet.columns else ""
                            elif col == 'parent_concept_code':
                                df_sheet[col] = df_sheet['ancestor_value'].astype(str) if 'ancestor_value' in df_sheet.columns else ""
                            elif col == 'concept_sort':
                                df_sheet[col] = df_sheet['item_sort'].astype(str) if 'item_sort' in df_sheet.columns else df_sheet.index.astype(str)
                            elif col == 'description':
                                df_sheet[col] = df_sheet['item_description'].astype(str) if 'item_description' in df_sheet.columns else ""
                            elif col == 'category_valueset_code':
                                df_sheet[col] = np.where(df_sheet['has_category'].astype(str) == 'Y', 
                                                        df_sheet['list'].astype(str) + "_category", 
                                                        '') if 'has_category' in df_sheet.columns else ""
                            elif col == 'category_concept_code':
                                df_sheet[col] = df_sheet['item_category'].astype(str) if 'item_category' in df_sheet.columns else ""
                            elif col == 'concept_category_sort':
                                df_sheet[col] = df_sheet['item_sort'].astype(str) if 'item_sort' in df_sheet.columns else df_sheet.index.astype(str)
                            elif col == 'formula':
                                df_sheet[col] = df_sheet['item_formula'].astype(str) if 'item_formula' in df_sheet.columns else ''
                            elif col == 'numerator':
                                df_sheet[col] = df_sheet['item_numerator'].astype(str) if 'item_numerator' in df_sheet.columns else ''
                            elif col == 'denominator':
                                df_sheet[col] = df_sheet['item_denominator'].astype(str) if 'item_denominator' in df_sheet.columns else ''
                            elif col == 'visibility_valueset_code':
                                df_sheet[col] = 'code_viz_persona'
                            elif col == 'visibility_concept_code':
                                df_sheet[col] = df_sheet['item_visibility'].astype(str) if 'item_visibility' in df_sheet.columns else ''
                            elif col == 'color':
                                df_sheet[col] = df_sheet['item_color'].astype(str) if 'item_color' in df_sheet.columns else ''
                            elif col == 'viz_app_code':
                                df_sheet[col] = df_sheet['app_code'].astype(str) if 'app_code' in df_sheet.columns else ""
                            elif col == 'view_by_list':
                                df_sheet[col] = ""        
                            else:
                                df_sheet[col] = pd.NA

                    # Ensure additional columns are formatted as strings, and add them if missing
                    if 'meta_yyy' not in df_sheet.columns:
                        df_sheet['meta_yyy'] = pd.NA
                    else:
                        df_sheet['meta_yyy'] = df_sheet['meta_yyy'].astype(str)

                    if 'data_product_id' not in df_sheet.columns:
                        df_sheet['data_product_id'] = pd.NA
                    else:
                        df_sheet['data_product_id'] = df_sheet['data_product_id'].astype(str)

                    if 'meta_mm' not in df_sheet.columns:
                        df_sheet['meta_mm'] = pd.NA
                    else:
                        # Pad numeric values with leading zeros if not NaN
                        df_sheet['meta_mm'] = df_sheet['meta_mm'].apply(lambda x: '{:02d}'.format(int(x)) if pd.notna(x) else '')


                    df_sheet['sheet_name'] = sheet
                    df_sheet = df_sheet[new_columns]
                    # df_sheet = df_sheet[new_columns[:-1]]  # Exclude 'sheet_name' temporarily    
                    df_sheet.fillna('')
                    df_sheet['parent_valueset_code'] = df_sheet['parent_valueset_code'].replace('nan', '')
                    df_sheet['parent_concept_code'] = df_sheet['parent_concept_code'].replace('nan', '')
                    df_sheet['description'] = df_sheet['description'].replace('nan', '')
                    df_sheet['category_valueset_code'] = df_sheet['category_valueset_code'].replace('nan', '')

                    df_sheet['concept_sort'] = df_sheet['concept_sort'].replace('nan', '')
                    # Convert 'concept_sort' to numeric, setting errors to 'coerce' to handle non-numeric values
                    df_sheet['concept_sort'] = pd.to_numeric(df_sheet['concept_sort'], errors='coerce')
                    df_sheet['concept_sort'] = df_sheet['concept_sort'].fillna(0).astype(int) 

     
                    df_sheet['concept_key'] = df_sheet['valueset_code'].astype(str) + '-' + df_sheet['concept_code'].astype(str)
                               
                    # Fill NaN values with a default value (e.g., 0) if needed
                    
                    df_sheet['concept_category_sort'] = df_sheet['concept_category_sort'].replace('nan', '')
                    # Convert 'concept_sort' to numeric, setting errors to 'coerce' to handle non-numeric values
                    df_sheet['concept_category_sort'] = pd.to_numeric(df_sheet['concept_category_sort'], errors='coerce')
                    # Fill NaN values with a default value (e.g., 0) if needed
                    df_sheet['concept_category_sort'] = df_sheet['concept_category_sort'].fillna(0).astype(int)
                    df_sheet['category_concept_code'] = df_sheet['category_concept_code'].replace('nan', '')
                    df_sheet['visibility_concept_code'] = df_sheet['visibility_concept_code'].replace('nan', '')
                    
                    df_sheet['color'] = df_sheet['color'].replace('nan', '')
                    df_sheet['viz_app_code'] = df_sheet['viz_app_code'].replace('nan', '')
                    combined_data = pd.concat([combined_data, df_sheet], ignore_index=True)
                    logger.info(f"Combined df_sheet shape after processing sheet {sheet}: {combined_data.shape}")

                if combined_data.empty:
                    logger.warning("Combined df_sheet is empty after processing all sheets.")
                else:
                    # Remove blank rows based on all columns being NaN
                    combined_data = combined_data.dropna(how='all')
                    combined_data['concept_code'] = combined_data['concept_code'].replace(['null', None], '')
                    combined_data = combined_data[combined_data['concept_code'].notna()]  # Remove nulls
                    combined_data = combined_data[combined_data['concept_code'].str.strip() != '']  # Remove blanks

                    logger.info(f"Shape after dropping blank rows: {combined_data.shape}")

                    # Finding the last non-blank column
                    last_valid_index = len(combined_data.columns) - 1
                    for col in reversed(combined_data.columns):
                        if cls.is_blank_column(col) and combined_data[col].isna().all():
                            last_valid_index -= 1
                        else:
                            break

                    # Dropping blank columns from the end
                    if last_valid_index + 1 < len(combined_data.columns):
                        combined_data = combined_data.iloc[:, :last_valid_index + 1]
                    logger.info(f"Shape after dropping blank columns: {combined_data.shape}")
                   
                    # Remove duplicate rows
                    combined_data = combined_data.drop_duplicates()
                    logger.info(f"Final df_sheet shape: {combined_data.shape}")

                return combined_data

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise