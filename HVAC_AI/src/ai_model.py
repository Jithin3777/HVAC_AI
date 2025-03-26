import os
import random
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

MODEL_FILE = "models/hvac_model.pkl"
SCALER_FILE = "models/scaler.pkl"
DATA_FILE = "data/HVAC_data.csv"

# Load or Initialize AI Model:-
if os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE):
    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    print("✅ AI Model Loaded Successfully!")
else:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    scaler = StandardScaler()
    print("⚠️ No existing model found! AI will learn from new data.")


# Load and Prepare Training Data (Updated for New Dataset):-
def load_and_prepare_data():
    """Loads HVAC dataset and prepares it for training."""

    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: Dataset file not found at {DATA_FILE}!")
        return None, None

    print(f"✅ Found dataset: {DATA_FILE}")

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return None, None

    print("✅ Data Loaded Successfully! First 5 Rows:")
    print(df.head())

    # Rename dataset columns to match AI model expectations
    df = df.rename(
        columns={
            "outlet_temp": "temperature",
            "amb_humid_1": "humidity",
            "co2_1": "co2_level",
            "on_off": "occupancy",
            "summer_setpoint_temp": "desired_temperature",
        }
    )

    # Keep only relevant columns
    df = df[
        ["temperature", "humidity", "co2_level", "occupancy", "desired_temperature"]
    ]

    # Drop rows with missing values
    df = df.dropna()

    # Scale the features
    X = df[["temperature", "humidity", "co2_level", "occupancy"]]
    y = df["desired_temperature"]

    X_scaled = scaler.fit_transform(X)  # Normalize inputs
    joblib.dump(scaler, SCALER_FILE)  # Save scaler

    return X_scaled, y


# Train the HVAC AI Model:-
def train_hvac_model():
    """Trains the HVAC AI model using historical data."""
    X, y = load_and_prepare_data()
    if X is None or y is None:
        print("⚠️ Skipping training: No dataset found.")
        return

    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    print("✅ HVAC AI Model Trained and Saved!")


# Predict Optimal Temperature (Ensure Model is Trained):-
def predict_temperature(sensor_data):
    """Predicts the optimal temperature based on sensor data."""

    if not os.path.exists(MODEL_FILE) or not os.path.exists(SCALER_FILE):
        print("⚠️ No trained model found! Training AI model first...")
        train_hvac_model()

    input_features = np.array(
        [
            [
                sensor_data["temperature"],
                sensor_data["humidity"],
                sensor_data["co2_level"],
                sensor_data["occupancy"],
            ]
        ]
    )

    scaler = joblib.load(SCALER_FILE)  # Load the trained scaler
    input_scaled = scaler.transform(input_features)  # Scale input features

    model = joblib.load(MODEL_FILE)  # Load the trained model
    predicted_temp = model.predict(input_scaled)[0]
    return round(predicted_temp, 2)


# Adaptive Learning: Save User Preferences:-
def update_model_with_user_preference(sensor_data, user_temp):
    """Updates the model based on user-set temperature preferences."""
    new_data = pd.DataFrame(
        [
            {
                "temperature": sensor_data["temperature"],
                "humidity": sensor_data["humidity"],
                "co2_level": sensor_data["co2_level"],
                "occupancy": sensor_data["occupancy"],
                "desired_temperature": user_temp,
            }
        ]
    )

    # Append to dataset
    new_data.to_csv(
        DATA_FILE, mode="a", header=not os.path.exists(DATA_FILE), index=False
    )

    # Retrain model with new data
    train_hvac_model()
    print("✅ Model Updated with User Preferences!")


# Test AI Model (Standalone Execution):-
if __name__ == "__main__":
    # Train model if no model exists
    if not os.path.exists(MODEL_FILE):
        train_hvac_model()

    # Simulate sensor input for testing
    simulated_sensor_data = {
        "temperature": round(random.uniform(18, 28), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "co2_level": random.randint(350, 1000),
        "occupancy": random.choice([0, 1]),
    }

    # Predict and print recommended temperature
    recommended_temp = predict_temperature(simulated_sensor_data)
    print(f"🌡️ AI Predicted Optimal Temperature: {recommended_temp}°C")
