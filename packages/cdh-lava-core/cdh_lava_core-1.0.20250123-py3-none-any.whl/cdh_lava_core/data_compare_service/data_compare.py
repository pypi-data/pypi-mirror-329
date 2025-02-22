import pandas as pd
from ydata_profiling import ProfileReport

class DataComparison:
    @staticmethod
    def load_csv(file_path):
        """Load a CSV file into a pandas DataFrame."""
        return pd.read_csv(file_path)
    
    @staticmethod
    def generate_profile_report(df, title):
        """Generate a profile report for a DataFrame."""
        return ProfileReport(df, title=title)
    
    @staticmethod
    def compare_profiles(profile1, profile2, output_file):
        """Compare two profile reports and save the comparison to an HTML file."""
        comparison = profile1.compare(profile2)
        comparison.to_file(output_file)
        print(f"Comparison report saved to '{output_file}'")
    
    @staticmethod
    def apply_filter(df, filter_clause=None):
        """Apply a filter clause to a DataFrame."""
        if filter_clause:
            df = df.query(filter_clause)
        return df

    @classmethod
    def compare_csv_files(cls, file1, file2, output_file, filter_clause1=None, filter_clause2=None):
        """Load two CSV files, apply filters, generate their profile reports, and compare them."""
        df1 = cls.load_csv(file1)
        df2 = cls.load_csv(file2)
        
        df1 = cls.apply_filter(df1, filter_clause1)
        df2 = cls.apply_filter(df2, filter_clause2)
        
        profile1 = cls.generate_profile_report(df1, title=f"{file1}")
        profile2 = cls.generate_profile_report(df2, title=f"{file2}")
        
        cls.compare_profiles(profile1, profile2, output_file)

# Example usage
if __name__ == "__main__":
    file1 = 'file1.csv'
    file2 = 'file2.csv'
    output_file = 'comparison_report.html'
    
    DataComparison.compare_csv_files(file1, file2, output_file)
