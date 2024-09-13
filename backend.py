from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder

app = Flask(__name__)

model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')

categorical_features = ['Customer_Segment', 'Subscription_Tier']
numerical_features = ['Spending_History', 'Num_Products_Bought', 'Avg_Price_Products', 'Frequency_Purchases']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = pd.DataFrame([data])
    encoded_features = encoder.transform(input_data[categorical_features])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
    input_data = pd.concat([input_data[numerical_features], encoded_df], axis=1)
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])
    prediction = model.predict_proba(input_data)[0, 1] * 100
    return jsonify({'upgrade_probability': prediction})

if __name__ == '__main__':
    app.run(debug=True)
