import pandas as pd
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import logging
import mlflow
import mlflow.sklearn

class DQRootCauseAnalyzer:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.feature_encoders = {}
        self.feature_names = None
        self.shap_values = None
        
    def prepare_data(
        self,
        exceptions_df: pd.DataFrame,
        shared_columns: List[str]
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Prepares data for SHAP analysis by focusing only on exceptions.
        """
        X = exceptions_df[shared_columns].copy()
        y = exceptions_df['is_missing'].values
        
        # Encode categorical variables
        for column in shared_columns:
            if X[column].dtype == 'object' or X[column].dtype.name == 'category':
                encoder = LabelEncoder()
                X[column] = encoder.fit_transform(X[column].astype(str))
                self.feature_encoders[column] = encoder
                
        self.feature_names = shared_columns
        return X, y
    
    def fit(
        self,
        actual_df: pd.DataFrame,
        expected_df: pd.DataFrame,
        pk_column: str,
        shared_columns: List[str],
        n_estimators: int = 100
    ) -> None:
        """
        Identifies exceptions and fits a RandomForest model for SHAP analysis.
        """
        with mlflow.start_run():
            # Identify exceptions
            missing_in_actual = set(expected_df[pk_column]) - set(actual_df[pk_column])
            missing_in_expected = set(actual_df[pk_column]) - set(expected_df[pk_column])

            # Prepare data with 'is_missing' labels
            exceptions_actual = actual_df[actual_df[pk_column].isin(missing_in_expected)].copy()
            exceptions_actual['is_missing'] = 0
            exceptions_expected = expected_df[expected_df[pk_column].isin(missing_in_actual)].copy()
            exceptions_expected['is_missing'] = 1
            
            # Combine exceptions
            exceptions_combined = pd.concat([exceptions_actual, exceptions_expected], ignore_index=True)
            
            # Prepare data for modeling
            X, y = self.prepare_data(exceptions_combined, shared_columns)
            
            # Train the RandomForest model
            self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
            self.model.fit(X, y)
            mlflow.log_params({"n_estimators": n_estimators, "random_state": 42})
            mlflow.sklearn.log_model(self.model, "model")

            # Create SHAP explainer
            self.explainer = shap.TreeExplainer(self.model)
            self.shap_values = self.explainer.shap_values(X)
            np.save("/tmp/shap_values.npy", self.shap_values)
            mlflow.log_artifact("/tmp/shap_values.npy", "shap_values")
    
    def analyze_global_impact(self) -> Dict:
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated. Please run fit() first.")
        feature_importance = {feature: np.abs(self.shap_values[1][:, i]).mean() for i, feature in enumerate(self.feature_names)}
        sorted_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        for feature, importance in sorted_importance.items():
            mlflow.log_metric(f"{feature}_importance", importance)
        return {"feature_importance": sorted_importance, "top_features": list(sorted_importance.keys())[:5]}

    def plot_shap_summary(self, output_path: str = None):
        plt.figure(figsize=(10, 6))
        shap.summary_plot(self.shap_values[1], feature_names=self.feature_names, show=False)
        if output_path:
            plt.savefig(output_path)
            plt.close()
            mlflow.log_artifact(output_path)
        else:
            plt.show()

# Sample usage within a Databricks environment or locally with Databricks connectivity setup
if __name__ == "__main__":
    mlflow.set_experiment("/my-experiment")
    actual_data = pd.DataFrame({
        'id': [1, 2, 3, 6],
        'value': ['A', 'B', 'C', 'F'],
        'score': [0.9, 0.8, 0.7, 0.5],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-06']
    })
    expected_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'value': ['A', 'B', 'C', 'D', 'E'],
        'score': [0.9, 0.8, 0.7, 0.6, 0.5],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
    })
    analyzer = DQRootCauseAnalyzer()
    analyzer.fit(actual_data, expected_data, 'id', ['value', 'score', 'date'])
    impact_results = analyzer.analyze_global_impact()
    print("Global feature importance:", impact_results)
