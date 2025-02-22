from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql import DataFrame

class DatasetPivot:
    
    @classmethod
    def pivot_dataframe(cls, df: DataFrame, pivot_col: str, value_col: str, agg_func: str = 'sum') -> DataFrame:
        """
        Pivots a DataFrame dynamically without hardcoding column names.
        
        Parameters:
        - df: Input DataFrame.
        - pivot_col: Column name to pivot.
        - value_col: Column name with values to aggregate.
        - agg_func: Aggregation function to use. Default is 'sum'.
        
        Returns:
        - Pivoted DataFrame.
        """
        # Get unique values in the pivot column
        pivot_values = df.select(pivot_col).distinct().rdd.flatMap(lambda x: x).collect()
        
        # Create a list of pivot expressions
        pivot_exprs = [cls._create_pivot_expr(pivot_col, value_col, value, agg_func) for value in pivot_values]
        
        # Group by all columns except the pivot column and the value column
        group_by_cols = [col for col in df.columns if col not in [pivot_col, value_col]]
        
        # Perform the pivot
        pivoted_df = df.groupBy(group_by_cols).agg(*pivot_exprs)
        
        return pivoted_df

    @staticmethod
    def _create_pivot_expr(pivot_col: str, value_col: str, pivot_value: str, agg_func: str):
        """
        Creates a pivot expression for a given pivot value.
        
        Parameters:
        - pivot_col: Column name to pivot.
        - value_col: Column name with values to aggregate.
        - pivot_value: Specific value in the pivot column.
        - agg_func: Aggregation function to use.
        
        Returns:
        - Pivot expression.
        """
        return (lit(pivot_value).alias(pivot_value), col(value_col)).alias(f"{agg_func}({value_col})")

# Example usage:
if __name__ == "__main__":
    spark = SparkSession.builder.appName("DynamicPivotExample").getOrCreate()
    
    # Example DataFrame
    data = [("A", "Category1", 100),
            ("B", "Category2", 200),
            ("A", "Category2", 150),
            ("B", "Category1", 250)]
    
    columns = ["Name", "Category", "Value"]
    
    df = spark.createDataFrame(data, columns)
    
    # Pivot the DataFrame
    pivoted_df = DatasetPivot.pivot_dataframe(df, pivot_col="Category", value_col="Value")
    
    pivoted_df.show()
