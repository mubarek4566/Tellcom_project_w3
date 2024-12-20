import pandas as pd 
import os 

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

