import pandas as pd
import os
from datetime import datetime

POWER_LOGS = "../data_collection/hardware_logs.csv"
SSD_LOGS = "../data_collection/ssd_health_logs.csv"
REPORT_FILE = "../daily_carbon_report.txt"
# Place this below your other def functions
def get_grid_intensity():
    hour = datetime.now().hour
    if 9 <= hour <= 16: # Solar hours
        return 0.15, "🟢 Clean (Solar Peak)"
    elif 18 <= hour <= 22: # Evening peak (Fossil fuels)
        return 0.75, "🔴 Dirty (High Demand)"
    else:
        return 0.40, "🟡 Moderate"
def generate_summary():
    if not os.path.exists(POWER_LOGS):
        print("No data found to generate a report.")
        return

    # Load Data
    df_p = pd.read_csv(POWER_LOGS)
    df_s = pd.read_csv(SSD_LOGS) if os.path.exists(SSD_LOGS) else None
    intensity, _ = get_grid_intensity()
    # Calculations
    avg_cpu = df_p['cpu_usage_percent'].mean()
    total_samples = len(df_p)
    # Estimate: (Avg CPU/100) * 45W * (hours of data) * 0.4 kg CO2
    hours_tracked = (total_samples * 10) / 3600 
    # Fetches the simulated dynamic intensity
     
    total_carbon = (avg_cpu / 100) * 45 * hours_tracked * intensity
    # total_carbon = (avg_cpu / 100) * 45 * hours_tracked * 0.4

    # Create Report Content
    report_content = f"""
    ================================================
    🌱 GREEN-OPS DAILY SUSTAINABILITY REPORT
    Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ================================================
    
    STATISTICS:
    - Total Monitoring Time: {round(hours_tracked, 2)} hours
    - Average CPU Load: {round(avg_cpu, 1)}%
    - Estimated Carbon Produced: {round(total_carbon, 4)} kg CO2
    
    HARDWARE HEALTH:
    """
    
    if df_s is not None:
        latest_wear = df_s['percentage_used'].iloc[-1]
        report_content += f"- SSD Wear Level: {latest_wear}% used\n"
        report_content += f"- Remaining Life Estimate: {100 - latest_wear}%\n"
    else:
        report_content += "- SSD health data not available.\n"

    report_content += "\nSUGGESTION:\n"
    if avg_cpu > 50:
        report_content += "⚠️ High energy usage detected. Consider optimizing background tasks."
    else:
        report_content += "✅ Your system is running efficiently!"
        
    report_content += "\n================================================"

    # Save to file
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    #print(f"✅ Success! Report saved to {os.path.abspath(REPORT_FILE)}")
    # Use standard text to ensure compatibility with all Windows terminals
    print(f"SUCCESS: Report saved to {os.path.abspath(REPORT_FILE)}")

if __name__ == "__main__":
    generate_summary()