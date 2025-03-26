# HVAC AI Project

# 🚀 AI-Powered HVAC Control System  

This project is an **AI-driven HVAC system** that **automatically optimizes temperature** based on real-time **sensor data**.  

## 🔥 Features  
✅ **Live Sensor Monitoring** (Temperature, Humidity, CO₂, Occupancy)  
✅ **AI-Powered Temperature Control** (Learns user preferences)  
✅ **Interactive Web Dashboard** (Set desired temperature, view real-time data)  
✅ **Smart HVAC Adjustments** (Automatic cooling/heating control)  
✅ **Runs on Raspberry Pi or Simulated Data**  

## 🛠️ Tech Stack  
🔹 Python (Flask, Scikit-learn, NumPy, Pandas)  
🔹 Machine Learning (RandomForest)  
🔹 Web: HTML, CSS, JavaScript  
🔹 IoT Integration: MQTT, RPi.GPIO (or simulated)  

## 🚀 How to Run  
1️⃣ Clone the repository  
```bash
git clone https://github.com/Jithin3777/HVAC_AI.git
cd HVAC_AI

#Install dependencies
pip install -r requirements.txt

#Run the AI Model
python src/ai_model.py

#Start the Web Dashboard
python -m src.web_app
