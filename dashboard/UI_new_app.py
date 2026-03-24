# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import time
# import psutil
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from datetime import datetime

# # --- 1. CORPORATE THEMING & LAYOUT ---
# st.set_page_config(page_title="Green-Ops Intelligence", layout="wide", page_icon="🌱")

# # Professional CSS Injection
# st.markdown("""
#     <style>
#     .main { background-color: #f4f7f6; }
#     [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #2e7d32 !important; }
#     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
#     .stTabs [data-baseweb="tab"] { 
#         height: 50px; white-space: pre-wrap; background-color: #f0f2f6; 
#         border-radius: 5px 5px 0 0; gap: 1px; padding: 10px;
#     }
#     .stTabs [aria-selected="true"] { background-color: #e8f5e9 !important; border-bottom: 3px solid #2e7d32 !important; }
#     div.stButton > button:first-child {
#         background-color: #2e7d32; color: white; border: none; width: 100%;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # --- 2. LOGIC FUNCTIONS (Ensuring 2-value returns) ---
# def get_battery_prediction(df):
#     if df is None or len(df) < 15:
#         return "Analyzing Patterns...", 0.0
    
#     df_ml = df.copy()
#     df_ml['id'] = range(len(df_ml))
#     X, y = df_ml[['id']].values, df_ml['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
#     accuracy = r2_score(y, model.predict(X))
#     slope = model.coef_[0]
    
#     if slope >= 0: return "⚡ Charging/Stable", accuracy
    
#     mins_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
#     return f"📉 ~{round(mins_left, 1)}m remain", accuracy

# def get_resource_hogs():
#     processes = []
#     ignore = ['system idle process', 'python.exe', 'svchost.exe', 'wmiprvse.exe', 'system']
#     for proc in psutil.process_iter(['name', 'cpu_percent']):
#         try:
#             if proc.info['cpu_percent'] > 1.5 and proc.info['name'].lower() not in ignore:
#                 processes.append(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied): continue
#     return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

# # --- 3. SIDEBAR & DATA LOADING ---
# with st.sidebar:
#     st.image("https://cdn-icons-png.flaticon.com/512/2942/2942531.png", width=80) # Generic Green Icon
#     st.title("Control Center")
#     if st.button("📄 Generate Audit Report"):
#         st.toast("Compiling ESG Data...")
#         # os.system("python ../devops_scripts/report_generator.py")
    
#     st.divider()
#     st.caption("Active Instance: " + os.environ.get('COMPUTERNAME', 'LocalNode'))

# # Updated paths for directory structure
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# def load_data(path):
#     return pd.read_csv(path) if os.path.exists(path) else None

# power_data = load_data(POWER_LOGS)
# ssd_data = load_data(SSD_LOGS)

# # --- 4. MAIN INTERFACE ---
# st.markdown("# 🌱 Green-Ops Intelligence Platform")
# st.markdown("### Asset Sustainability & Lifecycle Management")

# # KPI Ribbon (Top Row)
# kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# if power_data is not None and not power_data.empty:
#     latest = power_data.iloc[-1]
#     kpi1.metric("Battery State", f"{latest['battery_percent']}%")
#     kpi2.metric("Current Load", f"{latest['cpu_usage_percent']}%")
    
#     # ML Prediction Call (Fixed Unpacking)
#     pred_msg, acc = get_battery_prediction(power_data)
#     kpi3.metric("ML Est. Runtime", pred_msg)
#     kpi4.metric("Model Confidence", f"{int(acc*100)}%")

# st.divider()

# # Tabbed Analytics
# tab_telemetry, tab_lifecycle, tab_esg = st.tabs(["📊 Real-time Telemetry", "🛠️ Asset Health", "🌍 ESG Compliance"])

# with tab_telemetry:
#     col_chart, col_alerts = st.columns([2, 1])
#     with col_chart:
#         st.subheader("Energy Demand Profile")
#         if power_data is not None:
#             fig = px.area(power_data.tail(50), x='timestamp', y='cpu_usage_percent', 
#                           template="plotly_white", color_discrete_sequence=['#2e7d32'])
#             fig.update_layout(height=400, margin=dict(l=0,r=0,b=0,t=0))
#             st.plotly_chart(fig, use_container_width=True)
    
#     with col_alerts:
#         st.subheader("Resource Optimization")
#         hogs = get_resource_hogs()
#         for h in hogs:
#             st.error(f"**{h['name']}** is consuming **{h['cpu_percent']}%** CPU")

