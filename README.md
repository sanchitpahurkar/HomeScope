# **HomeScope - House Price Prediction App**

This project is a full-stack application designed to predict house prices based on various features such as location, size, and other parameters. The frontend is built with Vite and Tailwind CSS, while the backend is developed using Flask and serves a machine learning model for predicting house prices.

## Project Overview

### Features

**Frontend:**

- A user-friendly interface built with React.js(Vite) and styled using CSS.

- Allows users to input various house attributes (e.g., number of rooms, baths, city) to predict the price of a house.

**Backend:**

- A Flask API that serves a pre-trained machine learning model (using a regression algorithm) for house price prediction.

- Takes input from the frontend, processes the data, and returns a predicted price.

**Machine Learning Model:**

- The model is trained using historical data with features like house area, number of rooms, city, etc.

- The model is stored in the backend and serves predictions via the Flask API.

## **Technologies Used**

**Frontend:**

- Vite: Fast development environment and bundler for the React.js frontend.

- CSS

**Backend:**

- Flask: A lightweight Python web framework to build the backend API.

- Scikit-learn: For the machine learning model.

- Pandas: For data processing and handling.

- NumPy: For numerical computations.

**Model:**

- Trained machine learning model using regression algorithms Random Forest.

- Optimized the model using hyperparameter tuning and achieveing MAE score of 0.056

## **Installation Instructions**
### **Frontend Setup**

- Clone the frontend repository:
    ```
    git clone <frontend_repo_url>
    cd <frontend_folder>
    ```
- Install dependencies:
    ```
    npm install
    ```
- Start the development server:
    ```
    npm run dev
    ```
    The frontend will be available at http://localhost:3000.

### **Backend Setup**

1. Clone the backend repository:
    ```
    git clone <backend_repo_url>
    cd <backend_folder>
    ```
2. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run the Flask server:
    ```
    python app.py
    ```
    The backend API will be available at http://localhost:5000.

### **Connecting Frontend to Backend**

- The frontend makes HTTP requests to the backend API for price predictions.

- The requests should be sent to http://localhost:5000/predict, with the necessary house data in the request body.

## **Backend + Frontend Testing**
### **Testing the Frontend**

1. Open the app at http://localhost:3000.

2. Input different values for house attributes (e.g., size, number of rooms, city).

3. Click on the "Predict" button.

4. The app should display the predicted house price returned by the backend.

### **Testing the Backend**

1. API Endpoints:

    - POST /predict: This endpoint accepts a JSON object with the house attributes and returns the predicted price.

        Example request:
        ```
        {
            "size": 2000,
            "rooms": 3,
            "city": "Mumbai"
        }
        ```
        Example response:
        ```
        {
            "predicted_price": 12000000
        }
        ```

## **Next Steps**

1. Deploy the backend API on a cloud platform like Render, Heroku, AWS, or Azure.

2. Deploy the frontend on platforms like Vercel or Netlify.

3. Add more advanced features, such as data validation and additional model improvements (e.g., hyperparameter tuning).