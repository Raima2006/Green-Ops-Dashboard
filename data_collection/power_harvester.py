import psutil
import pandas as pd
import time
import os
from datetime import datetime

# Path to save our logs - keeping it inside the project folder
LOG_FILE = "hardware_logs.csv"

def collect_pulse():
    """Captures a single snapshot of hardware data."""
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Data dictionary
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "battery_percent": battery.percent if battery else 100,
        "power_plugged": 1 if (battery and battery.power_plugged) else 0,
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": psutil.virtual_memory().percent
    }
    return data

def save_to_csv(data):
    """Saves data to CSV. Creates the file if it doesn't exist."""
    df = pd.DataFrame([data])
    # if file does not exist write header 
    if not os.path.isfile(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else: # else it exists so append without writing the header
        df.to_csv(LOG_FILE, mode='a', index=False, header=False)

if __name__ == "__main__":
    print("🚀 Green-Ops Data Collection Started...")
    print(f"Recording data to {os.path.abspath(LOG_FILE)}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            pulse = collect_pulse()
            save_to_csv(pulse)
            print(f"Synced @ {pulse['timestamp']} | Battery: {pulse['battery_percent']}% | CPU: {pulse['cpu_usage_percent']}%")
            time.sleep(10) # Wait 10 seconds before next pulse
    except KeyboardInterrupt:
        print("\n🛑 Collection stopped by user.")