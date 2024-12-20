import pandas as pd

# Define data loader class
class EDA:
    def __init__(self, file_path):
        # Initialize the Folder path of the data
        self.df = file_path

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
        return decile_group
    
   