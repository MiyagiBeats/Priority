import os
import requests
import base64
import pandas as pd
from io import StringIO
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_github_file(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_content = response.json().get('content')
        decoded_content = base64.b64decode(file_content).decode('utf-8')
        return decoded_content
    else:
        raise Exception(f"Failed to fetch file: {response.status_code}")

def analyze_file(content):
    df = pd.read_csv(StringIO(content))
    analysis = {
        "summary": df.describe().to_dict(),
        "recommendations": "Modify, remove, or add keywords based on the analysis"
    }
    return analysis

@app.route('/analyze/campaign', methods=['GET'])
def analyze_campaign():
    repo = os.getenv('GITHUB_REPO')
    token = os.getenv('GITHUB_TOKEN')
    path = "data/Campaign_Performance.csv"

    try:
        file_content = fetch_github_file(repo, path, token)
        analysis_result = analyze_file(file_content)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/analyze/keyword', methods=['GET'])
def analyze_keyword():
    repo = os.getenv('GITHUB_REPO')
    token = os.getenv('GITHUB_TOKEN')
    path = "data/Keyword_Performance.csv"

    try:
        file_content = fetch_github_file(repo, path, token)
        analysis_result = analyze_file(file_content)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/analyze/search_terms', methods=['GET'])
def analyze_search_terms():
    repo = os.getenv('GITHUB_REPO')
    token = os.getenv('GITHUB_TOKEN')
    path = "data/Search_Terms.csv"

    try:
        file_content = fetch_github_file(repo, path, token)
        analysis_result = analyze_file(file_content)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/analyze/ads', methods=['GET'])
def analyze_ads():
    repo = os.getenv('GITHUB_REPO')
    token = os.getenv('GITHUB_TOKEN')
    path = "data/Ads_Performance.csv"

    try:
        file_content = fetch_github_file(repo, path, token)
        analysis_result = analyze_file(file_content)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
