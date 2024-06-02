import pandas as pd
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Function to remove commas from numerical values
def remove_commas(x):
    if isinstance(x, str):
        return x.replace(',', '')
    return x

# Function to remove percentage signs and convert to float
def remove_percentage(x):
    if isinstance(x, str) and '%' in x:
        return float(x.replace('%', ''))
    return x

# List of files and their specific columns to clean
files_to_clean = {
    'Campaign_Performance.csv': ['Clicks', 'Impr.', 'CTR', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conv. rate'],
    'Keyword_Performance.csv': ['Clicks', 'Impressions', 'CTR', 'Avg. CPC'],
    'Search_Terms.csv': ['Clicks', 'Impressions', 'CTR', 'Avg. CPC'],
    'Ads_Performance.csv': ['Clicks', 'Impr.', 'CTR', 'Impr. (Abs. Top) %', 'Impr. (Top) %'],
    'Audiences.csv': ['Clicks', 'Impr.', 'CTR', 'Cost per Conversion']
}

data_dir = os.path.join(os.path.dirname(__file__), 'data')

for file_name, columns in files_to_clean.items():
    file_path = os.path.join(data_dir, file_name)
    logging.info(f"Cleaning {file_path}...")
    df = pd.read_csv(file_path)
    
    # Add missing columns with NaN values
    for column in columns:
        if column not in df.columns:
            logging.warning(f"Column '{column}' not found in {file_name}. Adding this column with NaN values.")
            df[column] = float('nan')
    
    # Clean the columns
    for column in columns:
        if 'CTR' in column or 'Impr. (Abs. Top) %' in column or 'Impr. (Top) %' in column or 'Conv. rate' in column or 'Cost per Conversion' in column:
            df[column] = df[column].apply(remove_percentage).astype(float)
        else:
            df[column] = df[column].apply(remove_commas).astype(float)
    
    df.to_csv(file_path, index=False)
    logging.info(f"Cleaned data saved to {file_path}")