# with tab_lifecycle:
#     st.subheader("Hardware Degradation Analysis")
#     if ssd_data is not None:
#         wear = ssd_data.iloc[-1]['percentage_used']
#         st.write(f"SSD Health Remaining: **{100-wear}%**")
#         st.progress(100-int(wear))
#     else:
#         st.info("Run hardware scanners to view lifecycle data.")

# with tab_esg:
#     st.subheader("Sustainability Audit Metrics")
#     st.info("Dynamic Carbon Intensity tracking and Grid-Sync logic available in report export.")

# # Auto-Refresh
# time.sleep(5)
# st.rerun()


#draft2
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import time
# import psutil
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from datetime import datetime

# # --- 1. GLOBAL INTERFACE CONFIGURATION ---
# st.set_page_config(
#     page_title="Green-Ops Intelligence | Enterprise Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- 2. ADVANCED CSS INJECTION (The "Secret Sauce") ---
# st.markdown("""
#     <style>
#     /* Main Background & Font */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
#     html, body, [class*="css"]  {
#         font-family: 'Inter', sans-serif;
#         background-color: #F8FAFC;
#     }

#     /* Metric Card Styling */
#     div[data-testid="stMetric"] {
#         background-color: #ffffff;
#         border: 1px solid #E2E8F0;
#         padding: 15px 20px;
#         border-radius: 12px;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#     }

#     /* Horizontal Metric Styling */
#     [data-testid="stMetricValue"] {
#         font-size: 2.2rem !important;
#         font-weight: 700 !important;
#         color: #0F172A !important;
#     }

#     /* Sidebar Professionalism */
#     section[data-testid="stSidebar"] {
#         background-color: #0F172A !important;
#         color: white;
#     }
    
#     section[data-testid="stSidebar"] .stMarkdown {
#         color: #94A3B8;
#     }

#     /* Button Styling */
#     .stButton>button {
#         width: 100%;
#         border-radius: 8px;
#         height: 3em;
#         background-color: #10B981;
#         color: white;
#         border: none;
#         transition: all 0.3s ease;
#     }
#     .stButton>button:hover {
#         background-color: #059669;
#         transform: translateY(-2px);
#     }

#     /* Tabs Styling */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         background-color: #F1F5F9;
#         border-radius: 8px 8px 0 0;
#         padding: 10px 20px;
#         color: #475569;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: #ffffff !important;
#         color: #10B981 !important;
#         font-weight: 700;
#     }
#     </style>
#     """, unsafe_allow_html=True)
# def get_grid_intensity():
#     hour = datetime.now().hour
#     if 9 <= hour <= 16: 
#         return 0.15, "🟢 Clean (Solar Peak)", "Low"
#     elif 18 <= hour <= 22:
#         return 0.75, "🔴 Dirty (High Demand)", "Critical"
#     else:
#         return 0.40, "🟡 Moderate", "Nominal"

# def get_grid_mix():
#     hour = datetime.now().hour
#     if 9 <= hour <= 16:
#         return {"Renewable": 75, "Fossil": 25, "Status": "Optimal"}
#     elif 18 <= hour <= 22:
#         return {"Renewable": 15, "Fossil": 85, "Status": "Fossil-Heavy"}
#     else:
#         return {"Renewable": 40, "Fossil": 60, "Status": "Balanced"}
# # --- 3. CORE ANALYTICS ENGINE ---
# def get_battery_prediction(df):
#     if df is None or len(df) < 15:
#         return "Calibrating Sensors...", 0.0
    
#     df_ml = df.copy()
#     df_ml['id'] = range(len(df_ml))
#     X, y = df_ml[['id']].values, df_ml['battery_percent'].values
    
#     model = LinearRegression().fit(X, y)
#     accuracy = r2_score(y, model.predict(X))
#     slope = model.coef_[0]
    
#     if slope >= 0: return "⚡ Grid Connected", accuracy
    
#     mins_left = (-model.intercept_ / slope - len(df_ml)) * (10 / 60)
#     return f"📉 ~{round(mins_left, 1)}m Remaining", accuracy

# def get_resource_hogs():
#     processes = []
#     ignore = ['system idle process', 'python.exe', 'svchost.exe', 'wmiprvse.exe', 'system', 'streamlit']
#     for proc in psutil.process_iter(['name', 'cpu_percent']):
#         try:
#             if proc.info['cpu_percent'] > 1.0 and proc.info['name'].lower() not in ignore:
#                 processes.append(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied): continue
#     return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:4]

# # --- 4. DATA ORCHESTRATION ---
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# def load_data(path):
#     return pd.read_csv(path) if os.path.exists(path) else None

