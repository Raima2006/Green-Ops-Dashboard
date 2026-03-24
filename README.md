# 🌱 Green-Ops: Sustainable Computing & Hardware Analytics

An end-to-end DevOps and ML project designed to monitor, predict, and report the environmental impact and physical health of computing hardware.

## 🚀 How to Run
1. **Data Collection:** - Run `python data_collection/power_harvester.py` (Standard CMD)
   - Run `python data_collection/ssd_health.py` (Administrator CMD)
2. **Dashboard:** - Run `python -m streamlit run dashboard/app.py`
3. **Reporting:** - Click 'Generate Report' on the dashboard or run `python devops_scripts/report_generator.py`

## 📊 Features
- **Real-time Telemetry:** Tracks CPU load and battery discharge rates.
- **Hardware Lifecycle:** Monitors SSD wear levels using `smartmontools`.
- **Machine Learning:** Uses Linear Regression to predict battery shutdown time.
- **Carbon Accounting:** Estimates CO2 emissions based on real-time power consumption.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** Streamlit, Pandas, Plotly, Scikit-Learn, Psutil
- **Hardware Interface:** Smartmontools (smartctl)

.\.venv\Scripts\Activate.ps1
streamlit run app.py