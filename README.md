# 🌱 Green-Ops Intelligence: A Unified Sustainability Dashboard for Digital Carbon Accounting and Asset Reliability

Green-Ops Intelligence is a local, enterprise-grade telemetry and sustainability dashboard built with Python and Streamlit. It is designed to monitor system hardware, predict battery degradation using Machine Learning, and calculate the real-time digital carbon footprint of computing tasks based on simulated grid carbon intensity.

Developed as an Industry Oriented Mini Project (IOMP), this tool bridges the gap between DevOps and environmental sustainability (Green-Ops).

---

## 📚 Table of Contents

1. [Why Green-Ops?](#why-green-ops)  
2. [Key Features](#key-features)  
3. [Project Architecture](#project-architecture)  
4. [Prerequisites](#prerequisites)  
5. [Installation & Setup](#installation--setup)  
6. [How to Run Safely](#how-to-run-safely)  
7. [Privacy & Security](#privacy--security)  
8. [Author](#author)  

---

## 🌍 Why Green-Ops?

As computing power scales, so does its environmental impact and hardware degradation. Green-Ops Intelligence addresses two critical challenges in modern infrastructure:

- **Carbon Accounting:** Users rarely know the carbon cost of their background processes. This tool simulates grid intensity (Demand-Side Management) to advise when to run heavy workloads versus when to conserve energy.

- **Asset Reliability:** Sudden hardware failure leads to data loss and e-waste. By tracking SSD wear levels and predicting battery runtime via linear regression models, this dashboard enables proactive hardware lifecycle management.

---

## ✨ Key Features

- **Real-time Telemetry:** Tracks CPU load, memory utilization, and battery state at 10-second intervals.

- **Predictive ML Engine:** Uses `scikit-learn` to run a linear regression model on battery drain, predicting Remaining Useful Life (RUL) and charging stability.

- **Carbon-Critical Process Optimizer:** Scans background applications and flags processes consuming excessive CPU and increasing energy cost.

- **Hardware Lifecycle Tracking:** Interfaces with `smartmontools` to extract low-level NVMe/SSD telemetry, tracking degradation and wear percentage.

- **Automated ESG Reporting:** Generates a daily text-based audit report summarizing energy consumption, hardware health, and estimated carbon emissions.

---

## 🏗️ Project Architecture

The repository is structured to separate data collection from presentation logic:

```text
Green-Ops-Dashboard/
│
├── data_collection/
│   ├── power_harvester.py       # Continuous CPU/Battery logging
│   └── ssd_health.py            # SSD diagnostics (admin required)
│
├── devops_scripts/
│   └── report_generator.py      # ESG audit report generator
│
├── dashboard/
│   └── app.py                   # Streamlit dashboard UI
│
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚙️ Prerequisites

To run this project on a Windows machine, install:

- Python 3.10+
- `smartmontools` (for SSD telemetry)

Install smartmontools using Windows Package Manager:

```powershell
winget install smartmontools
```

> Restart your terminal after installation so `smartctl` is recognized.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/YourUsername/Green-Ops-Dashboard.git
cd Green-Ops-Dashboard
```

---

### 2. Install Dependencies

It is recommended to use a virtual environment:

```powershell
pip install -r requirements.txt
```

---

## ▶️ How to Run Safely

This project runs multiple components simultaneously.

---

### Step 1: Start the Power Harvester

```powershell
python data_collection/power_harvester.py
```

- Runs continuously  
- Logs CPU and battery data every 10 seconds  
- Keep this terminal open  

---

### Step 2: Log SSD Health (Admin Required)

Open a new terminal **as Administrator**:

```powershell
python data_collection/ssd_health.py
```

- Run once per session/day  
- Updates SSD lifecycle data  

---

### Step 3: Launch the Dashboard

```powershell
streamlit run dashboard/app.py
```

Access dashboard at:

```
http://localhost:8501
```

---

## 🔐 Privacy & Security

- **100% Local Execution:** No external APIs or servers involved  
- **No Data Transmission:** All data stays on your system  
- **Local Storage Only:** Telemetry stored in `.csv` files  
- **Safe Version Control:** `.gitignore` prevents logs from being pushed  

---

## 📌 Notes

- Ensure all scripts are running for full functionality  
- Admin privileges are required only for SSD diagnostics  
- Keep terminals active while monitoring  

---

## 👨‍💻 Author

Developed as part of an Industry Oriented Mini Project (IOMP) focused on sustainable computing and system reliability.
By- Raima Shasmeen and Noshank Fadiya

---

## 📄 License

This project is open-source and available under the MIT License.