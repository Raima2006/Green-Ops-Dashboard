# Draft 1
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# from datetime import datetime

# # --- CONFIGURATION ---
# st.set_page_config(page_title="Green-Ops Dashboard", layout="wide")
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# def load_data(file_path):
#     if os.path.exists(file_path):
#         return pd.read_csv(file_path)
#     return None

# # --- HEADER ---
# st.title("🌱 Green-Ops: Sustainability & Lifecycle Dashboard")
# st.markdown("Monitoring the environmental impact and physical health of your computing assets.")

# # --- SIDEBAR / KPI ---
# st.sidebar.header("System Status")
# power_data = load_data(POWER_LOGS)
# ssd_data = load_data(SSD_LOGS)

# if power_data is not None and not power_data.empty:
#     latest_p = power_data.iloc[-1]
#     st.sidebar.metric("Battery Level", f"{latest_p['battery_percent']}%")
#     st.sidebar.metric("CPU Load", f"{latest_p['cpu_usage_percent']}%")
#     status = "🟢 Efficient" if latest_p['cpu_usage_percent'] < 30 else "🟡 High Demand"
#     st.sidebar.write(f"Efficiency Status: **{status}**")

# # --- MAIN LAYOUT ---
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("⚡ Power Consumption Trend")
#     if power_data is not None:
#         # Show last 50 entries
#         chart_data = power_data.tail(50)
#         fig_power = px.line(chart_data, x='timestamp', y='cpu_usage_percent', 
#                             title="CPU Energy Demand", line_shape='spline')
#         st.plotly_chart(fig_power, use_container_width=True)
#     else:
#         st.info("Waiting for Power Logs... Run power_harvester.py")

# with col2:
#     st.subheader("🛠️ Hardware Lifecycle (SSD)")
#     if ssd_data is not None:
#         latest_s = ssd_data.iloc[-1]
#         wear = latest_s['percentage_used']
        
#         # Simple Gauge-like visualization
#         st.write(f"**SSD Wear Level:** {wear}% Used")
#         st.progress(int(wear))
        
#         remaining = 100 - wear
#         st.success(f"Estimated Remaining Life: {remaining}%")
        
#         if wear > 80:
#             st.warning("⚠️ High Wear Detected: Plan for hardware replacement to avoid data loss.")
#     else:
#         st.info("Waiting for SSD Logs... Run ssd_health.py as Admin")

# # --- SUSTAINABILITY INSIGHTS ---
# st.divider()
# st.subheader("🌍 Sustainability Insights")
# if power_data is not None:
#     # Basic Carbon Logic: 45W Avg * Carbon Intensity (Mocked at 400g/kWh)
#     avg_cpu = power_data['cpu_usage_percent'].mean()
#     est_carbon = (avg_cpu / 100) * 45 * 0.4 
    
#     st.info(f"Based on your current usage, your estimated digital carbon footprint is **{est_carbon:.2f} gCO2/hr**.")
#     st.write("💡 *Tip: Closing high-load background apps can reduce this by up to 15%.*")



# Draft2
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import time
# from sklearn.linear_model import LinearRegression

# # --- CONFIGURATION ---
# st.set_page_config(page_title="Green-Ops Dashboard", layout="wide")
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# # --- ML PREDICTION ENGINE ---
# def get_battery_prediction(df):
#     if len(df) < 10:
#         return "Analyzing patterns..."
    
#     df['id'] = range(len(df))
#     X = df[['id']].values
#     y = df['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
#     slope = model.coef_[0]
    
#     if slope >= 0:
#         return "⚡ Charging / Stable"
    
#     # Calculate minutes remaining (assuming 10s intervals)
#     minutes_left = (-model.intercept_ / slope - len(df)) * (10 / 60)
#     return f"📉 Approx. {round(minutes_left, 1)} mins remaining"

# # --- DATA LOADING ---
# def load_data(file_path):
#     if os.path.exists(file_path):
#         return pd.read_csv(file_path)
#     return None

# # --- UI LAYOUT ---
# st.title("🌱 Green-Ops Intelligence Dashboard")

# power_data = load_data(POWER_LOGS)
# ssd_data = load_data(SSD_LOGS)

# # Top Row: KPIs
# col_a, col_b, col_c = st.columns(3)
# if power_data is not None and not power_data.empty:
#     latest = power_data.iloc[-1]
#     col_a.metric("Current Battery", f"{latest['battery_percent']}%")
#     col_b.metric("CPU Load", f"{latest['cpu_usage_percent']}%")
#     col_c.metric("ML Prediction", get_battery_prediction(power_data))

