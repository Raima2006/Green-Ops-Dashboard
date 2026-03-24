import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import psutil
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime
import subprocess

# --- 1. ROBUST PATH ROUTING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Fallback routing to handle duplicate files in root vs data_collection
POWER_LOGS_DC = os.path.join(ROOT_DIR, "data_collection", "hardware_logs.csv")
POWER_LOGS_ROOT = os.path.join(ROOT_DIR, "hardware_logs.csv")
POWER_LOGS = POWER_LOGS_DC if os.path.exists(POWER_LOGS_DC) else POWER_LOGS_ROOT

SSD_LOGS_DC = os.path.join(ROOT_DIR, "data_collection", "ssd_health_logs.csv")
SSD_LOGS_ROOT = os.path.join(ROOT_DIR, "ssd_health_logs.csv")
SSD_LOGS = SSD_LOGS_DC if os.path.exists(SSD_LOGS_DC) else SSD_LOGS_ROOT

# --- 2. ENTERPRISE CONFIGURATION & CSS ---
st.set_page_config(page_title="Green-Ops Intelligence", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Datadog/Grafana Style Dark Theme */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        color: #C9D1D9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }

    /* Clean Headers */
    .header-container {
        border-bottom: 1px solid #30363D;
        padding-bottom: 15px;
        margin-bottom: 25px;
        margin-top: 10px;
    }
    
    .main-title {
        font-size: 26px;
        font-weight: 600;
        color: #E6EDF3;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sub-title {
        font-size: 14px;
        color: #8B949E;
        margin-top: 4px;
    }

    /* Flat Metric Panels */
    .metric-panel {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 20px;
        height: 100%;
    }
    
    .panel-title {
        font-size: 12px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .panel-value {
        font-size: 28px;
        color: #58A6FF;
        font-weight: 600;
        line-height: 1.2;
    }

    .panel-value.green { color: #3FB950; }
    .panel-value.yellow { color: #D29922; }
    .panel-value.red { color: #F85149; }
    .panel-value.blue { color: #58A6FF; }

    .panel-subtext {
        font-size: 12px;
        color: #8B949E;
        margin-top: 6px;
    }

    /* Custom Progress Bars */
    .progress-bg {
        width: 100%;
        background-color: #30363D;
        border-radius: 4px;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .progress-fill-green { background-color: #3FB950; height: 6px; border-radius: 4px; }
    .progress-fill-red { background-color: #F85149; height: 6px; border-radius: 4px; }
    .progress-fill-blue { background-color: #58A6FF; height: 6px; border-radius: 4px; }

    /* Standardized Code Blocks for Process List */
    .process-item {
        background-color: #0D1117;
        border: 1px solid #30363D;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        font-family: monospace;
        font-size: 13px;
    }
    
    /* Alerts */
    .alert-box {
        padding: 12px 15px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .alert-warn { background-color: rgba(210, 153, 34, 0.1); border: 1px solid #D29922; color: #D29922; }
    .alert-info { background-color: rgba(88, 166, 255, 0.1); border: 1px solid #58A6FF; color: #58A6FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKEND LOGIC ---
def load_data(filepath, name="Data"):
    if not os.path.exists(filepath):
        st.sidebar.error(f"[ERROR] {name} file missing: {filepath}")
        return None
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            st.sidebar.warning(f"[WARNING] {name} file is empty: {filepath}")
            return None
        # Strip whitespace from headers to prevent KeyError
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.sidebar.error(f"[ERROR] Error reading {name}: {str(e)}")
        return None

def get_grid_intel():
    hour = datetime.now().hour
    if 9 <= hour <= 16:
        return 0.15, "Solar Peak Active", 75, 25, "PERFORMANCE", "green"
    elif 18 <= hour <= 22:
        return 0.75, "High Demand Mix", 15, 85, "CONSERVATION", "red"
    else:
        return 0.40, "Standard Baseline", 45, 55, "BALANCED", "yellow"

def get_ml_forecast(df):
    if df is None or len(df) < 15:
        return "CALIBRATING", 0.0, "yellow"
    
    try:
        df_ml = df.copy()
        df_ml['id'] = range(len(df_ml))
        X = df_ml[['id']].values
        y = df_ml['battery_percent'].values
        
        model = LinearRegression().fit(X, y)
        accuracy = r2_score(y, model.predict(X))
        slope = model.coef_[0]
        
        if slope >= 0:
            return "STABLE / AC POWER", accuracy, "green"
        
        mins_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
        return f"{round(mins_left, 1)} MINS RUL", accuracy, "yellow"
    except Exception:
        return "MODEL ERROR", 0.0, "red"

def get_processes():
    processes = []
    ignore = ['system idle process', 'python.exe', 'svchost.exe', 'system', 'wmi', 'registry']
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 1.0 and proc.info['name'].lower() not in ignore:
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

# --- 4. DATA INITIALIZATION ---
power_data = load_data(POWER_LOGS, "Power Logs")
ssd_data = load_data(SSD_LOGS, "SSD Logs")

intensity_val, grid_label, renew_pct, fossil_pct, dsm_mode, dsm_color = get_grid_intel()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:20px; margin-bottom: 20px;">System Status</div>', unsafe_allow_html=True)
    
    if power_data is not None and not power_data.empty:
        latest_p = power_data.iloc[-1]
        
        # Battery
        st.markdown('<div class="panel-title">Battery Level</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-value blue" style="font-size:24px;">{latest_p.get("battery_percent", 0)}%</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CPU Load
        cpu_val = latest_p.get('cpu_usage_percent', 0)
        eff_status = "Efficient" if cpu_val < 30 else "High Demand"
        eff_color = "#3FB950" if cpu_val < 30 else "#D29922"
        
        st.markdown('<div class="panel-title">CPU Load</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-value" style="font-size:24px; color:{eff_color};">{cpu_val}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-subtext">Efficiency Status: <span style="color:{eff_color}; font-weight:bold;">{eff_status}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="panel-subtext">Awaiting Telemetry...</div>', unsafe_allow_html=True)

# --- 6. MAIN UI RENDER ---
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Green-Ops Intelligence Dashboard</h1>
        <div class="sub-title">Monitoring environmental impact, hardware health, and predictive analytics.</div>
    </div>
    """, unsafe_allow_html=True)

if power_data is None or power_data.empty:
    st.markdown('<div class="alert-box alert-warn">Telemetry stream unavailable. Ensure data collection scripts are running. Check the sidebar for specific file errors.</div>', unsafe_allow_html=True)
else:
    latest = power_data.iloc[-1]
    
    # KPI ROW 1: Core Metrics
    col1, col2, col3 = st.columns(3)
    ml_stat, ml_acc, ml_color = get_ml_forecast(power_data)
    
    with col1:
        st.markdown(f"""
            <div class="metric-panel">
                <div class="panel-title">Current Battery</div>
                <div class="panel-value blue">{latest.get('battery_percent', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        cpu_current = latest.get('cpu_usage_percent', 0)
        c_color = "green" if cpu_current < 40 else "red"
        st.markdown(f"""
            <div class="metric-panel">
                <div class="panel-title">CPU Load</div>
                <div class="panel-value {c_color}">{cpu_current}%</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-panel">
                <div class="panel-title">ML Prediction</div>
                <div class="panel-value {ml_color}" style="font-size:22px; margin-top:5px;">{ml_stat}</div>
                <div class="panel-subtext">Model R2 Accuracy: {round(ml_acc, 2)}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ROW 2: Graph and Lifecycle
    col_chart, col_side = st.columns([2, 1])

    with col_chart:
        st.markdown('<div class="panel-title" style="font-size:14px;">Power Consumption Trend</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-subtext" style="margin-bottom:10px;">Real-time CPU Energy Profile</div>', unsafe_allow_html=True)
        
        # The Restored Area Graph
        fig = px.area(power_data.tail(60), x='timestamp', y='cpu_usage_percent')
        fig.update_traces(line_color='#58A6FF', fillcolor='rgba(88, 166, 255, 0.15)', line_width=2)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, title="", visible=False), 
            yaxis=dict(showgrid=True, gridcolor='#30363D', title="CPU Usage %"),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.markdown('<div class="panel-title" style="font-size:14px;">Hardware Lifecycle (SSD)</div>', unsafe_allow_html=True)
        if ssd_data is not None and not ssd_data.empty:
            wear = ssd_data.iloc[-1].get('percentage_used', 0)
            status_color = "green" if wear < 10 else "yellow" if wear < 50 else "red"
            
            st.markdown(f'<div class="panel-subtext" style="margin-bottom:5px;">SSD Wear Level: {wear}% Used</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="progress-bg"><div class="progress-fill-blue" style="width: {wear}%;"></div></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background-color: rgba(63, 185, 80, 0.1); border: 1px solid #3FB950; padding: 10px; border-radius: 4px;">
                    <span style="color: #3FB950; font-size: 13px; font-weight: 600;">Estimated Remaining Life: {100-wear}%</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="process-item"><span>No hardware data logged.</span></div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #30363D; margin: 25px 0px;'>", unsafe_allow_html=True)

    # ROW 3: Industrial Energy Management & Process Optimizer
    col_dsm, col_proc = st.columns([1, 1])
    
    with col_dsm:
        st.markdown('<div class="panel-title" style="font-size:14px;">Industrial Energy Management (DSM)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-subtext">Current Grid Generation Source: {grid_label}</div>', unsafe_allow_html=True)
        
        # Renewable Bar
        st.markdown(f'<div class="panel-subtext" style="margin-top:15px;">Renewable Energy: {renew_pct}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bg"><div class="progress-fill-green" style="width: {renew_pct}%;"></div></div>', unsafe_allow_html=True)
        
        # Fossil Bar
        st.markdown(f'<div class="panel-subtext">Fossil Fuel (Coal/Gas): {fossil_pct}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bg"><div class="progress-fill-red" style="width: {fossil_pct}%;"></div></div>', unsafe_allow_html=True)

        # Mode Box
        box_bg = "rgba(248, 81, 73, 0.1)" if dsm_mode == "CONSERVATION" else "rgba(63, 185, 80, 0.1)"
        box_border = "#F85149" if dsm_mode == "CONSERVATION" else "#3FB950"
        st.markdown(f"""
            <div style="background-color: {box_bg}; border: 1px solid {box_border}; padding: 15px; border-radius: 6px; margin-top:20px;">
                <div style="color: {box_border}; font-weight: 600; margin-bottom: 5px;">MODE: {dsm_mode}</div>
                <div style="color: #C9D1D9; font-size: 12px;">{'Grid is dirty. Postpone heavy tasks.' if dsm_mode == 'CONSERVATION' else 'Optimal grid conditions for heavy computing.'}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_proc:
        st.markdown('<div class="panel-title" style="font-size:14px;">Carbon-Critical Process Optimizer</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-subtext" style="margin-bottom:15px;">Identified background applications impacting efficiency:</div>', unsafe_allow_html=True)
        
        hogs = get_processes()
        if hogs:
            for h in hogs:
                st.markdown(f"""
                    <div class="process-item">
                        <span>{h['name'][:25]}</span>
                        <span style="color:#F85149;">{h['cpu_percent']}% CPU</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="process-item"><span>System lean</span><span style="color:#3FB950;">OK</span></div>', unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #30363D; margin: 25px 0px;'>", unsafe_allow_html=True)

   # ROW 4: Sustainability Insights
    st.markdown('<div class="panel-title" style="font-size:14px;">Sustainability Insights</div>', unsafe_allow_html=True)
    
    # Calculate carbon footprint using the fallback average if data is short
    avg_cpu = power_data['cpu_usage_percent'].tail(20).mean() if len(power_data) > 0 else 0
    est_carbon = (avg_cpu / 100) * 45 * intensity_val

    st.markdown(f"""
        <div class="metric-panel" style="margin-bottom:15px;">
            <div class="panel-title">Real-time Grid Status</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <div>
                    <div class="panel-subtext">Current Carbon Intensity</div>
                    <div class="panel-value blue">{intensity_val} kg/kWh</div>
                </div>
                <div style="background-color:#161B22; border:1px solid #30363D; padding:10px 15px; border-radius:4px;">
                    <span class="panel-subtext">Grid Status: </span>
                    <span style="color:{dsm_color}; font-weight:600;">{grid_label}</span>
                </div>
            </div>
            <div class="alert-box alert-warn" style="margin-bottom: 10px;">
                Grid-Sync Advice: {"The grid is currently carbon-heavy. Avoid charging or heavy tasks." if intensity_val > 0.5 else "Carbon intensity is optimal. Safe for intensive tasks."}
            </div>
            <div class="alert-box alert-info">
                Based on recent usage, your estimated digital carbon footprint is {est_carbon:.2f} gCO2/hr.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ACTION FOOTER ---
st.markdown("<br>", unsafe_allow_html=True)
bot_col1, bot_col2 = st.columns([4, 1])

with bot_col1:
    st.markdown(f"<div class='panel-subtext'>System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data Sync: Active</div>", unsafe_allow_html=True)

with bot_col2:
    if st.button("Generate Audit Report", use_container_width=True):
        try:
            subprocess.run(["python", os.path.join(ROOT_DIR, "devops_scripts", "report_generator.py")], check=True)
            st.success("Report saved to project root.")
        except Exception as e:
            st.error("Audit failed. Check logs.")

time.sleep(5)
st.rerun()