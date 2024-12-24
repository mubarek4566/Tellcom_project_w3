import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# from scripts.connection import Db_Connection  # Corrected import path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from db_connection import Db_Connection  

# Function to create bar plot
def create_bar_plot(data, column, title):
    top_values = data[column].value_counts().nlargest(20)
    fig, ax = plt.subplots()
    top_values.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel(column)
    st.pyplot(fig)

# App layout
st.title("User Data Analysis")


menu = st.sidebar.selectbox(
    "Select Analysis",
    ["User Overview Analysis", "User Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"]
)

# Database connection details
st.sidebar.header("Database Configuration")
db_connection = Db_Connection()

# Define table names for each menu item
table_mapping = {
    "User Overview Analysis": "xdr_data",
    "User Engagement Analysis": "user_engagement",
    "Experience Analysis": "user_experience",
    "Satisfaction Analysis": "user_satisfaction"
}

# Fetch data when user clicks the button
if st.sidebar.button("Load Data and Visualize"):
    # Get the appropriate table name for the selected analysis
    table_name = table_mapping.get(menu)
    
    if table_name:
        # Fetch data from the selected table using the Db_Connection class
        data = db_connection.read_data(table_name)
        
        if not data.empty:
            st.write("Data Loaded Successfully!")
            st.write(data.head())
            
            # Customize column name based on analysis type
            if menu == "User Overview Analysis":
                column = "Bearer Id"  # Replace with the actual column name for the analysis
                title = "Top 20 User Overview Values"
            
            elif menu == "User Engagement Analysis":
                column = "Gaming_Traffic"  # Replace with the actual column name for the analysis
                title = "Top 20 User Engagement Values"
            
            elif menu == "Experience Analysis":
                column = "Average UL Throughput"  # Replace with the actual column name for the analysis
                title = "Top 20 Experience Level Values"
            
            elif menu == "Satisfaction Analysis":
                column = "satisfaction_score"  # Replace with the actual column name for the analysis
                title = "Top 20 Satisfaction Values"
            
            # Generate the bar plot
            create_bar_plot(data, column, title)
        else:
            st.error("Failed to load data.")
    else:
        st.error("Invalid table selection.")