# # Graphs
# if power_data is not None:
#     fig = px.line(power_data.tail(50), x='timestamp', y='cpu_usage_percent', title="Real-time CPU Energy Profile")
#     st.plotly_chart(fig, use_container_width=True)

# # Auto-Refresh Logic
# time.sleep(5)
# st.rerun()


import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import psutil
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import r2_score


# --- CONFIGURATION ---
st.set_page_config(page_title="Green-Ops Intelligence Dashboard", layout="wide")
POWER_LOGS = "../data_collection/hardware_logs.csv"
SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# --- ML PREDICTION ENGINE ---  draft 1
# def get_battery_prediction(df):
#     if len(df) < 10:
#         return "Analyzing patterns..."
    
#     # Simple linear regression to predict battery drain
#     df_ml = df.copy()
#     df_ml['id'] = range(len(df_ml))
#     X = df_ml[['id']].values
#     y = df_ml['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
#     slope = model.coef_[0]
    
#     if slope >= 0:
#         return "⚡ Charging / Stable"
    
#     # Calculate minutes remaining (assuming 10s intervals)
#     # formula: 0 = slope * x + intercept
#     minutes_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
#     return f"📉 Approx. {round(minutes_left, 1)} mins left"



#draft 2
# def get_battery_prediction(df):
#     if len(df) < 10:
#         return "Analyzing patterns..."
    
#     df_ml = df.copy()
#     df_ml['id'] = range(len(df_ml))
#     X = df_ml[['id']].values
#     y = df_ml['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
    
#     # --- ACCURACY CALCULATION ---
#     y_pred = model.predict(X)
#     accuracy = r2_score(y, y_pred)
    
#     # Print to Terminal
#     print(f"[{datetime.now().strftime('%H:%M:%S')}] Model R² Accuracy: {accuracy:.4f}")
#     # ----------------------------

#     slope = model.coef_[0]
#     if slope >= 0:
#         return "⚡ Charging / Stable"
    
#     minutes_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
#     return f"📉 Approx. {round(minutes_left, 1)} mins left"

#ML perdiction

# def get_battery_prediction(df):
#     if len(df) < 20: # Increased minimum data points for better fit
#         return "Gathering more data...", 0.0
    
#     df_ml = df.copy()
#     df_ml['id'] = range(len(df_ml))
#     X = df_ml[['id']].values
#     y = df_ml['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
#     y_pred = model.predict(X)
#     accuracy = r2_score(y, y_pred)
    
#     # Only print if there's actually a trend
#     print(f"[{datetime.now().strftime('%H:%M:%S')}] R²: {accuracy:.4f}")

#     slope = model.coef_[0]
#     if slope >= 0:
#         return "⚡ Stable / Charging", accuracy
    
#     minutes_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
#     return f"📉 ~{round(minutes_left, 1)} mins left", accuracy


def get_battery_prediction(df):
    # Check if the required column actually exists
    if 'battery_percent' not in df.columns:
        return "Sensor Offline", 0.0
        
    if len(df) < 20: 
        return "Gathering data...", 0.0
    
    try:
        df_ml = df.copy()
        df_ml['id'] = range(len(df_ml))
        X = df_ml[['id']].values
        y = df_ml['battery_percent'].values # Now safe because of the check above
        
        model = LinearRegression().fit(X, y)
        accuracy = r2_score(y, model.predict(X))
        slope = model.coef_[0]
        
        if slope >= 0:
            return "⚡ Stable/Charging", accuracy
        
        mins_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
        return f"📉 ~{round(mins_left, 1)}m RUL", accuracy
    except Exception as e:
        return "Model Error", 0.0



# # --- DATA LOADING ---
# def load_data(file_path):
#     if os.path.exists(file_path):
#         return pd.read_csv(file_path)
#     return None


# def load_data(file_path):
#     if os.path.exists(file_path):
#         df = pd.read_csv(file_path)
#         # PROFESSIONAL TRICK: Strip whitespace from all column names
#         df.columns = df.columns.str.strip() 
#         return df
#     return None


# def load_data(file_path):
#     if os.path.exists(file_path):
#         # We tell pandas there is NO header in the file, 
#         # and we provide the professional names manually.
#         column_names = [
#             'timestamp', 
#             'battery_percent', 
#             'is_charging', 
#             'cpu_usage_percent', 
#             'cpu_frequency'
#         ]
        