# power_data = load_data(POWER_LOGS)
# ssd_data = load_data(SSD_LOGS)

# # --- 5. SIDEBAR NAVIGATION ---
# with st.sidebar:
#     st.markdown("### 🏢 Enterprise Control")
#     st.caption("Green-Ops v3.0 | March 2026")
#     st.divider()
    
#     st.markdown("#### ⚙️ Data Management")
#     if st.button("📊 Export ESG Audit Report"):
#         st.toast("Generating PDF Report...")
#         # Add your report generator logic here
        
#     st.divider()
#     st.markdown("#### 📡 System Node")
#     st.code(os.environ.get('COMPUTERNAME', 'LOCAL_HOST'))
#     st.info("Status: Fully Operational")

# # --- 6. MAIN DASHBOARD CONTENT ---
# # Header Section
# col_header, col_status = st.columns([4, 1])
# with col_header:
#     st.markdown("# 🟢 Green-Ops Intelligence Platform")
#     st.markdown("*Real-time Telemetry, Predictive Analytics, and ESG Compliance Auditing*")

# # Top Ribbon KPIs
# st.markdown("---")
# kpi1, kpi2, kpi3, kpi4 ,kpi5 = st.columns(5)

# if power_data is not None and not power_data.empty:
#     latest = power_data.iloc[-1]
#     kpi1.metric("Battery Integrity", f"{latest['battery_percent']}%", delta="-0.2%")
#     kpi2.metric("Processing Load", f"{latest['cpu_usage_percent']}%", delta="Steady")
    
#     msg, acc = get_battery_prediction(power_data)
#     kpi3.metric("Predictive Runtime", msg)
#     kpi4.metric("ML Accuracy", f"{int(acc*100)}%", delta="High")
#     kpi5.metric("ML Accuracy", f"{int(acc*100)}%")

# # Analytics Tabs
# st.markdown("###")
# tab_main, tab_health, tab_esg = st.tabs(["📊 Performance Matrix", "🛡️ Asset Lifecycle", "🌍 Sustainability"])

# with tab_main:
#     col_viz, col_proc = st.columns([2, 1])
    
#     with col_viz:
#         st.markdown("#### Power Utilization Signature")
#         if power_data is not None:
#             fig = px.area(power_data.tail(60), x='timestamp', y='cpu_usage_percent',
#                          template="simple_white", color_discrete_sequence=['#10B981'])
#             fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10))
#             st.plotly_chart(fig, use_container_width=True)
#         st.markdown("---")
#     st.markdown("#### 🌐 Real-time Grid Intelligence")
#     mix = get_grid_mix()
    
#     c1, c2 = st.columns([2, 1])
#     with c1:
#         st.write(f"**Current Grid Composition:** {mix['Status']}")
#         st.progress(mix['Renewable'] / 100)
#         st.caption(f"Renewable Energy Contribution: {mix['Renewable']}%")
#     with c2:
#         if mix['Renewable'] > 50:
#             st.success("✅ **Green Mode Active**\nIdeal for heavy computation.")
#         else:
#             st.error("⚠️ **Dirty Grid Detected**\nPostpone non-essential tasks.")    
            
#     # with col_proc:
#     #     st.markdown("#### Active Carbon Hogs")
#     #     hogs = get_resource_hogs()
#     #     if hogs:
#     #         for h in hogs:
#     #             with st.expander(f"{h['name']}", expanded=True):
#     #                 st.progress(h['cpu_percent']/100)
#     #                 st.caption(f"Impact Score: {h['cpu_percent']}% CPU Utilization")
#     #     else:
#     #         st.success("System optimized. No high-energy processes detected.")
#     with col_proc:
#         st.markdown("#### Active Carbon Hogs")
#         hogs = get_resource_hogs()
#         if hogs:
#             for h in hogs:
#                 with st.expander(f"{h['name']}", expanded=True):
#                 # CLIP the value: Ensure it stays between 0.0 and 1.0
#                     cpu_val = min(float(h['cpu_percent'] / 100), 1.0)
                
#                     st.progress(cpu_val)
#                     st.caption(f"Impact Score: {h['cpu_percent']}% CPU Utilization")

# with tab_health:
#     st.markdown("#### Predictive Hardware Degradation")
#     if ssd_data is not None:
#         wear = ssd_data.iloc[-1]['percentage_used']
#         col_ssd1, col_ssd2 = st.columns(2)
#         with col_ssd1:
#             st.write("SSD Remaining Useful Life (RUL)")
#             st.progress(100-int(wear))
#         with col_ssd2:
#             st.metric("Percentage Used", f"{wear}%", delta="Increasing", delta_color="inverse")
#     else:
#         st.warning("Hardware telemetry missing. Please run ssd_health.py as Administrator.")

