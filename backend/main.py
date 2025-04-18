import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import pickle


# loading the dataset
df = pd.read_csv("Real Estate Data V21.csv")

def convert_price_to_number(price_str):
    try:
        if isinstance(price_str, str):
            price_str = price_str.replace("₹", "").strip().lower()
            
            if "cr" in price_str:
                return float(price_str.replace("cr", "").strip()) * 1e7
            elif "l" in price_str:
                return float(price_str.replace("l", "").strip()) * 1e5
            else:
                return None  # unknown unit like "acs", "per sqft", etc.
    except:
        return None
    

def extract_bhk(text) :
    match = re.search(r'(\d+)\s*BHK', str(text), re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None
 
df['Price'] = df['Price'].apply(convert_price_to_number)
df['City'] = df['Location'].apply(lambda x: x.split(',')[-1].strip())
df['BHK'] = df['Property Title'].apply(extract_bhk)

# encoding
# Use separate encoders to avoid overwriting
city_encoder = LabelEncoder()
balcony_encoder = LabelEncoder()

df['City'] = city_encoder.fit_transform(df['City'])
df['Balcony'] = balcony_encoder.fit_transform(df['Balcony'])

# Save only the city encoder (we'll use this in backend)
with open('city_encoder.pkl', 'wb') as f:
    pickle.dump(city_encoder, f)


# handling null values
df['Price'] = df['Price'].fillna(df['Price'].mean())
df['BHK'] = df['BHK'].fillna(-1)

# train and test split
X = df[['Total_Area', 'Price_per_SQFT', 'Baths', 'Balcony', 'City', 'BHK']]
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# normalization
X_scaler = StandardScaler()
y_scaler = StandardScaler()

X_train_scaled = X_scaler.fit_transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

y_train_scaled = y_scaler.fit_transform(y_train.values.reshape(-1,1))
y_test_scaled = y_scaler.transform(y_test.values.reshape(-1,1))

# model 
rf_model = RandomForestRegressor(random_state=42)

# hyperparameter tuning
param_dist = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_depth': [5, 10, 15, 20, 25, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}
random_search = RandomizedSearchCV(
    estimator=rf_model,
    param_distributions=param_dist,
    n_iter=50,  # number of parameter settings sampled
    scoring='neg_mean_absolute_error',
    cv=5,
    verbose=2,
    random_state=42,
    n_jobs=-1  # use all available cores
)

random_search.fit(X_train_scaled, y_train_scaled)


best_model = random_search.best_estimator_

# saving the model with .pkl file
with open('housing_india_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
    
with open("X_scaler.pkl", "wb") as f:
    pickle.dump(X_scaler, f)

with open("y_scaler.pkl", "wb") as f:
    pickle.dump(y_scaler, f)


# metrics evaluation
rfv_pred = best_model.predict(X_test_scaled)
mae = mean_absolute_error(y_test_scaled, rfv_pred)
print("Tuned MAE:", mae)