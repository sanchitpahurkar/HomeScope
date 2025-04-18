from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pickle
from babel.numbers import format_currency
import requests
import os

app = Flask(__name__)
CORS(app)

# Load model and preprocessing tools
MODEL_URL = "https://huggingface.co/sanchitpahurkar/HomeScope/resolve/main/housing_india_model.pkl"
MODEL_PATH = "backend/housing_india_model.pkl"

# Download the model if not already present
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
    print("Download complete.")

# Load the model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open("city_encoder.pkl", "rb") as f:
    city_encoder = pickle.load(f)

with open("X_scaler.pkl", "rb") as f:
    X_scaler = pickle.load(f)

with open("y_scaler.pkl", "rb") as f:
    y_scaler = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    print(data)

    try:
        # Encode city
        city_name = data["City"]
        city_encoded = city_encoder.transform([city_name])[0]

        # Create feature array
        features = np.array([[
            float(data["Total_Area"]),
            float(data["Price_per_SQFT"]),
            float(data["Baths"]),
            float(data["Balcony"]),
            city_encoded,
            float(data["BHK"])
        ]])

        # Scale features
        scaled_features = X_scaler.transform(features)

        # Predict (scaled)
        scaled_prediction = model.predict(scaled_features)

        # Inverse transform to get actual price
        actual_price = y_scaler.inverse_transform(scaled_prediction.reshape(-1, 1))[0][0]
        
        formatted_price = format_currency(actual_price, 'INR', locale='en_IN')

        return jsonify({"predicted_price": formatted_price}) 

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
