import random
import time

# Try importing real sensor libraries, fallback to simulation if not available
try:
    import Adafruit_DHT  # DHT22 Sensor
    import serial  # For MH-Z19 CO₂ Sensor

    REAL_SENSORS = True
except ImportError:
    print("⚠️ Warning: Sensor libraries not found! Using simulated sensor data.")
    REAL_SENSORS = False


# Read Temperature & Humidity (DHT22)**
def get_temperature_humidity():
    """Reads Temperature & Humidity from DHT22 Sensor (or simulates if unavailable)"""
    if REAL_SENSORS:
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 4  # GPIO Pin
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            return round(temperature, 2), round(humidity, 2)
        else:
            print("❌ Error: Failed to retrieve data from DHT22 sensor")
            return None, None
    else:
        return round(random.uniform(18, 30), 2), round(random.uniform(30, 70), 2)


# Read CO₂ Levels (MH-Z19)**
def get_co2_level():
    """Reads CO₂ Level from MH-Z19 Sensor (or simulates if unavailable)"""
    if REAL_SENSORS:
        try:
            ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
            ser.write(
                b"\xff\x01\x86\x00\x00\x00\x00\x00\x79"
            )  # Command to read CO2 level
            response = ser.read(9)
            if response and response[0] == 0xFF and response[1] == 0x86:
                co2 = response[2] * 256 + response[3]
                return co2
        except Exception as e:
            print(f"❌ Error: Failed to read CO₂ sensor: {e}")
            return None
    else:
        return random.randint(350, 1000)


# Detect Occupancy Using AI (or Simulated)**
def detect_occupancy():
    """Uses AI-powered camera to detect people (or simulates if unavailable)"""
    try:
        import cv2
        from ultralytics import YOLO

        model = YOLO("yolov8n.pt")  # Load YOLOv8 model (Pretrained on COCO dataset)
        cap = cv2.VideoCapture(0)  # Open camera

        if not cap.isOpened():
            print("❌ Error: Could not open camera! Assuming no occupancy.")
            return 0  # Assume no one is in the room

        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame! Assuming no occupancy.")
            return 0  # Assume no one is in the room

        results = model(frame)  # Run YOLO detection
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])  # Class ID
                if cls_id == 0:  # Class 0 is 'Person' in COCO dataset
                    return 1  # At least one person detected

        cap.release()
        return 0  # No people detected

    except ImportError:
        print(
            "⚠️ Warning: OpenCV & YOLO not found! Using simulated occupancy detection."
        )
        return random.choice([0, 1])  # Simulate random occupancy


# Simulate Energy Consumption**
def get_energy_usage():
    """Simulates energy consumption data"""
    return round(random.uniform(0.08, 0.30), 2)  # $ per kWh


# Retrieve All Sensor Data in Real-Time**
def get_real_sensor_data():
    """Retrieves real-time data from HVAC sensors"""
    temperature, humidity = get_temperature_humidity()
    co2_level = get_co2_level()
    occupancy = detect_occupancy()
    energy_cost = get_energy_usage()

    sensor_data = {
        "temperature": temperature if temperature else 22,  # Default 22°C
        "humidity": humidity if humidity else 50,  # Default 50%
        "co2_level": co2_level if co2_level else 400,  # Default 400 ppm
        "occupancy": occupancy,  # 1 if occupied, 0 if not
        "energy_cost": energy_cost,  # $ per kWh
    }

    return sensor_data


# Test the Sensors**
if __name__ == "__main__":
    while True:
        data = get_real_sensor_data()
        print("\n[Real-Time HVAC Sensor Data]")
        for key, value in data.items():
            unit = (
                "°C"
                if key == "temperature"
                else (
                    "%"
                    if key == "humidity"
                    else (
                        "ppm"
                        if key == "co2_level"
                        else "" if key == "occupancy" else "$ per kWh"
                    )
                )
            )
            print(f"{key.replace('_', ' ').capitalize()}: {value} {unit}")

        time.sleep(5)  # Refresh every 5 seconds
