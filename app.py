import os
import pandas as pd
from flask import Flask, jsonify
import logging
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_csv(file_name):
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
        logger.debug(f"Loading CSV file from: {data_path}")
        df = pd.read_csv(data_path, low_memory=False)
        df = df.apply(pd.to_numeric, errors='ignore')
        return df
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV file: {e}")
        return str(e)
    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
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
            logger.error(f"Error processing row in analyze_campaign_performance: {e}")
    return recommendations

def analyze_keyword_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            cpc = float(row['Avg. CPC']) if isinstance(row['Avg. CPC'], str) else row['Avg. CPC']
            if cpc > 1.0:
                recommendations.append({
                    "keyword": row['Search keyword'],
                    "action": "reduce CPC or remove"
                })
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing row in analyze_keyword_performance: {e}")
    return recommendations

def analyze_search_terms(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            ctr = float(row['CTR'].strip('%')) if isinstance(row['CTR'], str) else row['CTR']
            if row['Conversions'] == 0 and row['Clicks'] > 50:
                recommendations.append({
                    "search_term": row['Search term'],
                    "action": "add as negative keyword"
                })
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing row in analyze_search_terms: {e}")
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
            logger.error(f"Error processing row in analyze_ads_performance: {e}")
    return recommendations

def analyze_audience_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        try:
            cost_per_conversion = float(row.get('Cost per Conversion', 0))
            if cost_per_conversion > 10:
                recommendations.append({
                    "audience": row['Audience segment'],
                    "action": "review audience targeting or exclude"
                })
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing row in analyze_audience_performance: {e}")
    return recommendations

def get_google_ads_client():
    return GoogleAdsClient.load_from_storage()

@app.route('/analyze/campaign', methods=['GET'])
def analyze_campaign():
    df = load_csv('Campaign_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_campaign_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/keyword', methods=['GET'])
def analyze_keyword():
    df = load_csv('Keyword_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_keyword_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/search_terms', methods=['GET'])
def analyze_search_terms():
    df = load_csv('Search_Terms.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_search_terms(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/ads', methods=['GET'])
def analyze_ads():
    df = load_csv('Ads_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_ads_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/audience', methods=['GET'])
def analyze_audience():
    df = load_csv('Audiences.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_audience_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