# with tab_esg:
#     st.markdown("#### Dynamic ESG Compliance Metrics")
#     st.info("Carbon Intensity tracking is currently mapped to Grid Real-time Data. Export the audit report for full CO2 breakdown.")

# # --- 7. AUTO-REFRESH LOGIC ---
# st.markdown("---")
# st.caption("Dashboard auto-syncing every 5 seconds...")
# time.sleep(5)
# st.rerun()



#3
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import time
# import psutil
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from datetime import datetime

# # --- 1. SOVEREIGN THEME & GLASSMORPHISM CSS ---
# st.set_page_config(page_title="Green-Ops Sovereign", layout="wide", initial_sidebar_state="collapsed")

# st.markdown("""
#     <style>
#     /* Global Dark Theme */
#     [data-testid="stAppViewContainer"] {
#         background: radial-gradient(circle at top left, #0f172a, #020617);
#         color: #f8fafc;
#     }
    
#     /* Header Styling */
#     .main-title {
#         font-size: 3rem;
#         font-weight: 800;
#         background: -webkit-linear-gradient(#10b981, #059669);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0px;
#     }

#     /* Vertical Flip Card Container */
#     .flip-container {
#         perspective: 1000px;
#         margin-bottom: 20px;
#         height: 250px;
#     }
#     .flip-card {
#         position: relative;
#         width: 100%;
#         height: 100%;
#         transition: transform 0.6s;
#         transform-style: preserve-3d;
#         cursor: pointer;
#     }
#     .flip-container:hover .flip-card {
#         transform: rotateY(180deg);
#     }
#     .flip-front, .flip-back {
#         position: absolute;
#         width: 100%;
#         height: 100%;
#         backface-visibility: hidden;
#         border-radius: 15px;
#         border: 1px solid rgba(16, 185, 129, 0.2);
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#         align-items: center;
#         padding: 20px;
#     }
#     .flip-front {
#         background: rgba(30, 41, 59, 0.7);
#         backdrop-filter: blur(10px);
#     }
#     .flip-back {
#         background: linear-gradient(135deg, #065f46 0%, #064e3b 100%);
#         transform: rotateY(180deg);
#         text-align: center;
#     }

#     /* KPI Glow Metrics */
#     .metric-box {
#         background: rgba(15, 23, 42, 0.8);
#         border-top: 3px solid #10b981;
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);
#     }
    
#     /* Remove white backgrounds from Streamlit defaults */
#     .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
#     div[data-testid="stExpander"] { background: transparent; border: 1px solid #10b981; }
#     </style>
#     """, unsafe_allow_html=True)

# # --- 2. INTELLIGENCE ENGINE ---
# def get_grid_intel():
#     hour = datetime.now().hour
#     if 9 <= hour <= 16: return "LOW", "CLEAN (SOLAR)", 0.15
#     elif 18 <= hour <= 22: return "HIGH", "DIRTY (FOSSIL)", 0.75
#     else: return "MID", "MODERATE", 0.40

# def get_battery_prediction(df):
#     if df is None or len(df) < 15: return "Calibrating...", 0.0
#     X = [[i] for i in range(len(df))]
#     y = df['battery_percent'].values
#     model = LinearRegression().fit(X, y)
#     acc = r2_score(y, model.predict(X))
#     slope = model.coef_[0]
#     if slope >= 0: return "⚡ Grid Powered", acc
#     mins = (-model.intercept_ / slope - len(df)) * (10 / 60)
#     return f"📉 ~{round(mins, 1)}m RUL", acc

# # --- 3. DATA LOADING ---
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# def load_data(): return pd.read_csv(POWER_LOGS) if os.path.exists(POWER_LOGS) else None
# data = load_data()

# # --- 4. SOVEREIGN UI LAYOUT ---
# st.markdown('<p class="main-title">GREEN-OPS SOVEREIGN v4.0</p>', unsafe_allow_html=True)
# st.markdown("##### *Enterprise-Grade ESG Monitoring & AI Lifecycle Analytics*")
# st.markdown("---")

# # Row 1: Vertical Flip Cards (Replacing simple text)
# col1, col2, col3, col4 = st.columns(4)

# grid_val, grid_lbl, intensity = get_grid_intel()
# pred_msg, acc = get_battery_prediction(data)

