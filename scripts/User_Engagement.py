import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score


 # Define data loader class
class engagement():
  
    def __init__(self, dataframe):
        # Initialize the Folder path of the data
        self.data = dataframe
        self.customer_metrics = None  # Initialize a class-level attribute to store customer metrics
        self.trafic_app = None 
        self.normalized_df = None

    def session_freque(self):
        # Calculate session frequency for each IMSI
        session_frequency = self.data.groupby('IMSI').size().reset_index(name='Session Frequency')

        # Calculate session duration (already in Dur. (ms))
        self.data['Session Duration (seconds)'] = self.data['Dur. (ms)'] / 1000

        # Calculate total traffic for each session
        self.data['Total Traffic (Bytes)'] = self.data['Total DL (Bytes)'] + self.data['Total UL (Bytes)']
        # Suppress scientific notation for the entire DataFrame
        pd.set_option('display.float_format', '{:.0f}'.format)
        # Aggregate metrics for each IMSI
        eng_metrics = self.data.groupby('IMSI').agg({
            'Session Duration (seconds)': 'sum',  # Total session duration
            'Total Traffic (Bytes)': 'sum',  # Total traffic
            'Start': 'count'  # Session frequency
        }).rename(columns={'Start': 'Session Frequency'}).reset_index()

        # Display results
        eng_metrics.sort_values(by = 'Session Frequency', ascending=False)

        return eng_metrics

    def metrics_customer(self):
        # Aggregate metrics per customer (MSISDN/Number)
        self.customer_metrics = self.data.groupby('MSISDN/Number').agg({
            'Session Duration (seconds)': 'sum',
            'Total Traffic (Bytes)': 'sum',
            'Bearer Id': 'count'
        }).rename(columns={
            'Session Duration (seconds)': 'Total Session Duration (seconds)',
            'Total Traffic (Bytes)': 'Total Traffic (Bytes)',
            'Bearer Id': 'Session Frequency'
        }).reset_index()
        # Suppress scientific notation for the entire DataFrame
        pd.set_option('display.float_format', '{:.0f}'.format)
        # Top 10 customers per engagement metric
        
        # Top 10 customers per engagement metric
        top_10_duration = self.customer_metrics.nlargest(10, 'Total Session Duration (seconds)')
        top_10_traffic = self.customer_metrics.nlargest(10, 'Total Traffic (Bytes)')
        top_10_frequency = self.customer_metrics.nlargest(10, 'Session Frequency')

        top10_customer = {
            'Top 10 by Duration': top_10_duration,
            'Top 10 by Traffic': top_10_traffic,
            'Top 10 by Frequency': top_10_frequency
        }

        return top10_customer

    def Normalize_clus(self):
        if self.customer_metrics is None:
            raise ValueError("Customer metrics not yet calculated. Please run metrics_customer() first.")

        # Normalize the metrics using MinMaxScaler
        scaler = MinMaxScaler()
        self.normalized_df = scaler.fit_transform(self.customer_metrics[[
            'Total Session Duration (seconds)', 
            'Total Traffic (Bytes)', 
            'Session Frequency'
        ]])
        # Run k-means with k=3
        kmeans = KMeans(n_clusters=3, random_state=42)
        self.customer_metrics['Cluster'] = kmeans.fit_predict(self.normalized_df)

        # Add normalized metrics for reference
        normalized_dat = pd.DataFrame(self.normalized_df, columns=['Normalized Duration', 'Normalized Traffic', 'Normalized Frequency'])
        self.customer_metrics = pd.concat([self.customer_metrics, normalized_dat], axis=1)

        # Return the results
        return self.customer_metrics
    
    def cluster_group(self):
        cluster_stats = self.customer_metrics.groupby('Cluster').agg({
            'Total Session Duration (seconds)': ['min', 'max', 'mean', 'sum'],
            'Total Traffic (Bytes)': ['min', 'max', 'mean', 'sum'],
            'Session Frequency': ['min', 'max', 'mean', 'sum']
        }).reset_index()

        print("Cluster statistics:")
        return cluster_stats
    
    def total_trafic_app(self):
        # Aggregate user total traffic per application
        self.trafic_app = self.data.groupby('MSISDN/Number').agg({
            'Youtube DL (Bytes)': 'sum',
            'Youtube UL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Netflix UL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Gaming UL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum',
            'Other UL (Bytes)': 'sum'
        }).reset_index()

        # Derive the total traffic per application
        self.trafic_app['Youtube Traffic'] = self.trafic_app['Youtube DL (Bytes)'] + self.trafic_app['Youtube UL (Bytes)']
        self.trafic_app['Netflix Traffic'] = self.trafic_app['Netflix DL (Bytes)'] + self.trafic_app['Netflix UL (Bytes)']
        self.trafic_app['Gaming Traffic'] = self.trafic_app['Gaming DL (Bytes)'] + self.trafic_app['Gaming UL (Bytes)']

        # Top 10 most engaged users per application
        top_youtube = self.trafic_app.nlargest(10, 'Youtube Traffic')
        top_netflix = self.trafic_app.nlargest(10, 'Netflix Traffic')
        top_gaming = self.trafic_app.nlargest(10, 'Gaming Traffic')

        top10_trafic_app = {
            'Top 10 by Duration': top_youtube,
            'Top 10 by Traffic': top_netflix,
            'Top 10 by Frequency': top_gaming
        }
        return top10_trafic_app
    
    
    def top3_trafic_app(self):

        # Aggregate total traffic per application
        application_totals = {
            'Youtube': self.trafic_app['Youtube Traffic'].sum(),
            'Netflix': self.trafic_app['Netflix Traffic'].sum(),
            'Gaming': self.trafic_app['Gaming Traffic'].sum()
        }

        # Plot the data
        plt.figure(figsize=(8, 6))
        plt.bar(application_totals.keys(), application_totals.values(), color=['red', 'blue', 'green'])
        plt.title('Top 3 Most Used Applications by Total Traffic')
        plt.ylabel('Total Traffic (Bytes)')
        plt.xlabel('Application')
        plt.show()

    def K_Means_cluster(self):
        # Determine the optimal k values
        inertia = []
        silhouette_scores = []
        K = range(2, 10)  # Test k values from 2 to 9

        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(self.normalized_df)
            inertia.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(self.normalized_df, kmeans.labels_))

        # Plot the elbow curve
        plt.figure(figsize=(10, 5))
        plt.plot(K, inertia, marker='o', label='Inertia')
        plt.title('Elbow Method to Determine Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.legend()
        plt.show()

        # Plot the silhouette scores
        plt.figure(figsize=(10, 5))
        plt.plot(K, silhouette_scores, marker='o', color='orange', label='Silhouette Score')
        plt.title('Silhouette Scores to Evaluate k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.legend()
        plt.show()