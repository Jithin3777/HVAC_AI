from flask import Flask, render_template, request, jsonify
from src.sensors import get_real_sensor_data
from src.hvac_control import control_hvac
from src.ai_model import predict_temperature, update_model_with_user_preference

import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))

desired_temperature = 22  # Default desired temperature


# Home Route - Show Dashboard:-
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# API to Fetch Live Sensor Data:-
@app.route("/sensor_data")
def sensor_data():
    """Returns real-time sensor data in JSON format."""
    data = get_real_sensor_data()
    predicted_temp = predict_temperature(data)  # AI predicted temperature
    data["predicted_temperature"] = predicted_temp  # Add AI prediction to response
    return jsonify(data)


# API to Set Desired Temperature:-
@app.route("/set_temperature", methods=["POST"])
def set_temperature():
    """Receives user-defined temperature and updates the HVAC system."""
    global desired_temperature
    req_data = request.get_json()
    desired_temperature = float(req_data.get("temperature", 22))

    # Get current sensor data
    sensor_data = get_real_sensor_data()

    # Train AI with user feedback
    update_model_with_user_preference(sensor_data, desired_temperature)

    # Adjust HVAC system
    control_hvac(desired_temperature, sensor_data["temperature"])

    return jsonify(
        {"message": "Temperature updated", "temperature": desired_temperature}
    )


# Run Flask App:-
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
