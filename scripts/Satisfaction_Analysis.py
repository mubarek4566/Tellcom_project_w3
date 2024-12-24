import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# engagements.total_trafic_app()
class UserSatisfaction:
    def satisfaction_computing(self, df_engagement, df_experience):
        # Drop non-numeric columns
        experience_features = df_experience.drop(columns=['msisdn_number', 'Most Common Handset Type'])

        # Define the less engaged cluster (example: first row of engagement data)
        less_engaged_cluster = df_engagement.iloc[0, 1:].values

        # Define the worst experience cluster (example: first row of experience data)
        worst_experience_cluster = experience_features.iloc[0].values

        # Standardizing the data
        scaler_engagement = StandardScaler()
        scaler_experience = StandardScaler()

        engagement_features = df_engagement.iloc[:, 1:]
        scaled_engagement = scaler_engagement.fit_transform(engagement_features)
        scaled_experience = scaler_experience.fit_transform(experience_features)

        # Calculate Engagement Scores
        engagement_scores = [
            euclidean(
                row,
                scaler_engagement.transform(
                    pd.DataFrame([less_engaged_cluster], columns=engagement_features.columns)
                )[0]
            )
            for row in scaled_engagement
        ]

        # Calculate Experience Scores
        experience_scores = [
            euclidean(
                row,
                scaler_experience.transform(
                    pd.DataFrame([worst_experience_cluster], columns=experience_features.columns)
                )[0]
            )
            for row in scaled_experience
        ]

        # Combine results into a DataFrame
        results = pd.DataFrame({
            'MSISDN/Number': df_engagement['msisdn_number'],
            'Engagement Score': engagement_scores,
            'Experience Score': experience_scores
        })

        return results

    def calculate_top_satisfaction(self, results):
        # Calculate the Satisfaction Score
        results['Satisfaction Score'] = (results['Engagement Score'] + results['Experience Score']) / 2

        # Sort by Satisfaction Score in descending order
        top_satisfied_customers = results.sort_values(by='Satisfaction Score', ascending=False)
        return top_satisfied_customers
    
    
    def train_regression_model(self, results):
        # Prepare features (Engagement Score and Experience Score) and target (Satisfaction Score)
        X = results[['Engagement Score', 'Experience Score']]
        y = results['Satisfaction Score']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the regression model
        model = LinearRegression()

        # Train the model on the training data
        model.fit(X_train, y_train)

        # Predict the satisfaction scores on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Print model evaluation metrics
        print("Model Evaluation:")
        print(f"Mean Squared Error (MSE): {mse}")
        print(f"R-squared (R²) Score: {r2}")

        # Optionally, print the predicted vs actual values
        predictions_df = pd.DataFrame({
            'Actual Satisfaction Score': y_test,
            'Predicted Satisfaction Score': y_pred
        })
        return predictions_df
    
    
    def perform_kmeans_clustering(self, results):
        # Prepare the data (combining engagement and experience scores)
        X = results[['Engagement Score', 'Experience Score']]

        # Initialize the KMeans model with k=2
        kmeans = KMeans(n_clusters=2, random_state=42)

        # Fit the model to the data
        results['Cluster'] = kmeans.fit_predict(X)
        return results