# with col1:
#     st.markdown(f"""
#         <div class="flip-container">
#             <div class="flip-card">
#                 <div class="flip-front">
#                     <h3 style="color:#10b981;">🌍 GRID STATUS</h3>
#                     <p>{grid_val}</p>
#                 </div>
#                 <div class="flip-back">
#                     <p>Current intensity: <b>{intensity} kg/kWh</b></p>
#                     <p>{grid_lbl}</p>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""
#         <div class="flip-container">
#             <div class="flip-card">
#                 <div class="flip-front">
#                     <h3 style="color:#10b981;">🧠 AI PREDICTION</h3>
#                     <p>{pred_msg.split(' ')[0]}</p>
#                 </div>
#                 <div class="flip-back">
#                     <p>Model Confidence: <b>{int(acc*100)}%</b></p>
#                     <p>{pred_msg}</p>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown(f"""
#         <div class="flip-container">
#             <div class="flip-card">
#                 <div class="flip-front">
#                     <h3 style="color:#10b981;">🔋 BATTERY</h3>
#                     <p>{data.iloc[-1]['battery_percent'] if data is not None else '0'}%</p>
#                 </div>
#                 <div class="flip-back">
#                     <p>State of Health: <b>Optimal</b></p>
#                     <p>Voltage fluctuation: <b>Nominal</b></p>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with col4:
#     st.markdown(f"""
#         <div class="flip-container">
#             <div class="flip-card">
#                 <div class="flip-front">
#                     <h3 style="color:#10b981;">⚡ LOAD</h3>
#                     <p>{data.iloc[-1]['cpu_usage_percent'] if data is not None else '0'}%</p>
#                 </div>
#                 <div class="flip-back">
#                     <p>Processing Demand: <b>High</b></p>
#                     <p>Mode: <b>Balanced Performance</b></p>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# # Row 2: Graph (Full Width Glow Effect)
# st.markdown("### 📊 Energy Consumption Signature")
# if data is not None:
#     fig = px.area(data.tail(60), x='timestamp', y='cpu_usage_percent', template="plotly_dark")
#     fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.2)')
#     fig.update_layout(
#         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
#     )
#     st.plotly_chart(fig, use_container_width=True)

# # Footer Info
# st.markdown("---")
# st.caption("Active Monitoring | Real-time Grid Sync Enabled | AI Engine v4.0")

# # Auto-Refresh
# time.sleep(5)
# st.rerun()

#4
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os
# import time
# import psutil
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from datetime import datetime

# # --- 1. SOVEREIGN THEME & 3D INTERACTIVE CSS ---
# st.set_page_config(page_title="Green-Ops Sovereign v4.0", layout="wide", initial_sidebar_state="collapsed")

# st.markdown("""
#     <style>
#     /* Global Dark Master */
#     [data-testid="stAppViewContainer"] {
#         background: radial-gradient(circle at top left, #0f172a, #020617);
#         color: #f8fafc;
#     }
    
#     .main-title {
#         font-size: 3.2rem;
#         font-weight: 800;
#         background: -webkit-linear-gradient(#10b981, #34d399);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0px;
#     }

#     /* Vertical Flip Card Logic */
#     .flip-container { perspective: 1000px; margin-bottom: 25px; height: 220px; }
#     .flip-card {
#         position: relative; width: 100%; height: 100%;
#         transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer;
#     }
#     .flip-container:hover .flip-card { transform: rotateY(180deg); }
#     .flip-front, .flip-back {
#         position: absolute; width: 100%; height: 100%;
#         backface-visibility: hidden; border-radius: 15px;
#         border: 1px solid rgba(16, 185, 129, 0.3);
#         display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px;
#     }
#     .flip-front { background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(12px); }
#     .flip-back { 
#         background: linear-gradient(135deg, #065f46 0%, #064e3b 100%); 
#         transform: rotateY(180deg); color: white; font-size: 0.9rem;
#     }

#     /* Progress Bar Customization */
#     .stProgress > div > div > div > div { background-color: #10b981; }
    
#     /* Clean up Streamlit UI */
#     footer {visibility: hidden;}
#     #MainMenu {visibility: hidden;}
#     </style>
#     """, unsafe_allow_html=True)

# # --- 2. COMPLETE BACKEND LOGIC ---

# def get_grid_intel():
#     hour = datetime.now().hour
#     if 9 <= hour <= 16: return "LOW", "CLEAN (SOLAR PEAK)", 0.15, 75
#     elif 18 <= hour <= 22: return "HIGH", "DIRTY (FOSSIL PEAK)", 0.75, 15
#     else: return "MID", "MODERATE MIX", 0.40, 45

