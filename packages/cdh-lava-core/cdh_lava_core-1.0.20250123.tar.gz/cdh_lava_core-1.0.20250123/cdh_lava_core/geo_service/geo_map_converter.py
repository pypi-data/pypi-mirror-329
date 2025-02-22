import geopandas as gpd
import os
import sys
import json
import pandas as pd
from shapely.affinity import translate, scale
from shapely.ops import unary_union
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import matplotlib.pyplot as plt
import topojson as tp
import geojson
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import textwrap
import numpy as np  # Import NumPy for numerical operations
import random
import matplotlib.path as mpath
import matplotlib.transforms as mtransforms
import folium
from folium.plugins import MarkerCluster
import branca
from folium import MacroElement
from jinja2 import Template
import io
import base64
import matplotlib.pyplot as plt

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

# List of states to keep (continental US, Alaska, Hawaii, and Washington DC)
desired_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
    'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 
    'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia'
]

# Mapping of states to census regions (for possible future use)
state_to_region = {
    'Northeast': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania'],
    'Midwest': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
    'South': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'District of Columbia', 'West Virginia', 'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
    'West': ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming', 'Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
}

# Mapping of states to hhs regions (for possible future use)
state_to_hhs_region = {
    'Region 1': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont'],
    'Region 2': ['New Jersey', 'New York'],
    'Region 3': ['Delaware', 'District of Columbia', 'Maryland', 'Pennsylvania', 'Virginia', 'West Virginia'],
    'Region 4': ['Alabama', 'Florida', 'Georgia', 'Kentucky', 'Mississippi', 'North Carolina', 'South Carolina', 'Tennessee'],
    'Region 5': ['Illinois', 'Indiana', 'Michigan', 'Minnesota', 'Ohio', 'Wisconsin'],
    'Region 6': ['Arkansas', 'Louisiana', 'New Mexico', 'Oklahoma', 'Texas'],
    'Region 7': ['Iowa', 'Kansas', 'Missouri', 'Nebraska'],
    'Region 8': ['Colorado', 'Montana', 'North Dakota', 'South Dakota', 'Utah', 'Wyoming'],
    'Region 9': ['Arizona', 'California', 'Hawaii', 'Nevada'],
    'Region 10': ['Alaska', 'Idaho', 'Oregon', 'Washington']
}


