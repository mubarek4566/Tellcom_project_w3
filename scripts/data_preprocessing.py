# Loading Neccessary Libraries
import pandas as pd
import matplotlib.pyplot as plt
import math

class preprocess:
    def __init__(self, dataframe):
        """
        Initializes the SentimentEDA class with the merged dataframe.
        """
        self.df = dataframe

    def nu_statistical_summary(self):
        
        # Perform a statistical summary of the dataset.

        summary = {}
        
        # Numerical columns summary
        numerical_summary = self.df.describe().T  
        #numerical_summary['missing_values'] = self.df.isnull().sum()  # Count of missing values
        summary['Numerical Summary'] = numerical_summary

        return summary
    
    def ca_statistical_summary(self):
        # Categorical columns summary
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        categorical_summary = {}
        Catego_Summary = []
        for column in categorical_columns:
            categorical_summary[column] = {
                'unique_values': self.df[column].nunique(),
                'most_frequent': self.df[column].mode()[0] if not self.df[column].mode().empty else None,
                'missing_values': self.df[column].isnull().sum()
            }
        Catego_Summary = pd.DataFrame(categorical_summary).T

        # Print summaries
        #print("\nNumerical Columns Summary:")
        #print(summary['Numerical Summary'])
        
        #print("\nCategorical Columns Summary:")
        #print(summary['Categorical Summary'])
        
        return Catego_Summary

    def missingvalues(self):
        # Handling Missing Values
        # Step 1: Check for missing values
        missing_values = self.df.isnull().sum()
        missing_percentage = (missing_values / len(self.df)) * 100

        print("Missing Values and Percentage:")
        print(pd.DataFrame({'Missing Values': missing_values, 'Percentage (%)': missing_percentage}))
  
            
    def check_duplicates(self, drop_duplicates=False):
        #Check for duplicate rows in the dataset and optionally remove them.

        # Check for duplicates
        duplicate_count = self.df.duplicated().sum()
        print(f"Number of duplicate rows: {duplicate_count}")
        
        if drop_duplicates:
            self.df = self.df.drop_duplicates()
            print(f"Duplicates have been removed. Remaining rows: {len(self.df)}")
        
        return duplicate_count, self.df
    
    def plot_histograms(self, bins=30):
        # Plot histograms for all numerical columns in the dataset.

        # Select only numerical columns
        numerical_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        
        # Loop through each numerical column
        for col in numerical_columns:
            plt.figure(figsize=(8, 4))
            plt.hist(self.df[col].dropna(), bins=bins, alpha=0.7, color='blue', edgecolor='black')
            plt.title(f'Histogram for {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()

    def plot_histograms_in_grid(self, bins=30, columns=3):
        # Plot histograms for all numerical columns in the dataset in a grid layout.

        # Select only numerical columns
        numerical_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        num_vars = len(numerical_columns)
        
        # Calculate the number of rows needed
        rows = math.ceil(num_vars / columns)
        
        # Create a grid of subplots
        fig, axes = plt.subplots(rows, columns, figsize=(columns * 5, rows * 4))
        axes = axes.flatten()  # Flatten the axes array for easy indexing
        
        for i, col in enumerate(numerical_columns):
            axes[i].hist(self.df[col].dropna(), bins=bins, alpha=0.7, color='blue', edgecolor='black')
            axes[i].set_title(f'Histogram for {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
            axes[i].grid(axis='y', linestyle='--', alpha=0.7)
        
        # Hide any unused subplots
        for j in range(len(numerical_columns), len(axes)):
            axes[j].set_visible(False)
        
        # Adjust layout
        plt.tight_layout()
        plt.show()


    def detect_outliers(self, handle_outliers=False):
        #Detect and optionally handle outliers in numerical fields using the IQR method.

        numerical_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        outlier_summary = {}

        for column in numerical_columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Detect outliers
            outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
            outlier_count = outliers.shape[0]
            outlier_summary[column] = {
                "Lower Bound": lower_bound,
                "Upper Bound": upper_bound,
                "Outlier Count": outlier_count
            }

            # Handle outliers if specified
            if handle_outliers:
                self.df.loc[self.df[column] < lower_bound, column] = lower_bound
                self.df.loc[self.df[column] > upper_bound, column] = upper_bound

        print("\nOutlier Summary (using IQR method):")
        for col, stats in outlier_summary.items():
            print(f"{col}: {stats}")

        if handle_outliers:
            print("\nOutliers have been handled (clipped to bounds).")

        return outlier_summary, self.df


    