# def get_battery_prediction(df):
#     if df is None or len(df) < 15: return "CALIBRATING...", 0.0
#     X = [[i] for i in range(len(df))]
#     y = df['battery_percent'].values
#     model = LinearRegression().fit(X, y)
#     acc = r2_score(y, model.predict(X))
#     slope = model.coef_[0]
#     if slope >= 0: return "⚡ GRID POWERED", acc
#     mins = (-model.intercept_ / slope - len(df)) * (10 / 60)
#     return f"📉 ~{round(mins, 1)}m RUL", acc

# def get_resource_hogs():
#     processes = []
#     ignore = ['system idle process', 'python.exe', 'svchost.exe', 'system', 'streamlit']
#     for proc in psutil.process_iter(['name', 'cpu_percent']):
#         try:
#             if proc.info['cpu_percent'] > 1.0 and proc.info['name'].lower() not in ignore:
#                 processes.append(proc.info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied): continue
#     return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]

# # --- 3. DATA ORCHESTRATION ---
# POWER_LOGS = "../data_collection/hardware_logs.csv"
# SSD_LOGS = "../data_collection/ssd_health_logs.csv"

# def load_data(path): return pd.read_csv(path) if os.path.exists(path) else None

# power_data = load_data(POWER_LOGS)
# ssd_data = load_data(SSD_LOGS)

# # --- 4. DASHBOARD PRESENTATION ---

# st.markdown('<p class="main-title">GREEN-OPS SOVEREIGN</p>', unsafe_allow_html=True)
# st.markdown("##### *Sustainable Intelligence & Predictive Hardware Lifecycle Management*")
# st.markdown("---")

# # ROW 1: THE INTERACTIVE CORE (Flip Cards)
# col1, col2, col3, col4 = st.columns(4)

# grid_val, grid_lbl, intensity, renew_pct = get_grid_intel()
# pred_msg, acc = get_battery_prediction(power_data)
# latest_p = power_data.iloc[-1] if power_data is not None else None

# with col1:
#     st.markdown(f"""<div class="flip-container"><div class="flip-card">
#         <div class="flip-front"><h3 style="color:#10b981;">🌍 GRID</h3><p style="font-size:1.5rem;">{grid_val}</p></div>
#         <div class="flip-back"><b>{grid_lbl}</b><br>Intensity: {intensity}kg/kWh<br>Renewables: {renew_pct}%</div>
#     </div></div>""", unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""<div class="flip-container"><div class="flip-card">
#         <div class="flip-front"><h3 style="color:#10b981;">🧠 AI PREDICT</h3><p style="font-size:1.5rem;">{int(acc*100)}%</p></div>
#         <div class="flip-back"><b>Model Confidence</b><br>{pred_msg}<br>R² Accuracy: {round(acc,3)}</div>
#     </div></div>""", unsafe_allow_html=True)

# with col3:
#     batt = latest_p['battery_percent'] if latest_p is not None else 0
#     st.markdown(f"""<div class="flip-container"><div class="flip-card">
#         <div class="flip-front"><h3 style="color:#10b981;">🔋 BATTERY</h3><p style="font-size:1.5rem;">{batt}%</p></div>
#         <div class="flip-back"><b>Health Status: Optimal</b><br>Voltage: Nominal<br>Cycle Count: Stable</div>
#     </div></div>""", unsafe_allow_html=True)

# with col4:
#     load = latest_p['cpu_usage_percent'] if latest_p is not None else 0
#     st.markdown(f"""<div class="flip-container"><div class="flip-card">
#         <div class="flip-front"><h3 style="color:#10b981;">⚡ LOAD</h3><p style="font-size:1.5rem;">{load}%</p></div>
#         <div class="flip-back"><b>Current Demand</b><br>Thermal State: Normal<br>Efficiency: High</div>
#     </div></div>""", unsafe_allow_html=True)

# # ROW 2: ANALYTICS MATRIX
# st.markdown("###")
# col_viz, col_side = st.columns([2, 1])

# with col_viz:
#     st.markdown("#### 📊 Energy Consumption Signature")
#     if power_data is not None:
#         fig = px.area(power_data.tail(60), x='timestamp', y='cpu_usage_percent', template="plotly_dark")
#         fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.2)')
#         fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
#         st.plotly_chart(fig, use_container_width=True)

# with col_side:
#     st.markdown("#### 🛡️ Active Carbon Hogs")
#     hogs = get_resource_hogs()
#     if hogs:
#         for h in hogs:
#             st.caption(f"{h['name']} | {h['cpu_percent']}%")
#             st.progress(min(float(h['cpu_percent']/100), 1.0))
#     else:
#         st.success("System Optimized ✅")
    
