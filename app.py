import os
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

def load_csv(file_name):
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        return str(e)

@app.route('/analyze/campaign', methods=['GET'])
def analyze_campaign():
    df = load_csv('Campaign_Performance.csv')
    return jsonify(df.head().to_dict())

@app.route('/analyze/keyword', methods=['GET'])
def analyze_keyword():
    df = load_csv('Keyword_Performance.csv')
    return jsonify(df.head().to_dict())

@app.route('/analyze/search_terms', methods=['GET'])
def analyze_search_terms():
    df = load_csv('Search_Terms.csv')
    return jsonify(df.head().to_dict())

@app.route('/analyze/ads', methods=['GET'])
def analyze_ads():
    df = load_csv('Ads_Performance.csv')
    return jsonify(df.head().to_dict())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
