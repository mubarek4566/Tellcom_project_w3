import pandas as pd
import matplotlib.pyplot as plt


# Define data loader class
class EDA:
    def __init__(self, file_path):
        # Initialize the Folder path of the data
        self.df = file_path

    def fill_null_by_imsi_group(self: pd.DataFrame):
        # Replace null values in 'MSISDN/Number' and 'IMEI' columns with values from the same IMSI group.

        if 'IMSI' in self.df.columns:
            print("Filling missing 'MSISDN/Number' and 'IMEI' by IMSI group...")
            
            # Fill missing 'MSISDN/Number' using the same IMSI group
            self.df['MSISDN/Number'] = self.df.groupby('IMSI')['MSISDN/Number'].transform(lambda x: x.fillna(method='pad'))

            # Fill missing 'IMEI' using the same IMSI group
            self.df['IMEI'] = self.df.groupby('IMSI')['IMEI'].transform(lambda x: x.fillna(method='pad'))
        else:
            print("IMSI column is missing from the DataFrame, unable to fill null values.")
        return self.df
    
    def distribution_of_missing_values(self, column_names):
        """
        Plot the distribution of missing values for the specified columns.
        """
        # Check for missing values in the specified columns
        null_columns = self.file_path[column_names]
        constant_values = (null_columns.isnull().sum())

        # Calculate percentages
        total = constant_values.sum()
        percentages = (constant_values / total) * 100 if total > 0 else [0] * len(constant_values)

        # Bar plot for constant/zero values
        ax = constant_values.plot(kind='barh', figsize=(10, 8), color='orange')

        # Add number and percentage annotations
        for bar, percentage in zip(ax.patches, percentages):
            width = bar.get_width()
            y = bar.get_y() + bar.get_height() / 2
            annotation = f'{int(width)} ({percentage:.2f}%)'
            ax.annotate(annotation, xy=(width, y), xytext=(5, 0),
                        textcoords="offset points", ha='left', va='center')

        # Add labels and title
        plt.title("Distribution of Missing Values Per Column")
        plt.xlabel("Frequency")
        plt.ylabel("Columns")
        plt.xticks(rotation=45)
        plt.show()

    def segment(self):
        # 1. Aggregate data by IMSI for total duration and data usage
        aggregated_data = self.df.groupby('IMSI').agg({
            'Dur. (ms)': 'sum',
            'Youtube DL (Bytes)': 'sum',
            'Youtube UL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Netflix UL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Gaming UL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum',
            'Other UL (Bytes)': 'sum',
        }).reset_index()

        # 2. Calculate the total data volume (Download + Upload) for each application
        aggregated_data['Total Youtube (Bytes)'] = aggregated_data['Youtube DL (Bytes)'] + aggregated_data['Youtube UL (Bytes)']
        aggregated_data['Total Netflix (Bytes)'] = aggregated_data['Netflix DL (Bytes)'] + aggregated_data['Netflix UL (Bytes)']
        aggregated_data['Total Gaming (Bytes)'] = aggregated_data['Gaming DL (Bytes)'] + aggregated_data['Gaming UL (Bytes)']
        aggregated_data['Total Other (Bytes)'] = aggregated_data['Other DL (Bytes)'] + aggregated_data['Other UL (Bytes)']

        # 3. Calculate the total data volume across all applications
        aggregated_data['Total Data (Bytes)'] = aggregated_data[['Total Youtube (Bytes)', 'Total Netflix (Bytes)', 'Total Gaming (Bytes)', 'Total Other (Bytes)']].sum(axis=1)

        # 4. Segment users into decile classes based on total session duration
        aggregated_data['Decile'] = pd.qcut(aggregated_data['Dur. (ms)'], 10, labels=False) + 1  # Labels from 1 to 10 for deciles

        # 5. Compute total data (DL + UL) per decile class
        decile_group = aggregated_data.groupby('Decile').agg({
            'Total Data (Bytes)': 'sum',
            'Total Youtube (Bytes)': 'sum',
            'Total Netflix (Bytes)': 'sum',
            'Total Gaming (Bytes)': 'sum',
            'Total Other (Bytes)': 'sum',
        }).reset_index()

        # Display the result
        return decile_group, aggregated_data
    
   