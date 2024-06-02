import os
import pandas as pd
from flask import Flask, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def load_csv(file_name):
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
        logging.debug(f"Loading CSV file from: {data_path}")
        df = pd.read_csv(data_path, low_memory=False)
        df = df.apply(pd.to_numeric, errors='ignore')
        return df
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing CSV file: {e}")
        return str(e)
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        return str(e)

def analyze_campaign_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            ctr = float(row['CTR'].strip('%')) if isinstance(row['CTR'], str) else row['CTR']
            if ctr < 1.0:
                recommendations.append({
                    "campaign": row['Campaign'],
                    "action": "improve ad relevance or keywords"
                })
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing row: {e}")
    return recommendations

def analyze_keyword_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            cpc = float(row['CPC']) if isinstance(row['CPC'], str) else row['CPC']
            if cpc > 1.0:
                recommendations.append({
                    "keyword": row['Keyword'],
                    "action": "reduce CPC or remove"
                })
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing row: {e}")
    return recommendations

def analyze_search_terms(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            ctr = float(row['CTR'].strip('%')) if isinstance(row['CTR'], str) else row['CTR']
            if row['Conversions'] == 0 and row['Clicks'] > 50:
                recommendations.append({
                    "search_term": row['Search Term'],
                    "action": "add as negative keyword"
                })
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing row: {e}")
    return recommendations

def analyze_ads_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            ctr = float(row['CTR'].strip('%')) if isinstance(row['CTR'], str) else row['CTR']
            if ctr < 1.0:
                recommendations.append({
                    "ad": row['Ad'],
                    "action": "improve ad copy"
                })
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing row: {e}")
    return recommendations

def analyze_audience_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            cost_per_conversion = float(row.get('Cost per Conversion', 0))
            if cost_per_conversion > 10:
                recommendations.append({
                    "audience": row['Audience'],
                    "action": "review audience targeting or exclude"
                })
        except (ValueError, KeyError) as e:
            logging.error(f"Error processing row: {e}")
    return recommendations

@app.route('/analyze/campaign', methods=['GET'])
def analyze_campaign():
    df = load_csv('Campaign_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_campaign_performance(df)
    return jsonify({"data": df.head().to_dict(), "recommendations": recommendations})

@app.route('/analyze/keyword', methods=['GET'])
def analyze_keyword():
    df = load_csv('Keyword_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_keyword_performance(df)
    return jsonify({"data": df.head().to_dict(), "recommendations": recommendations})

@app.route('/analyze/search_terms', methods=['GET'])
def analyze_search_terms():
    df = load_csv('Search_Terms.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_search_terms(df)
    return jsonify({"data": df.head().to_dict(), "recommendations": recommendations})

@app.route('/analyze/ads', methods=['GET'])
def analyze_ads():
    df = load_csv('Ads_Performance.csv')