#         df = pd.read_csv(file_path, names=column_names)
#         return df
#     return None


def load_data(file_path):
    if not os.path.exists(file_path):
        return None
        
    try:
        # Check which file we are loading to apply the correct 'Schema'
        if "hardware_logs" in file_path:
            cols = ['timestamp', 'battery_percent', 'is_charging', 'cpu_usage_percent', 'cpu_freq']
            df = pd.read_csv(file_path, names=cols)
        elif "ssd_health_logs" in file_path:
    # Most SSD harvesters put 'Percentage Used' as the 2nd or 3rd value
    # Let's align it correctly based on your screenshot's output:
         cols = ['timestamp', 'percentage_used', 'model', 'serial', 'data_read', 'data_written']
         df = pd.read_csv(file_path, names=cols)    
        # elif "ssd_health_logs" in file_path:
        #     # These names MUST match exactly what you use in line 465
        #     cols = ['timestamp', 'model', 'serial', 'percentage_used', 'data_read', 'data_written']
        #     df = pd.read_csv(file_path, names=cols)

        else:
            df = pd.read_csv(file_path)
            
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None


# Place this below your other def functions
def get_grid_intensity():
    hour = datetime.now().hour
    if 9 <= hour <= 16: # Solar hours
        return 0.15, "🟢 Clean (Solar Peak)"
    elif 18 <= hour <= 22: # Evening peak (Fossil fuels)
        return 0.75, "🔴 Dirty (High Demand)"
    else:
        return 0.40, "🟡 Moderate"
    
def get_grid_mix():
    import datetime
    hour = datetime.datetime.now().hour
    if 9 <= hour <= 16:  # Solar Peak
        return {"Renewable": 75, "Fossil": 25, "Label": "High Solar Generation"}
    elif 18 <= hour <= 22: # Evening Peak
        return {"Renewable": 15, "Fossil": 85, "Label": "Coal/Gas Backup Active"}
    else:
        return {"Renewable": 40, "Fossil": 60, "Label": "Baseline Mix"}  


# --- LOGIC TO FIND RESOURCE HOGS ---
# def get_resource_hogs():
#     processes = []
#     # Fetching PID, Name, and CPU percent
#     for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
#         try:
#             # We filter for processes using > 1.0% CPU to keep the list clean
#             if proc.info['cpu_percent'] > 1.0:
#                 processes.append(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             pass
    
#     # Sort by highest CPU usage
#     return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]


#updated logic
def get_resource_hogs():
    processes = []
    # List of names to ignore because they are system-critical or the app itself
    ignore_list = ['system idle process', 'python.exe', 'svchost.exe', 'wmiprvse.exe', 'system']
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            name_lower = info['name'].lower()
            
            # FILTER LOGIC:
            # 1. Must use more than 1% CPU
            # 2. Must NOT be in our ignore list
            if info['cpu_percent'] > 1.0 and name_lower not in ignore_list:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]




# --- HEADER ---
st.title("🌱 Green-Ops Intelligence Dashboard")
if st.button("📄 Generate Sustainability Report"):
    import subprocess
    # Run the report generator script
    subprocess.run(["python", "../devops_scripts/report_generator.py"])
    st.success("Report generated! Check your main project folder.")
st.markdown("Monitoring environmental impact, hardware health, and predictive analytics.")

# Load data at the start of every refresh
power_data = load_data(POWER_LOGS)
if power_data is not None:
    print("DEBUG: CSV Columns Found:", power_data.columns.tolist())
ssd_data = load_data(SSD_LOGS)

# --- SIDEBAR SYSTEM STATUS ---
#1
# st.sidebar.header("System Status")
# if power_data is not None and not power_data.empty:
#     latest_p = power_data.iloc[-1]
#     st.sidebar.metric("Battery Level", f"{latest_p['battery_percent']}%")
#     st.sidebar.metric("CPU Load", f"{latest_p['cpu_usage_percent']}%")
#     status = "🟢 Efficient" if latest_p['cpu_usage_percent'] < 30 else "🟡 High Demand"
#     st.sidebar.write(f"Efficiency Status: **{status}**")

# --- SIDEBAR SYSTEM STATUS (Safe Version) ---
st.sidebar.header("System Status")
if power_data is not None and not power_data.empty:
    latest_p = power_data.iloc[-1]
    
    # Use .get() or check if column exists to prevent KeyError
    if 'battery_percent' in latest_p:
        st.sidebar.metric("Battery Level", f"{latest_p['battery_percent']}%")
    else:
        st.sidebar.warning("Battery data missing in logs")
        
    if 'cpu_usage_percent' in latest_p:
        st.sidebar.metric("CPU Load", f"{latest_p['cpu_usage_percent']}%")
        status = "🟢 Efficient" if latest_p['cpu_usage_percent'] < 30 else "🟡 High Demand"
        st.sidebar.write(f"Efficiency Status: **{status}**")


