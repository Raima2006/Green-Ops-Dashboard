import pandas as pd
import os
from datetime import datetime

POWER_LOGS = os.path.join("data_collection", "hardware_logs.csv")
SSD_LOGS = os.path.join("data_collection", "ssd_health_logs.csv")
REPORT_FILE = "daily_carbon_report.txt"

def get_grid_intensity():
    hour = datetime.now().hour
    if 9 <= hour <= 16:
        return 0.15, "Clean Supply (Solar Peak)"
    elif 18 <= hour <= 22:
        return 0.75, "Dirty Supply (High Demand)"
    else:
        return 0.40, "Moderate Supply"

def generate_summary():
    if not os.path.exists(POWER_LOGS):
        print("[ERROR] No data found to generate a report.")
        return

    df_p = pd.read_csv(POWER_LOGS)
    df_s = pd.read_csv(SSD_LOGS) if os.path.exists(SSD_LOGS) else None
    intensity, intensity_label = get_grid_intensity()
    
    avg_cpu = df_p['cpu_usage_percent'].mean()
    total_samples = len(df_p)
    hours_tracked = (total_samples * 10) / 3600 
    
    total_carbon = (avg_cpu / 100) * 45 * hours_tracked * intensity

    report_content = f"""
================================================
GREEN-OPS DAILY SUSTAINABILITY REPORT
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
================================================

STATISTICS:
- Total Monitoring Time     : {round(hours_tracked, 2)} hours
- Average CPU Load          : {round(avg_cpu, 1)}%
- Estimated Carbon Produced : {round(total_carbon, 4)} kg CO2
- Grid Status at Generation : {intensity_label}

HARDWARE HEALTH:
"""
    
    if df_s is not None and not df_s.empty:
        latest_wear = df_s['percentage_used'].iloc[-1]
        report_content += f"- SSD Wear Level          : {latest_wear}% used\n"
        report_content += f"- Remaining Life Estimate : {100 - latest_wear}%\n"
    else:
        report_content += "- SSD health data not available.\n"

    report_content += "\nSYSTEM SUGGESTION:\n"
    if avg_cpu > 50:
        report_content += "[WARNING] High energy usage detected. Consider optimizing background tasks."
    else:
        report_content += "[OK] System is running within efficient parameters."
        
    report_content += "\n================================================\n"

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"[SUCCESS] Report saved to {os.path.abspath(REPORT_FILE)}")

if __name__ == "__main__":
    generate_summary()