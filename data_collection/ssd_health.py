import subprocess
import json
import pandas as pd
from datetime import datetime
import os

LOG_FILE = os.path.join("data_collection", "ssd_health_logs.csv")

def get_ssd_metrics():
    try:
        result = subprocess.run(['smartctl', '--json', '-a', 'pd0'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        nvme_info = data.get('nvme_smart_health_information_log', {})
        
        if not nvme_info:
            print("[WARNING] No NVMe health data found. Drive might be SATA.")
            return None

        metrics = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": nvme_info.get('temperature', 0),
            "percentage_used": nvme_info.get('percentage_used', 0),
            "data_units_written": nvme_info.get('data_units_written', 0),
            "power_cycles": nvme_info.get('power_cycles', 0)
        }
        return metrics
    except Exception as e:
        print(f"[ERROR] Reading SSD: {e}")
        return None

def save_health_data(data):
    if data:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        df = pd.DataFrame([data])
        if not os.path.isfile(LOG_FILE):
            df.to_csv(LOG_FILE, index=False)
        else:
            df.to_csv(LOG_FILE, mode='a', index=False, header=False)

if __name__ == "__main__":
    print("Starting SSD Health Monitoring...")
    try:
        stats = get_ssd_metrics()
        if stats:
            save_health_data(stats)
            print(f"[SUCCESS] SSD Health Logged | Wear Level: {stats['percentage_used']}% Used")
        else:
            print("[FAILED] Could not retrieve data. Ensure execution as Administrator.")
    except KeyboardInterrupt:
        print("\nSSD Monitoring stopped.")