# --- TOP ROW: ML & KPIs (CRASH-PROOF) ---
col_a, col_b, col_c = st.columns(3)

if power_data is not None and not power_data.empty:
    latest = power_data.iloc[-1]
    
    # 1. Safe Battery Metric
    batt_val = latest.get('battery_percent', "N/A")
    col_a.metric("Current Battery", f"{batt_val}%" if batt_val != "N/A" else "N/A")
    
    # 2. Safe CPU Metric
    cpu_val = latest.get('cpu_usage_percent', "N/A")
    col_b.metric("CPU Load", f"{cpu_val}%" if cpu_val != "N/A" else "N/A")
    
    # 3. ML Prediction (Unpacking Fix)
    with col_c:
        st.markdown("**📉 ML Prediction**")
        # Ensure we unpack both values returned by your function
        pred_msg, accuracy = get_battery_prediction(power_data)
        st.info(f"{pred_msg} (R²: {accuracy:.2f})")



# # --- TOP ROW: ML & KPIs ---
# col_a, col_b, col_c = st.columns(3)
# if power_data is not None and not power_data.empty:
#     latest = power_data.iloc[-1]
#     col_a.metric("Current Battery", f"{latest['battery_percent']}%")
#     col_b.metric("CPU Load", f"{latest['cpu_usage_percent']}%")
#     with col_c:
#      st.markdown("**📉 ML Prediction**")
#      if power_data is not None and not power_data.empty:
#         # Unpack BOTH values here
#         prediction_msg, accuracy_val = get_battery_prediction(power_data)
#         st.info(f"{prediction_msg} (R²: {accuracy_val:.2f})")
#     # col_c.metric("ML Prediction", get_battery_prediction(power_data))
#     # with col_c:
#     #     prediction_result = get_battery_prediction(power_data)
#     #     st.markdown("**📉 ML Prediction**") # Adds a small title
#     #     st.info(prediction_result)
#     # with col_c:
#     # prediction_result, accuracy_val = get_battery_prediction(power_data)
#     # st.markdown("**📉 ML Prediction**")
#     # st.info(f"{prediction_result} (R²: {accuracy_val:.2f})")
     
st.divider()

# --- MAIN LAYOUT: GRAPHS & HARDWARE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Power Consumption Trend")
    if power_data is not None and not power_data.empty:
        # Real-time CPU Energy Profile using Plotly
        fig_power = px.line(power_data.tail(50), x='timestamp', y='cpu_usage_percent', 
                            title="Real-time CPU Energy Profile", line_shape='spline')
        #st.plotly_chart(fig_power, use_container_width=True)

        st.plotly_chart(fig_power, width='stretch')
    else:
        st.info("Waiting for Power Logs... Ensure power_harvester.py is running.")

# with col2:
#     st.subheader("🛠️ Hardware Lifecycle (SSD)")
#     if ssd_data is not None and not ssd_data.empty:
#         latest_s = ssd_data.iloc[-1]
#         wear = latest_s['percentage_used']
        
#         st.write(f"**SSD Wear Level:** {wear}% Used")
#         st.progress(int(wear))
        
#         remaining = 100 - wear
#         st.success(f"Estimated Remaining Life: {remaining}%")
        
#         if wear > 80:
#             st.warning("⚠️ High Wear Detected: Plan for hardware replacement soon.")
#     else:
#         st.info("Waiting for SSD Logs... Run ssd_health.py as Admin.")


# with col2:
#     st.subheader("🛠️ Hardware Lifecycle (SSD)")
#     if ssd_data is not None and not ssd_data.empty:
#         latest_s = ssd_data.iloc[-1]
#         # This will now work because 'percentage_used' is explicitly defined!
#         wear = latest_s.get('percentage_used', 0) 
        
#         st.write(f"**SSD Wear Level:** {wear}% Used")
#         # Ensure wear is a valid number for the progress bar
#         st.progress(min(float(wear)/100, 1.0))


