from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
import pg8000  # Import the pg8000 library for PostgreSQL connection

load_dotenv()  # Load environment variables from .env file

class Db_Connection:
    def __init__(self):
        """
        Initializes the connection parameters and establishes a database connection.
        """
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "telecom")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "Bismilah")
        self.connection = None  # Initialize the connection attribute

        # Automatically connect to the database during initialization
        self.initialize_connection()

    # Establishes a connection to the PostgreSQL database using pg8000.
    def initialize_connection(self):
        try:
            # Use pg8000 directly for connection
            self.connection = pg8000.connect(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port
            )

            # Test the connection by executing a simple SQL query
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")  # Test query
            result = cursor.fetchone()
            if result:
                print("Database connection initialized successfully!")
            else:
                print("Failed to establish connection.")
            cursor.close()  # Close the cursor after test query

        except Exception as e:
            print(f"Error initializing database connection: {e}")
            self.connection = None

    def get_connection(self):
        """
        Returns the active pg8000 connection.
        """
        return self.connection

    def close_connection(self):
        """
        Closes the database connection if it exists.
        """
        if self.connection:
            self.connection.close()  # Close the connection
            print("Database connection closed.")

    def read_data(self, table_name):
       # Reads all rows from the specified table and converts it into a pandas DataFrame.
        try:
            if self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Create a cursor to fetch data
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")  # Query to fetch data
            rows = cursor.fetchall()

            # Convert rows into a DataFrame and get column names
            columns = [desc[0] for desc in cursor.description]  # Get column names
            df = pd.DataFrame(rows, columns=columns)

            cursor.close()  

            return df  # Return the DataFrame
        except Exception as e:
            print(f"Error reading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def insert_cleaned_data(self, data, table_name="cleaned_telecom"):
        # Inserts new data into the specified table.

        try:
            if self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Create a cursor for the insertion
            cursor = self.connection.cursor()

            # Build the query dynamically
            for _, row in data.iterrows():
                columns = ', '.join(row.index)
                placeholders = ', '.join(['%s'] * len(row))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(row.values))

            self.connection.commit()  # Commit the transaction
            cursor.close()  # Close the cursor after insertion
            print(f"Data successfully inserted into {table_name}.")

        except Exception as e:
            print(f"Error inserting data: {e}")