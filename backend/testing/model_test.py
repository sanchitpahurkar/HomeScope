# this is a testing file for the trained model. This file is to be used to directly test the model on specific inputs explicitly.

import joblib
import numpy as np

# Load model and preprocessing tools
model = joblib.load("housing_india_model.pkl")
X_scaler = joblib.load("X_scaler.pkl")
y_scaler = joblib.load("y_scaler.pkl")

sample_data = np.array([[
    2500,
    7700,
    4,
    1,
    3,
    4
]])

# Scale the features using X_scaler
sample_data_scaled = X_scaler.transform(sample_data)

# Get the model prediction
predicted_price_scaled = model.predict(sample_data_scaled)

# Inverse transform the prediction using y_scaler
predicted_price = y_scaler.inverse_transform(predicted_price_scaled.reshape(-1, 1))

# Print the predicted price
print(f"Predicted Price: ₹{predicted_price[0][0]:.2f}")