import time
import random

# Try importing real hardware control libraries, fallback to simulation
try:
    import RPi.GPIO as GPIO  # Raspberry Pi GPIO control

    REAL_GPIO = True
except ImportError:
    print("⚠️ Warning: RPi.GPIO not found! Running in simulation mode.")
    REAL_GPIO = False

try:
    import paho.mqtt.client as mqtt  # MQTT for IoT-based HVAC control

    REAL_MQTT = True
except ImportError:
    print("⚠️ Warning: paho-mqtt not found! Running in simulation mode.")
    REAL_MQTT = False


### **1️⃣ Setup HVAC Control Using GPIO (Raspberry Pi)**
if REAL_GPIO:
    # Define GPIO pins for HVAC components
    FAN_PIN = 17
    HEATER_PIN = 27
    AC_PIN = 22

    # Setup GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.setup(HEATER_PIN, GPIO.OUT)
    GPIO.setup(AC_PIN, GPIO.OUT)

    # Ensure all devices are OFF initially
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.output(HEATER_PIN, GPIO.LOW)
    GPIO.output(AC_PIN, GPIO.LOW)


### **2️⃣ Setup IoT-Based HVAC Control Using MQTT**
if REAL_MQTT:
    MQTT_BROKER = "mqtt.example.com"  # Replace with your actual broker
    TOPIC_FAN = "home/hvac/fan"
    TOPIC_HEATER = "home/hvac/heater"
    TOPIC_AC = "home/hvac/ac"

    # Initialize MQTT Client
    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, 1883, 60)
    except Exception as e:
        print(f"⚠️ Warning: MQTT connection failed! Error: {e}")
        REAL_MQTT = False  # Fallback to simulation


### **3️⃣ Function to Control HVAC Using GPIO (Raspberry Pi)**
def control_hvac_gpio(desired_temperature, current_temperature):
    """Controls HVAC system using Raspberry Pi GPIO based on temperature readings"""
    if not REAL_GPIO:
        return simulate_hvac_control(desired_temperature, current_temperature)

    print("\n[GPIO HVAC Control]")
    if current_temperature > desired_temperature:
        print(f"Cooling down to {desired_temperature}°C... ❄️")
        GPIO.output(FAN_PIN, GPIO.HIGH)
        GPIO.output(AC_PIN, GPIO.HIGH)
        GPIO.output(HEATER_PIN, GPIO.LOW)
    elif current_temperature < desired_temperature:
        print(f"Heating up to {desired_temperature}°C... 🔥")
        GPIO.output(FAN_PIN, GPIO.LOW)
        GPIO.output(AC_PIN, GPIO.LOW)
        GPIO.output(HEATER_PIN, GPIO.HIGH)
    else:
        print("Temperature is optimal. No adjustment needed. ✅")
        GPIO.output(FAN_PIN, GPIO.LOW)
        GPIO.output(AC_PIN, GPIO.LOW)
        GPIO.output(HEATER_PIN, GPIO.LOW)


### **4️⃣ Function to Control HVAC Using IoT MQTT**
def control_hvac_mqtt(desired_temperature, current_temperature):
    """Controls HVAC system using IoT (MQTT-based smart plugs)"""
    if not REAL_MQTT:
        return simulate_hvac_control(desired_temperature, current_temperature)

    print("\n[IoT HVAC Control via MQTT]")
    if current_temperature > desired_temperature:
        print(f"Cooling down to {desired_temperature}°C... ❄️")
        client.publish(TOPIC_FAN, "ON")
        client.publish(TOPIC_AC, "ON")
        client.publish(TOPIC_HEATER, "OFF")
    elif current_temperature < desired_temperature:
        print(f"Heating up to {desired_temperature}°C... 🔥")
        client.publish(TOPIC_FAN, "OFF")
        client.publish(TOPIC_AC, "OFF")
        client.publish(TOPIC_HEATER, "ON")
    else:
        print("Temperature is optimal. No adjustment needed. ✅")
        client.publish(TOPIC_FAN, "OFF")
        client.publish(TOPIC_AC, "OFF")
        client.publish(TOPIC_HEATER, "OFF")


### **5️⃣ Simulated HVAC Control (For Non-Raspberry Pi Users)**
def simulate_hvac_control(desired_temperature, current_temperature):
    """Simulates HVAC system control when no real hardware is available"""
    print("\n[Simulated HVAC Control]")
    if current_temperature > desired_temperature:
        print(
            f"🌡️ Current Temperature: {current_temperature}°C (Too Hot) ❄️ Cooling to {desired_temperature}°C..."
        )
        hvac_status = {"fan": "ON", "ac": "ON", "heater": "OFF"}

    elif current_temperature < desired_temperature:
        print(
            f"🌡️ Current Temperature: {current_temperature}°C (Too Cold) 🔥 Heating to {desired_temperature}°C..."
        )
        hvac_status = {"fan": "OFF", "ac": "OFF", "heater": "ON"}

    else:
        print(
            f"✅ Current Temperature: {current_temperature}°C (Optimal) - No Adjustment Needed."
        )
        hvac_status = {"fan": "OFF", "ac": "OFF", "heater": "OFF"}

    return hvac_status


### **6️⃣ Run the HVAC System with Real or Simulated Data**
def control_hvac(desired_temperature, current_temperature):
    """Selects the best available method for HVAC control"""
    if REAL_GPIO:
        return control_hvac_gpio(desired_temperature, current_temperature)
    elif REAL_MQTT:
        return control_hvac_mqtt(desired_temperature, current_temperature)
    else:
        return simulate_hvac_control(desired_temperature, current_temperature)


### **7️⃣ Test HVAC Control (Standalone Execution)**
if __name__ == "__main__":
    TEST_TEMPERATURE = 22  # Desired temperature
    CURRENT_TEMPERATURE = round(
        random.uniform(18, 28), 2
    )  # Simulated current room temperature

    print(
        f"\n[Testing HVAC Control] Desired: {TEST_TEMPERATURE}°C, Current: {CURRENT_TEMPERATURE}°C"
    )
    control_hvac(TEST_TEMPERATURE, CURRENT_TEMPERATURE)