# Mapping of states to census divisions (for possible future use)
state_to_division = {
    'New England': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont'],
    'Middle Atlantic': ['New Jersey', 'New York', 'Pennsylvania'],
    'East North Central': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin'],
    'West North Central': ['Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
    'South Atlantic': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'District of Columbia', 'West Virginia'],
    'East South Central': ['Alabama', 'Kentucky', 'Mississippi', 'Tennessee'],
    'West South Central': ['Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
    'Mountain': ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming'],
    'Pacific': ['Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
}

# Mapping of state names to USPS abbreviations
state_name_to_abbreviation = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia':'DC'
}


# Create a custom CSS string
custom_css = """
<style>
.my-cluster-small {
    background-color: rgba(0, 200, 0, 0.6);
    width: 30px;
    height: 30px;
    border-radius: 50%;
    text-align: center;
    color: white;
    font-size: 14px;
    line-height: 30px;
}
.my-cluster-medium {
    background-color: rgba(255, 200, 0, 0.6);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    text-align: center;
    color: white;
    font-size: 16px;
    line-height: 40px;
}
.my-cluster-large {
    background-color: rgba(255, 0, 0, 0.6);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    text-align: center;
    color: white;
    font-size: 18px;
    line-height: 50px;
}
</style>
"""



class GeoMapConverter:
    @staticmethod
    def load_shapefile(shapefile_path, data_product_id, environment):
        """Load the shapefile into a GeoDataFrame."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("load_shapefile"):
            try:
                geo_data_frame = gpd.read_file(shapefile_path)
                logger.info(f"Shapefile {shapefile_path} loaded successfully.")
                logger.info(f"Columns in the shapefile: {str(geo_data_frame.columns)}")
                return geo_data_frame
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def filter_states(gdf):
        """Filter the GeoDataFrame to include only the desired states."""
        return gdf[gdf['NAME'].isin(desired_states)]

    @classmethod
    def move_alaska_hawaii(cls, gdf, data_product_id, environment):
        """Move Alaska and Hawaii for better visualization based on their shape names."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("move_alaska_hawaii"):
            try:
                # Reproject to a common projection for transformation
                gdf = gdf.to_crs("ESRI:102003")

                # Identify Alaska and Hawaii by name
                gdf_alaska = gdf[gdf['NAME'] == 'Alaska']
                gdf_hawaii = gdf[gdf['NAME'] == 'Hawaii']

                if not gdf_alaska.empty:     
                    gdf_alaska = cls.translate_geometries(gdf_alaska, 1300000, -4900000, 0.5, 32)
                    logger.info("Alaska repositioned.")
                if not gdf_hawaii.empty:
                    gdf_hawaii = cls.translate_geometries(gdf_hawaii, 5400000, -1500000, 1, 24)
                    logger.info("Hawaii repositioned.")

                # Remove original Alaska and Hawaii from the main GeoDataFrame
                gdf = gdf[~gdf['NAME'].isin(['Alaska', 'Hawaii'])]

                # Add moved Alaska and Hawaii back to the GeoDataFrame
                gdf = pd.concat([gdf, gdf_alaska, gdf_hawaii])

                return gdf

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def translate_geometries(df, x, y, scale_factor, rotate_angle):
        df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
        center = df.dissolve().centroid.iloc[0]
        df.loc[:, "geometry"] = df.geometry.scale(xfact=scale_factor, yfact=scale_factor, origin=center)
        df.loc[:, "geometry"] = df.geometry.rotate(rotate_angle, origin=center)
        return df

    @classmethod
    def merge_by_division(cls, gdf, data_product_id, environment):
        """Merge states into census divisions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("merge_by_division"):
            try:
                divisions = []
                for division, states in state_to_division.items():
                    division_gdf = gdf[gdf['NAME'].isin(states)]
                    if not division_gdf.empty:
                        merged_division = division_gdf.dissolve()
                        merged_division['NAME'] = division
                        divisions.append(merged_division)
                
                if not divisions:
                    raise ValueError("No divisions were found when merging by division.")
                    
                merged_gdf = pd.concat(divisions, ignore_index=True)
                logger.info("States merged into divisions successfully.")
                return merged_gdf
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def merge_by_region(cls, gdf, data_product_id, environment):
        """Merge states into census regions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("merge_by_region"):
            try:
                regions = []
                for region, states in state_to_region.items():
                    region_gdf = gdf[gdf['NAME'].isin(states)]
                    if not region_gdf.empty:
                        merged_region = region_gdf.dissolve()
                        merged_region['NAME'] = region
                        regions.append(merged_region)
                
                if not regions:
                    raise ValueError("No regions were found when merging by region.")
                    
                merged_gdf = pd.concat(regions, ignore_index=True)
                logger.info("States merged into regions successfully.")
                return merged_gdf
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def merge_by_hhs_region(cls, gdf, data_product_id, environment):
        """Merge states into HHS regions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("merge_by_hhs_region"):
            try:
                regions = []
                for region, states in state_to_hhs_region.items():
                    region_gdf = gdf[gdf['NAME'].isin(states)]
                    if not region_gdf.empty:
                        merged_region = region_gdf.dissolve()
                        merged_region['NAME'] = region
                        regions.append(merged_region)
                
                if not regions:
                    raise ValueError("No regions were found when merging by HHS region.")
                    
                merged_gdf = pd.concat(regions, ignore_index=True)
                logger.info("States merged into HHS regions successfully.")
                return merged_gdf
            except Exception as ex:
                error_msg = f"Error merging HHS regions: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
            
    @classmethod
    def plot_map_with_counties(cls, states_gdf, county_gdf, output_path, data_product_id, environment, move_ak_hi=True, merge_regions=False, merge_divisions=False, print_names=False, print_usps=False, base_color="#a7c1bc", county_color="#d3d3d3"):
        """Plot the map including Alaska and Hawaii with options to move them, merge regions or divisions, and overlay counties."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("plot_map_with_counties"):
            try:
                # Filter the GeoDataFrame to include only desired states
                states_gdf = cls.filter_states(states_gdf)
                county_gdf = county_gdf[county_gdf['STATEFP'].isin(states_gdf['STATEFP'].unique())]

                if move_ak_hi:
                    states_gdf = cls.move_alaska_hawaii(states_gdf, data_product_id, environment)
                    county_gdf = cls.move_alaska_hawaii(county_gdf, data_product_id, environment)
                    
                if merge_regions:
                    states_gdf = cls.merge_by_region(states_gdf, data_product_id, environment)
                
                if merge_divisions:
                    states_gdf = cls.merge_by_division(states_gdf, data_product_id, environment)

                # Reproject to WGS 84 for both state and county GeoDataFrames
                states_gdf = states_gdf.to_crs("EPSG:4326")
                county_gdf = county_gdf.to_crs("EPSG:4326")
                logger.info("Data reprojected to EPSG:4326")

                # Create figure and axes with Matplotlib for the main map
                fig, ax = plt.subplots(1, figsize=(18, 14))
                # Remove the axis box from the main map
                ax.axis('off')
                                
                # Plot states on top with the specified base color
                states_gdf.plot(color=base_color, linewidth=1.0, ax=ax, edgecolor='#4d4d4d')

                # Plot counties first with a lighter color
                county_gdf.plot(color=county_color, linewidth=0.5, ax=ax, edgecolor='gray')

                # Define callouts for smaller states
                callout_states = {
                    'RI': (42.1, -68.0),  # Rhode Island, slightly moved to the left
                    'CT': (41.5, -70.5),  # Connecticut, moved further down and left
                    'NJ': (40.7, -73.0),  # New Jersey, moved further down and left
                    'DE': (42.5, -75.0),  # Delaware, moved significantly north
                    'MD': (37.5, -78.0),  # Maryland, moved significantly down and slightly left
                    'DC': (36.0, -90.0),  # District of Columbia, moved significantly left and down to -90
                }

                # Print names or USPS if requested
                if print_names or print_usps:
                    for x, y, label, usps in zip(states_gdf.geometry.centroid.x, states_gdf.geometry.centroid.y, states_gdf['NAME'], states_gdf['STUSPS']):
                        label_text = label.upper() if print_names else usps.upper()
                        wrapped_label = textwrap.fill(label_text, width=10)  # Wrap text to a specified width (e.g., 10 characters)
                        y_offset = y - 0.15  # Adjust this value as necessary for the correct offset
                        
                        if usps in callout_states:
                            label_x, label_y = callout_states[usps]
                            ax.annotate(label_text, xy=(x, y), xytext=(label_x, label_y), textcoords="offset points",
                                        arrowprops=dict(arrowstyle="-", lw=0.4), ha='center', va='center', fontsize=14, fontweight='bold')
                        else:
                            ax.text(x, y_offset, wrapped_label, fontsize=14, ha='center', color='black', fontweight='bold')

                # Save the figure
                if output_path is not None:
                    fig.savefig(output_path, dpi=400, bbox_inches="tight")
                    logger.info(f"Map saved to {output_path}")

                return states_gdf, fig, ax

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise



    @classmethod
    def plot_map(cls, gdf, output_path, data_product_id, environment, move_ak_hi=False, merge_regions=False, merge_divisions=False, merge_hhs_regions=False, print_names=False, print_usps=False,base_color="#a7c1bc"):
        """Plot the map including Alaska and Hawaii with options to move them and merge regions or divisions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("plot_map"):
            try:
                # Filter the GeoDataFrame to include only desired states
                gdf = cls.filter_states(gdf)

                if move_ak_hi:
                    gdf = cls.move_alaska_hawaii(gdf, data_product_id, environment)

                if merge_hhs_regions:
                    gdf = cls.merge_by_hhs_region(gdf, data_product_id, environment)
                    

                if merge_regions:
                    gdf = cls.merge_by_region(gdf, data_product_id, environment)
                
                if merge_divisions:
                    gdf = cls.merge_by_division(gdf, data_product_id, environment)

                # Reproject to WGS 84
                gdf = gdf.to_crs("EPSG:4326")
                logger.info("Data reprojected to EPSG:4326")

                # Create figure and axes for with Matplotlib for main map
                fig, ax = plt.subplots(1, figsize=(18, 14))
                # Remove the axis box from the main map
                ax.axis('off')
                
                # Create map of all divisions
                gdf.plot(color=base_color, linewidth=1.0, ax=ax, edgecolor='#4d4d4d')

                # Define callouts for smaller states
                callout_states = {
    'RI': (42.1, -68.0),  # Rhode Island, slightly moved to the left
    'CT': (41.5, -70.5),  # Connecticut, moved further down and left
    'NJ': (40.7, -73.0),  # New Jersey, moved further down and left
    'DE': (42.5, -75.0),  # Delaware, moved significantly north
    'MD': (37.5, -78.0),  # Maryland, moved significantly down and slightly left
    'DC': (36.0, -90.0),  # District of Columbia, moved significantly left and down to -90
}


                # Print names or USPS if requested
                if print_names or print_usps:
                    for x, y, label, usps in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['NAME'], gdf['STUSPS']):
                        label_text = label.upper() if print_names else usps.upper()
                        wrapped_label = textwrap.fill(label_text, width=10)  # Wrap text to a specified width (e.g., 10 characters)
                        y_offset = y - 0.15  # Adjust this value as necessary for the correct offset
                        
                        if usps in callout_states:
                            label_x, label_y = callout_states[usps]
                            ax.annotate(label_text, xy=(x, y), xytext=(label_x, label_y), textcoords="offset points",
                                        arrowprops=dict(arrowstyle="-", lw=0.4), ha='center', va='center', fontsize=14, fontweight='bold')
                        else:
                            ax.text(x, y_offset, wrapped_label, fontsize=14, ha='center', color='black', fontweight='bold')

                # Save the figure
                if output_path is not None:
                    fig.savefig(output_path, dpi=400, bbox_inches="tight")
                    logger.info(f"Map saved to {output_path}")

                return gdf, fig, ax

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    @classmethod 
    def plot_map_with_region_and_district_colors(cls, gdf, output_path, data_product_id, environment, move_ak_hi=False, merge_regions=False, merge_divisions=False, print_names=False):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("plot_map_with_region_and_district_colors"):
            try:
                # Filter the GeoDataFrame to include only desired states
                gdf = cls.filter_states(gdf)

                if move_ak_hi:
                    gdf = cls.move_alaska_hawaii(gdf, data_product_id, environment)
                    
                if merge_regions:
                    gdf = cls.merge_by_region(gdf, data_product_id, environment)
                
                if merge_divisions:
                    gdf = cls.merge_by_division(gdf, data_product_id, environment)

                # Reproject to WGS 84
                gdf = gdf.to_crs("EPSG:4326")
                logger.info("Data reprojected to EPSG:4326")

                # Define colors based on the district
                district_colors = {
                    'New England': '#5f9b67',  # Blue
                    'Middle Atlantic': '#a99cc3',  # Orange
                    'East North Central': '#f18651',  # Green
                    'West North Central': '#7fd1dd',  # Red
                    'South Atlantic': '#e4f0f7',  # Purple
                    'East South Central': '#8c564b',  # Brown
                    'West South Central': '#f4c94a',  # Pink
                    'Mountain': '#5995c5',  # Gray
                    'Pacific': '#ea595f',  # Olive
                    # Add more districts if necessary
                }

                region_colors = {
                    'Northeast': '#fdae61',  # Light orange
                    'Midwest': '#fee08b',  # Light yellow
                    'South': '#d73027',  # Red
                    'West': '#4575b4',  # Blue
                    # Add more regions if necessary
                }

                # Apply colors based on merging preference
                if merge_divisions:
                    gdf['color'] = gdf['NAME'].map(district_colors)
                elif merge_regions:
                    gdf['color'] = gdf['NAME'].map(region_colors)
                else:
                    # Default to using district colors if neither regions nor divisions are merged
                    gdf['color'] = gdf['NAME'].map(district_colors)

                # Plot the map with darker gray outlines
                fig, ax = plt.subplots(1, figsize=(18, 14))
                gdf.plot(color=gdf['color'], linewidth=1.0, ax=ax, edgecolor='#4d4d4d')  # Darker gray for outlines

                # Print names if requested
                if print_names:
                    for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['NAME']):
                        wrapped_label = textwrap.fill(label.upper(), width=10)  # Wrap text to a specified width (e.g., 10 characters) and convert to uppercase
                        y_offset = y - 0.15  # Adjust this value as necessary for the correct offset
                        ax.text(x, y_offset, wrapped_label, fontsize=14, ha='center', color='black', fontweight='bold')
                        
                ax.axis('off')

                # Save the figure
                fig.savefig(output_path, dpi=400, bbox_inches="tight")
                logger.info(f"Map saved to {output_path}")

                return gdf, fig, ax

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def csv_to_topojson(cls, csv_file, geojson_file, topojson_file, data_product_id, environment):
        """
        Convert CSV directly to TopoJSON.
        
        :param csv_file: Path to the input CSV file.
        :param geojson_file: Path to the intermediate GeoJSON file.
        :param topojson_file: Path to the final TopoJSON file.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("csv_to_topojson"):
            try:

                cls.csv_to_geojson(csv_file, geojson_file, data_product_id, environment)
                cls.geojson_to_topojson(geojson_file, topojson_file, data_product_id, environment)
                logger.info(f"CSV converted to TopoJSON: {topojson_file}")
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod 
    def clean_geojson(cls, data):
        """
        Recursively clean GeoJSON data by replacing NaN, inf, and -inf values with None.
        """
        if isinstance(data, dict):
            return {k: cls.clean_geojson(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.clean_geojson(item) for item in data]
        elif isinstance(data, float) and (np.isnan(data) or np.isinf(data)):
            return None
        else:
            return data
            
    @classmethod
    def geojson_to_topojson(cls, geojson_file, topojson_file, data_product_id, environment):
        """
        Convert a GeoJSON file to TopoJSON format.
        
        :param geojson_file: Path to the input GeoJSON file.
        :param topojson_file: Path to the output TopoJSON file.
        :param data_product_id: Data product identifier.
        :param environment: Environment name.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("geojson_to_topojson"):
            try:
                # Read the GeoJSON file
                with open(geojson_file, 'r') as f:
                    geojson_data = geojson.load(f)
                
                # Clean the GeoJSON data to replace NaN, inf, and -inf values
                cleaned_geojson_data = cls.clean_geojson(geojson_data)
                
                # Convert cleaned GeoJSON to TopoJSON using the Topology function from the topojson library
                topojson_data = tp.Topology(cleaned_geojson_data)

                # Save the TopoJSON file
                with open(topojson_file, 'w') as f:
                    f.write(topojson_data.to_json())

                logger.info(f"TopoJSON file created: {topojson_file}")

            except FileNotFoundError:
                error_msg = f"File not found: {geojson_file} or {topojson_file}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            except Exception as ex:
                error_msg = f"Error while converting GeoJSON to TopoJSON: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
                    


    @classmethod
    def csv_to_geojson(cls, csv_file, geojson_file, data_product_id, environment):
        """
        Convert CSV to GeoJSON.
        
        :param csv_file: Path to the input CSV file.
        :param geojson_file: Path to the output GeoJSON file.
        :param data_product_id: Data product identifier.
        :param environment: Environment name.
        """

        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("csv_to_geojson"):
            try:
                # Load the CSV file
                df = pd.read_csv(csv_file)

                # Replace NaN, Inf, -Inf with None (to be JSON-compliant)
                df = df.replace([np.inf, -np.inf], None)
                df = df.where(pd.notnull(df), None)

                # Create a GeoDataFrame from the CSV
                gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))

                # Set the initial Coordinate Reference System (CRS) to WGS84 (EPSG:4326)
                gdf.set_crs(epsg=4326, inplace=True)

                # Reproject to ESRI:102003 (USA_Contiguous_Albers_Equal_Area_Conic)
                gdf = gdf.to_crs("ESRI:102003")

                # Convert to GeoJSON features
                features = []
                for _, row in gdf.iterrows():
                    point = geojson.Point((row['Longitude'], row['Latitude']))
                    properties = row.drop(['Latitude', 'Longitude', 'geometry']).to_dict()

                    # Add NAME property if it exists
                    if 'Name' in row:
                        properties['NAME'] = row['Name']
                    
                    # Append the GeoJSON feature
                    features.append(geojson.Feature(geometry=point, properties=properties))

                # Create a GeoJSON FeatureCollection
                feature_collection = geojson.FeatureCollection(features)

                # Clean the GeoJSON data to handle NaN values
                cleaned_feature_collection = cls.clean_geojson(feature_collection)
                
                # Write the GeoJSON to a file
                with open(geojson_file, 'w') as f:
                    geojson.dump(cleaned_feature_collection, f)

                logger.info(f"GeoJSON file created: {geojson_file}")
                return str(geojson_file)

            except Exception as ex:
                error_msg = f"Error while converting CSV to GeoJSON: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
                    
    @classmethod
    def convert_to_topojson(cls, geo_data_frame, output_path, data_product_id, environment, move_ak_hi=False, merge_regions=False, merge_divisions=False, merge_hhs_regions=False):
        """Convert the shapefile to a TopoJSON file."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("convert_to_topojson"):
            try:
                
                if geo_data_frame is not None:
                    # Filter the GeoDataFrame to include only desired states
                    geo_data_frame = cls.filter_states(geo_data_frame)

                    if move_ak_hi:
                        geo_data_frame = cls.move_alaska_hawaii(geo_data_frame, data_product_id, environment)
                        
                    if merge_regions:
                        geo_data_frame = cls.merge_by_region(geo_data_frame, data_product_id, environment)

                    if merge_hhs_regions:
                        geo_data_frame = cls.merge_by_hhs_region(geo_data_frame, data_product_id, environment)
                    
                    if merge_divisions:
                        geo_data_frame = cls.merge_by_division(geo_data_frame, data_product_id, environment)

                    # Reproject to WGS 84
                    geo_data_frame = geo_data_frame.to_crs("EPSG:4326")
                    logger.info("Data reprojected to EPSG:4326")
                        
                    # Log the columns to identify the correct name column
                    logger.info(f"Columns in the shapefile: {str(geo_data_frame.columns)}")

                    # Try common alternatives if 'NAME' is not present
                    name_column = 'NAME'
                    if name_column not in geo_data_frame.columns:
                        possible_columns = ['name', 'Name', 'NAMELSAD', 'GEOID', 'LSAD', 'STUSPS']
                        for possible_col in possible_columns:
                            if possible_col in geo_data_frame.columns:
                                name_column = possible_col
                                break
                        else:
                            raise ValueError("The shapefile does not contain a 'NAME' or similar column for Power BI compatibility.")

                    # Convert GeoDataFrame to GeoJSON
                    geojson_data = json.loads(geo_data_frame.to_json())

                    # Convert GeoJSON to TopoJSON
                    topojson_data = tp.Topology(geojson_data).to_dict()

                    # Save the TopoJSON to a file
                    with open(output_path, 'w') as f:
                        json.dump(topojson_data, f, indent=2)

                    logger.info(f"TopoJSON file has been saved to {output_path}")
                else:
                    raise ValueError("Failed to load the shapefile. Conversion to TopoJSON aborted.")
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def plot_map_with_points(
        cls, base_map_gdf, df_programs, fig, ax, output_path, 
        data_product_id, environment, basecolor='#a7c1bc', emptycolor='#d3d3d3',
        show_pin=True, show_number=True, large_circle=False, prefix_usps=False
    ):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("plot_map_with_points"):
            try:
                # Fill the states with points with the specified base color
                if basecolor is None:
                    base_map_gdf.plot(color='none', linewidth=1.0, ax=ax, edgecolor='#4d4d4d')
                else:
                    base_map_gdf.plot(color=basecolor, linewidth=1.0, ax=ax, edgecolor='#4d4d4d')
                
                # Fill the states without points with a different color if specified
                if emptycolor is not None:
                    states_with_points = df_programs['State/Territory'].unique()
                    states_without_points = base_map_gdf[~base_map_gdf['NAME'].isin(states_with_points)]
                    states_without_points.plot(color=emptycolor, linewidth=1.0, ax=ax, edgecolor='#4d4d4d')

                # Define a custom location pin marker if pins should be shown
               
                # Add program points to the existing GeoDataFrame plot
                for district, group in df_programs.groupby('State/Territory'):
                    # Create a series of numbers for markers in each district
                    numbers = range(1, len(group) + 1)

                    # Plot each point with the custom pin marker or large circle if enabled
                    for i, (index, row) in enumerate(group.iterrows()):
                        if large_circle and show_number:
                            # Large circle with number
                            ax.scatter(
                                row['Longitude'], 
                                row['Latitude'], 
                                s=300,  # Size of the circle
                                marker='o', 
                            color=(0.302, 0.302, 0.302, 0.75),  # Marker fill color
    edgecolor=(0.302, 0.302, 0.302, 0.75)  # Semi-transparent blue (R, G, B, A)
                            )
                            if prefix_usps == True:
                                ax.text(
                                    row['Longitude'], 
                                    row['Latitude'], 
                                    f"{group}{str(numbers[i])}", 
                                    color='white', 
                                    fontsize=10, 
                                    ha='center', 
                                    va='center',
                                    fontweight='bold'
                                )

                            else:
                                ax.text(
                                    row['Longitude'], 
                                    row['Latitude'], 
                                    f"{str(numbers[i])}", 
                                    color='white', 
                                    fontsize=10, 
                                    ha='center', 
                                    va='center',
                                    fontweight='bold'
                                )
                        elif show_pin:
                            # Show pin marker
                            ax.scatter(
                                row['Longitude'], 
                                row['Latitude'], 
                                s=200,  # Size of the outer circle
                                marker='o', 
                                color='none',  # No fill color
                                edgecolor=(0.302, 0.302, 0.302, 0.75),  # Outer circle color
                                linewidth=2  # Outer circle line width
                            )

                            # Inner circle
                            ax.scatter(
                                row['Longitude'], 
                                row['Latitude'], 
                                s=100,  # Size of the inner circle
                                marker='o', 
                                color=(0.302, 0.302, 0.302, 0.75),  # Inner circle fill color
                                edgecolor='none'  # No outline for the inner circle
                            )
                            if show_number:
                                ax.text(
                                    row['Longitude'], 
                                    row['Latitude'] - 0.5,  # Adjust label position slightly below the pin
                                    f"{str(numbers[i])}", 
                                    color=(0.302, 0.302, 0.302, 0.75) ,  # Semi-transparent blue (R, G, B, A)
                                    fontsize=10, 
                                    ha='center', 
                                    va='center',
                                    fontweight='bold'
                                )
                        elif show_number:
                            # Show number only
                            ax.text(
                                row['Longitude'], 
                                row['Latitude'], 
                                f"{str(numbers[i])}", 
                                color='blue', 
                                fontsize=10, 
                                ha='center', 
                                va='center',
                                fontweight='bold'
                            )

                logger.info("Program points added to the map.")
                # Save the figure
                if output_path is not None:
                    fig.savefig(output_path, dpi=400, bbox_inches="tight")
                    logger.info(f"Map saved to {output_path}")

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
    
    @staticmethod
    def create_white_image_url():
        # Create a 2x2 white image using numpy
        img = np.ones((2, 2, 3), dtype=np.uint8) * 255

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')

        # Encode the image to Base64
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Create a data URL
        img_url = f"data:image/png;base64,{img_str}"
        return img_url
        
    @classmethod
    def plot_map_with_zoom_point_mouseovers(
        cls, base_map_gdf, df_programs, output_path=None,
        data_product_id=None, environment=None, basecolor='#a7c1bc', emptycolor='#d3d3d3',
        show_pin=True, show_number=True, large_circle=False, prefix_usps=False
    ):


        # Create a MacroElement to inject the CSS into the map
        css_element = MacroElement()
        css_element._template = Template(custom_css)

        # Create a white image of 4 pixels, and embed it in a URL.
        white_tile = cls.create_white_image_url()

        # Calculate the centroid and shift it eastward by adjusting the longitude
        mean_lat = base_map_gdf.geometry.centroid.y.mean()
        mean_lon = base_map_gdf.geometry.centroid.x.mean()
        shifted_lon = mean_lon - 5  # Shift the center 5 degrees to the east

        # Initialize a Folium map centered around the mean latitude and shifted longitude
        m = folium.Map(
            location=[mean_lat, shifted_lon],
            zoom_start=5,  # Default zoom level set to 5
            tiles=white_tile,  # Light tiles for minimal background
            attr='white_tile',
            min_zoom=5                    # Minimum zoom level (most zoomed out
        )

        # Add the white tile as an overlay to cover the entire map area
        image_overlay = folium.raster_layers.ImageOverlay(
            name='White Background',
            image=white_tile,
            bounds=[[24.396308, -125.0], [49.384358, -66.93457]],  # Approximate bounds for the contiguous US
            opacity=1,
            interactive=False,
            zindex=1
        )

        image_overlay.add_to(m)

        # Create the "Drill Up to US" button (initially hidden)
        drill_up_button = """
        <div id="drill-up-button" style="display:none; position: absolute; top: 10px; left: 10px; z-index: 1000;">
            <button onclick="drillUpToUS()">Drill Up to US</button>
        </div>
        """
        m.get_root().html.add_child(folium.Element(drill_up_button))

        # Add the custom CSS to the map
        m.get_root().add_child(css_element)


        # Plot base_map_gdf with basecolor or emptycolor
        geojson = folium.GeoJson(
            base_map_gdf,
            name='geojson_layer',
            style_function=lambda x: {
                'fillColor': basecolor if x['properties']['NAME'] in df_programs['State/Territory'].values else emptycolor,
                'color': '#4d4d4d',
                'weight': 1,
                'fillOpacity': 0.5
            },
            highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
            tooltip=folium.GeoJsonTooltip(
                fields=['NAME'],
                aliases=['State:']
            )
        )
        geojson.options['custom_id'] = 'geojson_layer'  # Correct way to set custom_id
        geojson.add_to(m)

        # Add state abbreviation labels
        for _, row in base_map_gdf.iterrows():
            state_name = row['NAME']
            state_abbreviation = state_name_to_abbreviation.get(state_name, state_name)
            centroid = row['geometry'].centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 12px; color: black;">{state_abbreviation}</div>'
                )
            ).add_to(m)

        # Create a marker cluster for each state
        state_marker_info = {}
        states = df_programs['State/Territory'].unique()
        for state in states:
            state_cluster = folium.plugins.MarkerCluster().add_to(m)
            state_data = df_programs[df_programs['State/Territory'] == state]
            state_marker_info[state] = len(state_data) > 0  # Store whether the state has markers

            for _, row in state_data.iterrows():
                state_abbreviation = state_name_to_abbreviation.get(row['State/Territory'], row['State/Territory'])

                html = f'''{state_abbreviation}<br>
                {row['Program Name']}<br>
                3rd line'''

                iframe = folium.IFrame(html, width=220, height=100)
                popup = folium.Popup(iframe, max_width=250)

                # Adding the CircleMarker with a tooltip
                folium.Marker(
                    location=(row['Latitude'], row['Longitude']),
                    icon=folium.Icon(color="blue", icon="info-sign"),
                    popup=popup
                ).add_to(state_cluster)


        # Save map to file
        if output_path is not None:
            m.save(output_path)

            # JavaScript for adding click-to-zoom functionality
            custom_js = f"""
            <script>
            document.addEventListener("DOMContentLoaded", function() {{
                try {{
                    // Automatically find the map variable
                    var map = Object.values(window).find(v => v instanceof L.Map);

                    if (!map) {{
                        throw new Error("Map object not found.");
                    }}

                    var originalBounds = map.getBounds(); // Save the original map bounds
                    var activeLayer = null; // Track the currently active (clicked) layer
                    var stateMarkerInfo = {str(state_marker_info).replace("True", "true").replace("False", "false")}; // State marker information

                    function fadeAndFitLayer(clickedLayer) {{
                        // Check if the clicked state has no markers or is styled with emptycolor
                        var stateName = clickedLayer.feature.properties.NAME;
                        var fillColor = clickedLayer.options.fillColor || clickedLayer.defaultOptions.style.fillColor;
                        if (!stateMarkerInfo[stateName] || fillColor === "{emptycolor}") {{
                            var popupContent = `No markers in the selected state: ${{stateName}}`;
                            var popup = L.popup()
                                .setLatLng(clickedLayer.getBounds().getCenter())
                                .setContent(popupContent)
                                .openOn(map);
                            return;  // Do not proceed with zoom if the state is empty
                        }}

                        if (activeLayer) {{
                            activeLayer.setStyle({{
                                fillOpacity: 0.1,
                                opacity: 0.1
                            }});
                        }}

                        map.eachLayer(function(layer) {{
                            if (layer.options && layer.options.custom_id === 'geojson_layer') {{
                                if (layer !== clickedLayer) {{
                                    layer.setStyle({{
                                        fillOpacity: 0.1,
                                        opacity: 0.1
                                    }});
                                }} else {{
                                    layer.setStyle({{
                                        fillOpacity: 0.75,
                                        opacity: 1
                                    }});

                                    var layerBounds = layer.getBounds();
                                    if (layerBounds.isValid()) {{
                                        map.fitBounds(layerBounds, {{
                                            padding: [20, 20],
                                            maxZoom: 16
                                        }});
                                        document.getElementById('drill-up-button').style.display = 'block'; // Show button
                                    }}
                                    activeLayer = layer; // Set the clicked layer as active
                                }}
                            }}
                        }});

                        // Disable highlight on hover after a state is clicked
                        map.eachLayer(function(layer) {{
                            if (layer.options && layer.options.custom_id === 'geojson_layer') {{
                                if (layer.eachLayer) {{
                                    layer.eachLayer(function(subLayer) {{
                                        subLayer.off('mouseover');  // Disable hover effect
                                        subLayer.off('mouseout');  // Disable hover effect
                                    }});
                                }} else {{
                                    layer.off('mouseover');  // Disable hover effect
                                    layer.off('mouseout');  // Disable hover effect
                                }}
                            }}
                        }});
                    }}

                    function drillUpToUS() {{
                        // Set the map view to the original center with zoom level 5
                        var center = originalBounds.getCenter(); // Get the center of the original bounds
                        map.setView(center, 5); // Set view to center with zoom level 5

                        document.getElementById('drill-up-button').style.display = 'none'; // Hide button
                        activeLayer = null; // Reset the active layer
                        map.eachLayer(function(layer) {{
                            if (layer.options && layer.options.custom_id === 'geojson_layer') {{
                                if (layer.eachLayer) {{
                                    layer.eachLayer(function(subLayer) {{
                                        subLayer.setStyle({{
                                            fillOpacity: 0.5,
                                            opacity: 1
                                        }});
                                    }});
                                }} else {{
                                    layer.setStyle({{
                                        fillOpacity: 0.5,
                                        opacity: 1
                                    }});
                                }}
                            }}
                        }});

                        // Re-enable highlight on hover after resetting to the US view
                        attachLayerHoverEvents(map);
                    }}

                    function attachLayerHoverEvents(map) {{
                        map.eachLayer(function(layer) {{
                            if (layer.options && layer.options.custom_id === 'geojson_layer') {{
                                if (layer.eachLayer) {{
                                    layer.eachLayer(function(subLayer) {{
                                        subLayer.on('mouseover', function(e) {{
                                            subLayer.setStyle({{ weight: 3, color: 'blue' }});
                                        }});
                                        subLayer.on('mouseout', function(e) {{
                                            subLayer.setStyle({{ weight: 1, color: '#4d4d4d' }});
                                        }});
                                    }});
                                }} else {{
                                    layer.on('mouseover', function(e) {{
                                        layer.setStyle({{ weight: 3, color: 'blue' }});
                                    }});
                                    layer.on('mouseout', function(e) {{
                                        layer.setStyle({{ weight: 1, color: '#4d4d4d' }});
                                    }});
                                }}
                            }}
                        }});
                    }}

                    function attachLayerClickEvents(map) {{
                        map.eachLayer(function(layer) {{
                            if (layer.options && layer.options.custom_id === 'geojson_layer') {{
                                if (layer.eachLayer) {{
                                    layer.eachLayer(function(subLayer) {{
                                        subLayer.on('click', function(e) {{
                                            fadeAndFitLayer(subLayer);
                                        }});
                                    }});
                                }} else {{
                                    layer.on('click', function(e) {{
                                        fadeAndFitLayer(layer);
                                    }});
                                }}
                            }}
                        }});
                    }}

                    // Initial attachment of click and hover events
                    attachLayerClickEvents(map);
                    attachLayerHoverEvents(map);

                    window.drillUpToUS = drillUpToUS;
                }} catch (error) {{
                    console.error("An error occurred while setting up the map:", error);
                    alert("An error occurred while setting up the map. Please check the console for details.");
                }}
            }});
            </script>
            """

            # Append the custom JavaScript after the map is saved
            with open(output_path, 'a') as f:
                f.write(custom_js)

        return m


# Example usage
if __name__ == "__main__":
    shapefile_path = 'path_to_your_shapefile.shp'
    output_map_path = 'output_map.png'
    output_topojson_path = 'output_map.topojson'
    data_product_id = 'your_data_product_id'
    environment = 'your_environment'

    # Load and process shapefile
    gdf = GeoMapConverter.load_shapefile(shapefile_path, data_product_id, environment)
    
    # Plot map with moving Alaska and Hawaii
    GeoMapConverter.plot_map(gdf, output_map_path.replace(".png", "_moved.png"), data_product_id, environment, move_ak_hi=True, merge_regions=True)

    # Convert to TopoJSON
    GeoMapConverter.convert_to_topojson(gdf, output_topojson_path, data_product_id, environment, move_ak_hi=True, merge_regions=True)