#     st.markdown("---")
#     st.markdown("#### 🛠️ SSD Lifecycle")
#     if ssd_data is not None:
#         wear = ssd_data.iloc[-1]['percentage_used']
#         st.caption(f"Hardware Wear: {wear}%")
#         st.progress(wear/100)
#     else:
#         st.info("Run SSD Harvester as Admin")

# # FOOTER
# st.markdown("---")
# col_f1, col_f2 = st.columns(2)
# col_f1.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')} | Sync Active")
# if col_f2.button("🚀 Generate Journal-Ready Audit"):
#     st.toast("Compiling ESG metrics and ML weights...")

# # REFRESH
# time.sleep(5)
# st.rerun()


#5
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import psutil
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime

# --- 1. SOVEREIGN THEME & HUD-DISPLAY CSS ---
# Using wide layout and a unique page icon (maybe a stylized tree)
st.set_page_config(page_title="Green-Ops Sovereign v4.1", layout="wide", initial_sidebar_state="collapsed", page_icon="🌲")

st.markdown("""
    <style>
    /* GLOBAL DARK MASTER & BACKGROUND TEXTURE */
    /* Link to a high-quality dark abstract pattern */
    [data-testid="stAppViewContainer"] {
        background-color: #020617; /* Deepest black */
        background-image: url('https://www.transparenttextures.com/patterns/dark-geometric.png'); /* Subtle pattern */
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* REMOVING TOP STREAMLIT BARS & MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* MAIN TYPOGRAPHY HEADERS */
    .title-ribbon {
        font-family: 'Inter', sans-serif; /* Modern, clean font */
        padding: 30px 0px 10px 0px;
        margin-bottom: 0px;
        border-bottom: 2px solid rgba(52, 211, 153, 0.2); /* Thin emerald trace */
    }
    
    .super-title {
        font-size: 6rem; /* Extremely large and dominant */
        font-weight: 900;
        line-height: 1.1;           
        background: -webkit-linear-gradient(#10b981, #34d399); /* Green to emerald gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .sub-title {
        font-size: 2rem;
        color: #94a3b8; /* Cool grey-blue */
        font-weight: 500;
        margin-top: 0px;
        letter-spacing: 1px;
    }

    /* CARD DESIGN: Trace Border & Glow */
    .metric-card {
        background: rgba(15, 23, 42, 0.85); /* Frosty glass */
        backdrop-filter: blur(8px);
        border: 1px solid rgba(16, 185, 129, 0.2); /* Faint green trace */
        padding: 25px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        transition: all 0.2s ease-in-out;
        margin-bottom: 20px;
        height: 100%;
    }
    .metric-card:hover {
        border: 1px solid rgba(16, 185, 129, 0.5);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1), 0 4px 6px -2px rgba(16, 185, 129, 0.05);
        transform: translateY(-2px);
    }
    
    .card-label {
        font-size: 1.1rem;
        color: #f1f5f9;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    .card-value {
        font-size: 2.8rem;
        color: #10b981; /* Emerald */
        font-weight: 700;
        margin-bottom: -5px;
    }
    .card-delta {
        font-size: 0.9rem;
        color: #34d399; /* Mint */
    }

    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ANALYTICS LOGIC ---
# Updated path - ensured correct backslash for multi-platform
LOGS_PATH = os.path.join("..", "data_collection", "hardware_logs.csv")

def load_power_data():
    if os.path.exists(LOGS_PATH):
        try:
            return pd.read_csv(LOGS_PATH)
        except Exception as e:
            st.error(f"Error loading logs: {e}")
    return None

def get_grid_impact():
    hour = datetime.now().hour
    # Mocking logic based on standard peak/off-peak grid cycles
    if 10 <= hour <= 15: # Solar Peak (Mid-day)
        return "OPTIMAL", "Clean Supply Active"
    elif 18 <= hour <= 21: # Evening Peak (Fossil-heavy)
        return "CRITICAL", "High Demand Detected"
    else:
        return "BALANCED", "Standard Grid Mix"

def get_ml_forecast(df):
    if df is None or len(df) < 15: # Minimum data threshold
        return "CALIBRATING...", 0.0
    
    df_forecast = df.copy()
    df_forecast['id'] = range(len(df_forecast))
    X = df_forecast[['id']].values
    y = df_forecast['battery_percent'].values
    
    # Simple linear model to predict battery wear curve
    model = LinearRegression().fit(X, y)
    accuracy = r2_score(y, model.predict(X)) # R² score
    slope = model.coef_[0]
    
    if slope >= 0:
        return "⚡ GRID STABLE", accuracy
    
    # Minutes remaining based on negative slope
    # Assumes 10-second data interval
    minutes_left = (-model.intercept_ / slope - len(df_forecast)) * (10 / 60)
    return f"📈 ~{round(minutes_left, 1)}m RUL", accuracy

# --- 3. DATA HARVESTING ---
power_logs = load_power_data()

# --- 4. PRESENTATION LAYER ---
# HEADER SECTION
st.markdown("""
    <div class="title-ribbon">
        <p class="super-title">GREEN-OPS SOVEREIGN</p>
        <p class="sub-title">Enterprise Sustainability Intelligence & Predictive Hardware Lifecycle Management</p>
    </div>
    """, unsafe_allow_html=True)

# Top KPI Ribbon
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

if power_logs is not None and not power_logs.empty:
    latest = power_logs.iloc[-1]
    
    # Calling the internal intelligence functions
    impact, impact_msg = get_grid_impact()
    ml_msg, ml_acc = get_ml_forecast(power_logs)

    # 1. GRID STATUS CARD (Minimalist, no emoji)
    with kpi1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="card-label">GRID STATUS</div>
                <div class="card-value">{impact}</div>
                <div class="card-delta">{impact_msg}</div>
            </div>
            """, unsafe_allow_html=True)

    # 2. AI PREDICT CARD
    with kpi2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="card-label">ML FORECAST</div>
                <div class="card-value">{int(ml_acc * 100)}%</div>
                <div class="card-delta">Confidence: R² {round(ml_acc,3)}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. BATTERY CARD
    with kpi3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="card-label">INTEGRITY</div>
                <div class="card-value">{latest['battery_percent']}%</div>
                <div class="card-delta">State of Health: Stable</div>
            </div>
            """, unsafe_allow_html=True)

    # 4. LOAD CARD
    with kpi4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="card-label">COMPUTE LOAD</div>
                <div class="card-value">{latest['cpu_usage_percent']}%</div>
                <div class="card-delta">Status: Optimized</div>
            </div>
            """, unsafe_allow_html=True)