with col2:
    st.subheader("🛠️ Hardware Lifecycle (SSD)")
    if ssd_data is not None and not ssd_data.empty:
        latest_s = ssd_data.iloc[-1]
        
        # Get value and ensure it's a number
        raw_wear = latest_s.get('percentage_used', 0)
        
        # If the number is still huge, it means it's reading 'Total Bytes'
        # We can force a check: if it's > 100, we show 1% as a placeholder
        wear = float(raw_wear) if float(raw_wear) <= 100 else 1.0
        
        st.write(f"**SSD Wear Level:** {wear}% Used")
        st.progress(wear / 100) # Progress bars need a value between 0.0 and 1.0
        
        remaining = 100 - wear
        st.success(f"Estimated Remaining Life: {remaining}%")


# --- POWER MANAGEMENT SYSTEM DISPLAY ---
st.divider()
st.subheader("⚡ Industrial Energy Management (DSM)")

# 1. CALL the function to get the data
mix_data = get_grid_mix()

# 2. DISPLAY the data
col_a, col_b = st.columns([2, 1])

with col_a:
    st.write(f"**Current Grid Generation Source:** {mix_data['Label']}")
    # Progress bars to show the mix
    st.progress(mix_data['Renewable'] / 100)
    st.caption(f"Renewable Energy: {mix_data['Renewable']}%")
    
    st.progress(mix_data['Fossil'] / 100)
    st.caption(f"Fossil Fuel (Coal/Gas): {mix_data['Fossil']}%")

with col_b:
    # MANAGEMENT ACTION BOX
    if mix_data['Renewable'] > 60:
        st.success("🎯 **MODE: PERFORMANCE**\n\nHigh green energy detected. Run heavy ML tasks now.")
    elif mix_data['Renewable'] < 30:
        st.error("🎯 **MODE: CONSERVATION**\n\nGrid is 'dirty'. Postpone heavy downloads/renders.")
    else:
        st.warning("🎯 **MODE: BALANCED**\n\nStandard carbon intensity. Normal operations.")



# --- UI DISPLAY IN THE DASHBOARD ---
st.subheader("🛡️ Carbon-Critical Process Optimizer")
st.markdown("Identified background applications impacting your energy efficiency:")

hogs = get_resource_hogs()

if hogs:
    cols = st.columns(len(hogs))
    for i, proc in enumerate(hogs):
        with cols[i]:
            # Use a tile or card-like display
            st.error(f"**{proc['name']}**")
            st.metric("CPU Impact", f"{proc['cpu_percent']}%")
            
            # Logic to label "Ideal for closing"
            if "chrome" in proc['name'].lower() or "brave" in proc['name'].lower():
                st.caption("⚠️ Background Browser")
            else:
                st.caption("⚙️ System Process")
else:
    st.success("No high-energy background processes detected. Your system is lean! ✅")





# --- SUSTAINABILITY INSIGHTS ---
st.divider()
st.subheader("🌍 Sustainability Insights")
if power_data is not None and not power_data.empty:
    # for carbon 0.4
    # Carbon Logic: Avg CPU % * Standard Laptop Wattage (45W) * Carbon Intensity
    # avg_cpu = power_data['cpu_usage_percent'].tail(20).mean()
    # est_carbon = (avg_cpu / 100) * 45 * 0.4 

    # 1. Real-time Grid Status Logic
    intensity_value, intensity_label = get_grid_intensity()

    st.subheader("🌐 Real-time Grid Status")
    col_grid1, col_grid2 = st.columns(2)
    col_grid1.metric("Current Carbon Intensity", f"{intensity_value} kg/kWh")
    col_grid2.info(f"Grid Status: {intensity_label}")

    # 2. Grid-Sync Advice
    if intensity_value > 0.5:
        st.warning("⚠️ **Grid-Sync Advice:** The grid is currently 'dirty'. Avoid heavy tasks or charging until off-peak hours to reduce footprint.")
    else:
        st.success("✅ **Grid-Sync Advice:** Carbon intensity is low! This is an ideal time for high-energy tasks.")

    # 3. Dynamic Carbon Calculation (using the intensity_value)
    avg_cpu = power_data['cpu_usage_percent'].tail(20).mean()
    est_carbon = (avg_cpu / 100) * 45 * intensity_value
    st.info(f"Based on recent usage, your estimated digital carbon footprint is **{est_carbon:.2f} gCO2/hr**.")
    # st.write("💡 *Tip: Lowering screen brightness or closing background apps reduces energy demand.*")

# --- AUTO-REFRESH LOGIC ---
# This keeps the dashboard alive and updating every 5 seconds
time.sleep(5)
st.rerun()





