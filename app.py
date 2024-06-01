from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Process the data and generate recommendations
    recommendations = generate_recommendations(df)

    return jsonify(recommendations)

def generate_recommendations(df):
    # Implement your logic to analyze data and generate recommendations
    recommendations = {
        "total_impressions": df["Impressions"].sum(),
        "average_ctr": df["Ctr"].mean()
    }
    return recommendations

if __name__ == '__main__':
    app.run(debug=True)

