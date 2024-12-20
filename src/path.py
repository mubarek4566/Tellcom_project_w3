import pandas as pd 
import os 
#import psycopg2


# Get the current working directory
current_dir = os.getcwd()

# Build the relative path

def get_path():
    # Path to the folder containing CSV files
    file_path = os.path.join(current_dir, '../data/Copy of Week2_challenge_data_source(CSV).csv')  
    return file_path

def get_path2():
    # Path to the folder containing Excel files
    file_path = os.path.join(current_dir, '../data/Field Descriptions.xlsx')  
    return file_path

def new_load(path):
    return path

def connection():

    import psycopg2

    # Database connection parameters
    DB_HOST = "localhost"
    DB_NAME = "telecom"
    DB_USER = "your_username"
    DB_PASSWORD = "your_password"
    DB_PORT = 5432  # Default PostgreSQL port

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Define the query
        query = "SELECT * FROM your_table_name"

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
