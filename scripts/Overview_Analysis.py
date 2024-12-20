import pandas as pd

# Define data loader class
class overview:
    def __init__(self, file_path):
        # Initialize the Folder path of the data
        self.df = file_path

    def identify_top10_handsets(self, column_name="Handset Type", top_n=10):
        
        # Check if the column exists in the dataset
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return None
        
        # Count the frequency of each handset type
        handset_counts = self.df[column_name].value_counts().head(top_n)
        
        # Convert to DataFrame for better readability
        top_handsets = handset_counts.reset_index()
        top_handsets.columns = [column_name, "Count"]
        
        print(f"\nTop {10} Handsets Used by Customers:")
        
        return top_handsets

    def top3_manufacturers(self, column_name="Handset Type", top_n=3):
        # Identify the top N handset manufacturers based on frequency.

        # Check if the column exists in the dataset
        if column_name not in self.df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return None
        
        # Extract the manufacturer name (assumes it's the first word in the handset name)
        self.df['Manufacturer'] = self.df[column_name].str.split().str[0]
        
        # Count the frequency of each manufacturer
        manufacturer_counts = self.df['Manufacturer'].value_counts().head(top_n)
        
        # Convert to DataFrame for better readability
        top_manufacturers = manufacturer_counts.reset_index()
        top_manufacturers.columns = ['Manufacturer', 'Count']
        
        print(f"\nTop {3} Handset Manufacturers:")
        
        return top_manufacturers

    def top5_handsets_pertop3_manufacturer1(self, column_name="Handset Type", top_manufacturers=3, top_handsets=5):
        # Extract the manufacturer name (assumes it's the first word in the handset name)
        self.df['Manufacturer'] = self.df[column_name].str.split().str[0]

        # Identify the top 3 manufacturers
        top_manufacturers = self.df['Manufacturer'].value_counts().head(top_manufacturers).index

        # Dictionary to store top handsets for each manufacturer
        top_handsets = {}

        for manufacturer in top_manufacturers:
            # Filter data for the current manufacturer
            manufacturer_data = self.df[self.df['Manufacturer'] == manufacturer]
            
            # Count handset usage and get the top N handsets
            handset_counts = manufacturer_data[column_name].value_counts().head(top_handsets)
            
            # Convert to DataFrame for better readability
            top_handsets[manufacturer] = handset_counts.reset_index()
            top_handsets[manufacturer].columns = ['Handset', 'Count']

        for manufacturer, handsets in top_handsets.items():
            print(f"\nTop {top_handsets} Handsets for {manufacturer}:")
            print(handsets)
        return top_handsets
    
    def top5_handsets_pertop3_manufactu(self):

            # Check if data is loaded successfully
        top_manufacturers = None
        if not self.df.empty:
            # Identify the top 3 manufacturers
            top_manufacturers = (self.df.groupby("Handset Manufacturer")
                                    .size()
                                    .reset_index(name="Count")
                                    .sort_values(by="Count", ascending=False)
                                    .head(3)["Handset Manufacturer"]
                                    .tolist())
            
        print("Top 3 Handset Manufacturers:", top_manufacturers)

        # Filter data for the top 3 manufacturers
        filtered_data = self.df[self.df["Handset Manufacturer"].isin(top_manufacturers)]

        # Identify top 5 handsets for each manufacturer
        top_handsets_per_manufacturer = (
            filtered_data.groupby(["Handset Manufacturer", "Handset Type"])
            .size()
            .reset_index(name="Count")
            .sort_values(["Handset Manufacturer", "Count"], ascending=[True, False])
            .groupby("Handset Manufacturer")
            .head(5)
        )
        print("Top 5 Handsets per Top 3 Handset Manufacturers:")
        return top_handsets_per_manufacturer

    def xdr_sessions1(self):
        # Check if data is loaded successfully
        xDR_sessions = None
        if not self.df.empty:
            # Aggregate data to count the number of xDR sessions per user
            xDR_sessions = (self.df.groupby("IMSI")
                                .agg(Number_of_xDR_Sessions=("Bearer Id", "nunique"))
                                .reset_index()
                                .sort_values(by="Number_of_xDR_Sessions", ascending=False))
            return xDR_sessions

    def session_duration(self):
        # Convert duration from milliseconds to seconds
        self.df["Duration (seconds)"] = self.df["Dur. (ms)"] / 1000

        # Group by IMSI and aggregate data
        sesion_dur_agg = self.df.groupby("IMSI").agg(
            Total_UL=("Total UL (Bytes)", "sum"),
            Total_DL=("Total DL (Bytes)", "sum"),
            Total_Duration=("Duration (seconds)", "sum")
        ).reset_index()

        # Add a new column for session duration in hours (optional)
        sesion_dur_agg["Session Duration (hours)"] = sesion_dur_agg["Total_Duration"] / 3600

        sesion_dur_agg.sort_values(by = 'Session Duration (hours)', ascending=False).head(10)
        return sesion_dur_agg
    '''
    def xdr_sessions(self):
        # Aggregates the number of xDR sessions and their total duration per user for specific applications.

        # Calculate session duration in seconds
        self.df['Start Time'] = pd.to_datetime(self.df['Start']) + pd.to_timedelta(self.df['Start ms'], unit='ms')
        self.df['End Time'] = pd.to_datetime(self.df['End']) + pd.to_timedelta(self.df['End ms'], unit='ms')
        self.df['Session Duration (s)'] = (self.df['End Time'] - self.df['Start Time']).dt.total_seconds()

        # Select relevant columns for aggregation
        aggregation_columns = [
            'MSISDN/Number',  # User identifier
            'Session Duration (s)',
            'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)'
        ]

        # Filter the dataset to include only the necessary columns
        filtered_data = self.df[aggregation_columns]

        # Replace usage data with session counts (if any usage > 0, count as a session)
        session_columns = aggregation_columns[2:]
        filtered_data[session_columns] = filtered_data[session_columns].applymap(lambda x: 1 if x > 0 else 0)

        # Aggregate the session counts and total duration per user
        aggregated_data = filtered_data.groupby('MSISDN/Number').agg({
            'Session Duration (s)': 'sum',
            'Youtube DL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum'
        }).reset_index()

        return aggregated_data '''

    def total_DL_UP(self):
        # Group by user column (e.g., IMSI or MSISDN/Number)
        user_column = "IMSI"
        grouped = self.df.groupby(user_column)

        # Aggregate required metrics
        aggregated_data = grouped.agg(
            number_of_sessions=('Bearer Id', 'count'),  # Count xDR sessions
            total_session_duration=('Dur. (ms)', 'sum'),  # Sum session durations
            total_download=('Total DL (Bytes)', 'sum'),  # Total DL data
            total_upload=('Total UL (Bytes)', 'sum'),  # Total UL data
            youtube_dl=('Youtube DL (Bytes)', 'sum'),  # YouTube DL data
            youtube_ul=('Youtube UL (Bytes)', 'sum'),  # YouTube UL data
            netflix_dl=('Netflix DL (Bytes)', 'sum'),  # Netflix DL data
            netflix_ul=('Netflix UL (Bytes)', 'sum'),  # Netflix UL data
            gaming_dl=('Gaming DL (Bytes)', 'sum'),  # Gaming DL data
            gaming_ul=('Gaming UL (Bytes)', 'sum'),  # Gaming UL data
            other_dl=('Other DL (Bytes)', 'sum'),  # Other DL data
            other_ul=('Other UL (Bytes)', 'sum')  # Other UL data
        ).reset_index()
        # Suppress scientific notation for the entire DataFrame
        pd.set_option('display.float_format', '{:.0f}'.format)
        # Save or display the aggregated data
        aggregated_data.sort_values(by = 'number_of_sessions', ascending=False).head(10)
        # aggregated_data.to_csv("aggregated_user_data.csv", index=False)
        return aggregated_data
    
    def total_DL_UP_app(self):
            # Aggregate data by IMSI
        aggregated_data = self.df.groupby('IMSI').agg({
            'Youtube DL (Bytes)': 'sum',
            'Youtube UL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Netflix UL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Gaming UL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum',
            'Other UL (Bytes)': 'sum',
        }).reset_index()

        # Calculate the total data volume for each application (Download + Upload)
        aggregated_data['Total Youtube (Bytes) DL_UL'] = aggregated_data['Youtube DL (Bytes)'] + aggregated_data['Youtube UL (Bytes)']
        aggregated_data['Total Netflix (Bytes) DL_UL'] = aggregated_data['Netflix DL (Bytes)'] + aggregated_data['Netflix UL (Bytes)']
        aggregated_data['Total Gaming (Bytes) DL_UL'] = aggregated_data['Gaming DL (Bytes)'] + aggregated_data['Gaming UL (Bytes)']
        aggregated_data['Total Other (Bytes) DL_UL'] = aggregated_data['Other DL (Bytes)'] + aggregated_data['Other UL (Bytes)']

        # Optionally, you can drop individual columns if you only want total per application
        aggregated_data = aggregated_data[['IMSI', 'Total Youtube (Bytes) DL_UL', 'Total Netflix (Bytes) DL_UL', 
                                        'Total Gaming (Bytes) DL_UL', 'Total Other (Bytes) DL_UL']]

        # Display the result
        return aggregated_data.head(50)