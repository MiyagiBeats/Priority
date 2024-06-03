import os
import pandas as pd
from flask import Flask, jsonify
import logging

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

def ensure_columns(df, required_columns):
    for column in required_columns:
        if column not in df.columns:
            df[column] = float('nan')
    return df

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

@app.route('/analyze/campaign', methods=['GET'])
def analyze_campaign():
    required_columns = ['Campaign', 'Campaign state', 'Campaign type', 'Clicks', 'Impr.', 'CTR', 'Currency code', 
                        'Avg. CPC', 'Cost', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 
                        'Cost / conv.', 'Conv. rate']
    df = load_csv('Campaign_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    df = ensure_columns(df, required_columns)
    recommendations = analyze_campaign_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/keyword', methods=['GET'])
def analyze_keyword():
    required_columns = ['Search keyword', 'Search keyword status', 'Search keyword status reasons', 'Search keyword match type',
                        'Campaign', 'Ad group', 'Currency code', 'Keyword max CPC', 'Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 
                        'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 'Cost / conv.', 'Conv. rate', 
                        'Avg. CPM', 'Impressions']
    df = load_csv('Keyword_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    df = ensure_columns(df, required_columns)
    recommendations = analyze_keyword_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/search_terms', methods=['GET'])
def analyze_search_terms():
    required_columns = ['Search term', 'Search terms match type', 'Added/Excluded', 'Clicks', 'Impr.', 'CTR', 'Currency code', 
                        'Avg. CPC', 'Cost', 'Impr. (Abs. Top) %', 'Impr. (Top) %', 'Conversions', 'View-through conv.', 'Cost / conv.', 
                        'Conv. rate', 'Impressions']
    df = load_csv('Search_Terms.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    df = ensure_columns(df, required_columns)
    recommendations = analyze_search_terms(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/ads', methods=['GET'])
def analyze_ads():
    required_columns = ['Ad state', 'Ad type', 'Final URL', 'Beacon URLs', 'Long headline', 'Headline 1', 'Headline 1 position', 
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
                        'Avg. CPC', 'Cost', 'Conversions', 'View-through conv.', 'Cost / conv.', 'Conv. rate', 'Impr. (Abs. Top) %', 'Impr. (Top) %']
    df = load_csv('Ads_Performance.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    df = ensure_columns(df, required_columns)
    recommendations = analyze_ads_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

@app.route('/analyze/audience', methods=['GET'])
def analyze_audience():
    required_columns = ['Audience segment', 'Audience segment state', 'Campaign', 'Ad group', 'Currency code', 'Ad group default max. CPC', 
                        'Audience segment max CPC', 'Audience Segment Bid adj.', 'Targeting Setting', 'Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 
                        'Avg. CPM', 'Cost per Conversion']
    df = load_csv('Audiences.csv')
    if isinstance(df, str):
        return jsonify({"error": df}), 500
    df = ensure_columns(df, required_columns)
    recommendations = analyze_audience_performance(df)
    return jsonify({"data": df.to_dict(), "recommendations": recommendations})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
``
