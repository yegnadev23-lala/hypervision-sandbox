import streamlit as st
import psutil
import os
from modules.vm_controller import get_vm_status, control_vm
from modules.file_analyzer import calculate_hashes, analyze_file_heuristics

st.set_page_config(page_title="HyperVision CyberLab", page_icon="🛡️", layout="wide")

# Custom Dark Theme Styling matching Pro SOC Dashboards
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    .metric-card { background-color: #111827; border: 1px solid #1f2937; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Top Bar Header
col_h1, col_h2, col_h3 = st.columns([3, 6, 3])
with col_h1:
    st.markdown("### 🛡️ HyperVision CyberLab")
with col_h2:
    st.caption("Dashboard Version: 1.0.0_Stable | Mode: Hybrid Sandbox Agent")
with col_h3:
    st.markdown("🟢 **Status: Protected**")

st.markdown("---")

# Main Navigation Tabs (SOC style)
tab_dash, tab_siem, tab_vm, tab_files = st.tabs([
    "📊 Lab Dashboard", 
    "🚨 SIEM & Events", 
    "💻 VM & Snapshot Manager", 
    "📂 Malware Analysis Vault"
])

with tab_dash:
    st.subheader("Server Health & Telemetry")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Host CPU Usage", f"{psutil.cpu_percent(interval=0.5)}%")
    with c2:
        st.metric("Host RAM Usage", f"{psutil.virtual_memory().percent}%")
    with c3:
        st.metric("Sandbox VM State", get_vm_status("HyperVision-VM"))
    with c4:
        st.metric("Active Shield", "Online 🟢", "All Browsers Monitored")

    st.markdown("---")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("System Incidents & Telemetry Logs")
        st.info("System operating normally. No host anomalies detected.")
    with col_b:
        st.subheader("Sandbox VM Quick Slot")
        vm_action = st.selectbox("Action", ["Select Action...", "Start VM", "Power Off", "Revert to Snapshot"])
        if st.button("Execute Command"):
            if vm_action != "Select Action...":
                res = control_vm(vm_action, "HyperVision-VM")
                if res.get("success"):
                    st.success(f"Successfully executed: {vm_action}")
                else:
                    st.error(f"Error: {res.get('error')}")

with tab_siem:
    st.subheader("SIEM Alert Center & Event Timeline")
    s1, s2, s3, s4 = st.columns(4)
    s1.error("Critical Alerts: 0")
    s2.warning("High Alerts: 2")
    s3.info("Medium Alerts: 5")
    s4.success("Low Alerts: 12")
    
    st.markdown("### Active Security Events")
    st.markdown("""
    | Time | Alert Type | Severity | Source IP / Target | Status |
    | :--- | :--- | :--- | :--- | :--- |
    | 2:17 AM | Multiple Failed Logins | Medium | 197.162.38.20 | Open |
    | 11:45 PM | Suspicious File Download | High | 10.1.20.25 | Under Review |
    | 11:15 PM | Unusual Network Activity | Low | 172.16.8.12 | Resolved |
    """)

with tab_vm:
    st.subheader("Virtual Machine Snapshot Manager & Isolation")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**Current VM Node:** `HyperVision-VM`")
        st.markdown("**Snapshot Baseline:** `Fresh-Install-OK`")
        if st.button("Restore Clean Snapshot Now"):
            st.warning("Reverting VM to snapshot baseline...")
    with col_v2:
        st.markdown("**Isolation Settings:**")
        st.checkbox("Network Host-Only Isolation", value=True)
        st.checkbox("Clipboard Access", value=False)

with tab_files:
    st.subheader("File Static Analysis & Threat Scoring")
    uploaded_file = st.file_uploader("Upload sample for instant hash calculation and heuristic inspection", type=["exe", "zip", "txt", "pdf", "bat", "ps1"])
    
    if uploaded_file is not None:
        temp_path = os.path.join(".", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        hashes = calculate_hashes(temp_path)
        risk, reason = analyze_file_heuristics(uploaded_file.name)
        
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**Threat Assessment:** {risk}")
            st.write(f"**Details:** {reason}")
        with c_f2:
            if hashes:
                st.code(f"SHA-256: {hashes['sha256']}\nMD5: {hashes['md5']}", language="text")
                
        if os.path.exists(temp_path):
            os.remove(temp_path)