else:
    kpi1.warning(" telemetry missing.")
    # Show placeholders or error if no data loaded

# ANALYTICS MATRIX SECTION
st.markdown("---")
st.markdown("### 📊 Active Telemetry Stream")
col_chart, col_side = st.columns([3, 1])

with col_chart:
    st.subheader("Energy Demand Profile (CPU)")
    if power_logs is not None:
        fig = px.area(power_logs.tail(60), x='timestamp', y='cpu_usage_percent', template="plotly_dark")
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.15)')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.subheader("Carbon Hogs")
    # Add a simplified process logic display if psutil data available
    ignore = ['system idle process', 'python.exe', 'svchost.exe']
    hogs = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 1.0 and proc.info['name'].lower() not in ignore:
                hogs.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue
    
    if hogs:
        for h in sorted(hogs, key=lambda x: x['cpu_percent'], reverse=True)[:3]:
            st.error(f"{h['name']} - {h['cpu_percent']}%")
    else:
        st.success("Lean profile")

# AUTO-REFRESH LOGIC
st.markdown("---")
col_sync, col_ref = st.columns(2)
col_sync.caption(f"Sync Active | Updated: {datetime.now().strftime('%H:%M:%S')}")

# --- 5. ENTERPRISE CONTROL & REPORTING ---
st.markdown("---")
col_info, col_action = st.columns([3, 1])

with col_info:
    st.markdown("#### 🛡️ Compliance & Audit Log")
    st.caption(f"System Instance: {os.environ.get('COMPUTERNAME', 'LOCAL_NODE')} | Data Integrity: Verified")
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')} | Frequency: 5.0s")

with col_action:
    # A professional, high-contrast button for the Audit Report
    if st.button("🚀 GENERATE ESG AUDIT", help="Click to compile all ML and Hardware logs into a formal report"):
        with st.spinner("Compiling Sovereignty Metrics..."):
            try:
                import subprocess
                # This runs your external report script
                # Ensure the path to your report_generator.py is correct
                result = subprocess.run(["python", "../devops_scripts/report_generator.py"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.toast("Success: Report Generated!", icon="✅")
                    st.success("Audit Report saved to Project Root.")
                else:
                    st.error("Report Generation Failed.")
                    st.info(f"Debug: {result.stderr}")
            except Exception as e:
                st.error(f"Internal Error: {e}")

time.sleep(5)
st.rerun()