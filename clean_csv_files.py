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
    'Campaign_Performance.csv': ['Campaign', 'Campaign state', 'Campaign type', 'Clicks', 'Impr.', 'CTR', 'Currency code', 
                                 'Avg. CPC', 'Cost', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 
                                 'Cost / conv.', 'Conv. rate'],
    'Keyword_Performance.csv': ['Search keyword', 'Search keyword status', 'Search keyword status reasons', 'Search keyword match type',
                                'Campaign', 'Ad group', 'Currency code', 'Keyword max CPC', 'Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 
                                'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 'Cost / conv.', 'Conv. rate', 
                                'Avg. CPM', 'Impressions'],
    'Search_Terms.csv': ['Search term', 'Search terms match type', 'Added/Excluded', 'Clicks', 'Impr.', 'CTR', 'Currency code', 
                         'Avg. CPC', 'Cost', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 'Cost / conv.', 
                         'Conv. rate', 'Impressions'],
    'Ads_Performance.csv': ['Ad state', 'Ad type', 'Final URL', 'Beacon URLs', 'Long headline', 'Headline 1', 'Headline 1 position', 
                            'Headline 2', 'Headline 2 position', 'Headline 3', 'Headline 3 position', 'Headline 4', 'Headline 4 position', 
                            'Headline 5', 'Headline 5 position', 'Headline 6', 'Headline 6 position', 'Headline 7', 'Headline 7 position', 
                            'Headline 8', 'Headline 8 position', 'Headline 9', 'Headline 9 position', 'Headline 10', 'Headline 10 position', 
                            'Headline 11', 'Headline 11 position', 'Headline 12', 'Headline 12 position', 'Headline 13', 'Headline 13 position', 
                            'Headline 14', 'Headline 14 position', 'Headline 15', 'Headline 15 position', 'Description', 'Description 1', 
                            'Description 1 position', 'Description 2', 'Description 2 position', 'Description 3', 'Description 3 position', 
                            'Description 4', 'Description 4 position', 'Description 5', 'Image ID', 'Square image ID', 'Logo ID', 'Landscape logo ID', 
                            'Business name', 'Call to action text', 'Video ID', 'Accent color', 'Main color', 'Allow flexible color', 
                            'Ad format preference', 'Promotion text', 'Price prefix', 'Enable Asset Enhancements', 'Enable Autogen Video', 'Path 1', 
                            'Path 2', 'Auto-applied ad suggestion', 'Mobile final URL', 'Tracking template', 'Final URL suffix', 'Custom parameter', 
                            'Campaign', 'Ad group', 'Campaign type', 'Campaign subtype', 'Ad final URL', 'Clicks', 'Impr.', 'CTR', 'Currency code', 
                            'Avg. CPC', 'Cost', 'Conversions', 'View-through conv.', 'Cost / conv.', 'Conv. rate', 'Impr. (Abs. Top) %', 'Impr. (Top) %'],
    'Audiences.csv': ['Audience segment', 'Audience segment state', 'Campaign', 'Ad group', 'Currency code', 'Ad group default max. CPC', 
                      'Audience segment max CPC', 'Audience Segment Bid adj.', 'Targeting Setting', 'Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 
                      'Avg. CPM', 'Cost per Conversion']
}

# Function to determine if a column should be processed for numerical conversion
def is_numeric_column(column_name):
    numeric_keywords = ['Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 
                        'Conversions', 'View-through conv.', 'Cost / conv.', 'Conv. rate', 'Avg. CPM', 'Cost per Conversion']
    return any(keyword in column_name for keyword in numeric_keywords)

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
        elif is_numeric_column(column):
            df[column] = df[column].apply(remove_commas).astype(float)
    
    df.to_csv(file_path, index=False)
    logging.info(f"Cleaned data saved to {file_path}")
