import psutil
import pandas as pd
import time
import os
from datetime import datetime

# Saving relative to the script's execution context
LOG_FILE = os.path.join("data_collection", "hardware_logs.csv")

def collect_pulse():
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent(interval=1)
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "battery_percent": battery.percent if battery else 100,
        "power_plugged": 1 if (battery and battery.power_plugged) else 0,
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": psutil.virtual_memory().percent
    }
    return data

def save_to_csv(data):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    df = pd.DataFrame([data])
    if not os.path.isfile(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode='a', index=False, header=False)

if __name__ == "__main__":
    print("System Data Collection Started...")
    print(f"Recording data to {os.path.abspath(LOG_FILE)}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            pulse = collect_pulse()
            save_to_csv(pulse)
            print(f"[{pulse['timestamp']}] SYNC | Battery: {pulse['battery_percent']}% | CPU: {pulse['cpu_usage_percent']}%")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nCollection stopped by user.")