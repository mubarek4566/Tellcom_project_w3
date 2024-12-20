# import Python libraries
import pandas as pd
import os
from path import get_path
from path import get_path2

# Define data loader class
class CSVData:
    def __init__(self, file_path):
        # Initialize the Folder path of the data
        self.folder_path = file_path
    
        
    def load_description(self):
        # Use pandas to read the file
        return pd.read_excel(self.folder_path, engine='openpyxl')  


    def load_csv_file(self):
        """
        Function to load a CSV file using the path returned by get_csv_path().
        """
        csv_path = get_path()
        try:
            data = pd.read_csv(csv_path)
            return data
        except FileNotFoundError:
            print(f"Error: File not found at {csv_path}. Please check the path.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return csv_path
    '''
    def load_description(self):
        """
        Function to load a excel file using the path returned by get_csv_path().
        """
        description_path = get_path2()
        try:
            data = pd.read_excel(description_path, engine='openpyxl')
            return data
        except FileNotFoundError:
            print(f"Error: File not found at {description_path}. Please check the path.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return description_path


'''