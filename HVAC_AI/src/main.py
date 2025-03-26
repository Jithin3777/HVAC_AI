from sensors import get_real_sensor_data
from hvac_control import control_hvac
from ai_model import predict_temperature


def run_hvac_system():
    """Runs the HVAC AI system using real or simulated sensor data."""

    # Get real-time sensor data
    sensor_data = get_real_sensor_data()

    # AI Predicted Temperature
    predicted_temperature = predict_temperature(sensor_data)

    print("\n[📡 Real-Time HVAC Sensor Data]")
    for key, value in sensor_data.items():
        unit = (
            "°C"
            if key == "temperature"
            else "%" if key == "humidity" else "ppm" if key == "co2_level" else ""
        )
        print(f"{key.replace('_', ' ').capitalize()}: {value} {unit}")

    print(f"🌡️ AI Predicted Optimal Temperature: {predicted_temperature}°C")

    # Adjust HVAC system based on AI's recommendation
    control_hvac(predicted_temperature, sensor_data["temperature"])


if __name__ == "__main__":
    run_hvac_system()
