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
        if row['Conversions'] < 5 and row['Impressions'] > 1000:
            recommendations.append({
                "campaign": row['Campaign'],
                "action": "review targeting or ad copy to improve conversions"
            })
        if row['CTR'] < 1.0:
            recommendations.append({
                "campaign": row['Campaign'],
                "action": "improve ad relevance or keywords"
            })
    return recommendations

def analyze_keyword_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        if row['CPC'] > 1.0:
            recommendations.append({
                "keyword": row['Keyword'],
                "action": "reduce CPC or remove"
            })
        if row['Impressions'] > 1000 and row['Clicks'] < 50:
            recommendations.append({
                "keyword": row['Keyword'],
                "action": "increase bid"
            })
        if row['Conversions'] > 0 and row['Cost per Conversion'] > 10:
            recommendations.append({
                "keyword": row['Keyword'],
                "action": "optimize landing page or ad copy"
            })
    return recommendations

def analyze_search_terms(df):
    recommendations = []
    for index, row in df.iterrows():
        if row['Conversions'] == 0 and row['Clicks'] > 50:
            recommendations.append({
                "search_term": row['Search Term'],
                "action": "add as negative keyword"
            })
        if row['CTR'] > 2.0 and row['Impressions'] > 500:
            recommendations.append({
                "search_term": row['Search Term'],
                "action": "add as keyword"
            })
    return recommendations

def analyze_ads_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        if row['CTR'] < 1.0:
            recommendations.append({
                "ad": row['Ad'],
                "action": "improve ad copy"
            })
        if row['Conversions'] < 5 and row['Impressions'] > 1000:
            recommendations.append({
                "ad": row['Ad'],
                "action": "A/B test new ad variations"
            })
    return recommendations

def analyze_audience_performance(df):
    recommendations = []
    for index, row in df.iterrows():
        if row['Cost per Conversion'] > 10:
            recommendations.append({
                "audience": row['Audience'],
                "action": "review audience targeting or exclude"
            })
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
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_ads_performance(df)
    return jsonify({"data": df.head().to_dict(), "recommendations": recommendations})

@app.route('/analyze/audience', methods=['GET'])
def analyze_audience():
    df = load_csv('Audiences.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    recommendations = analyze_audience_performance(df)
    return jsonify({"data": df.head().to_dict(), "recommendations": recommendations})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
