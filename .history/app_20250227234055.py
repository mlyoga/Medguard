import streamlit as st
import pandas as pd
import hashlib
import time

# Load user login data
@st.cache_data
def load_user_data():
    try:
        return pd.read_csv("user_data.csv")
    except FileNotFoundError:
        st.error("❌ Error: 'user_data.csv' not found!")
        return pd.DataFrame(columns=["User ID", "Password"])

# Load sensor data
@st.cache_data
def load_sensor_data():
    try:
        return pd.read_csv("sensor_data.csv")
    except FileNotFoundError:
        st.error("❌ Error: 'sensor_data.csv' not found!")
        return pd.DataFrame(columns=["User ID", "Timestamp", "Body Temperature (°C)", "Heart Rate (BPM)", "Emergency Alert", "Tablet Reminder"])

# Hash function for password verification
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication function
def authenticate(user_id, password, users_df):
    hashed_password = hash_password(password)
    user_match = users_df[(users_df["User ID"].str.strip() == user_id) & (users_df["Password"].str.strip() == hashed_password)]
    return not user_match.empty

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# UI - Login Page
if not st.session_state["authenticated"]:
    st.title("🔐 MedGuard Login")
    
    user_id = st.text_input("User ID", key="user")
    password = st.text_input("Password", type="password", key="pass")
    login_btn = st.button("Login")
    
    users_df = load_user_data()
    
    if login_btn:
        if authenticate(user_id, password, users_df):
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = user_id
            st.success(f"✅ Welcome, {user_id}!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
    
else:
    st.sidebar.title("📌 MedGuard Features")
    menu = st.sidebar.radio(
        "Select a Feature",
        ["📊 Body Temperature Monitoring", "💓 Heart Rate Monitoring", "🚨 Emergency Alerts", "💊 Tablet Reminder"]
    )
    
    sensor_df = load_sensor_data()
    user_data = sensor_df[sensor_df["User ID"] == st.session_state["user_id"]]
    user_data["Timestamp"] = pd.to_datetime(user_data["Timestamp"], errors='coerce')
    
    if menu == "📊 Body Temperature Monitoring":
        st.title("🌡️ Real-time Body Temperature Monitoring (DHT11)")
        if not user_data.empty:
            st.line_chart(user_data.set_index("Timestamp")["Body Temperature (°C)"])
            st.dataframe(user_data[["Timestamp", "Body Temperature (°C)"]].tail(10))
        else:
            st.warning("No data available.")
    
    elif menu == "💓 Heart Rate Monitoring":
        st.title("❤️ Real-time Heart Rate Monitoring (MAX30100)")
        if not user_data.empty:
            st.line_chart(user_data.set_index("Timestamp")["Heart Rate (BPM)"])
            st.dataframe(user_data[["Timestamp", "Heart Rate (BPM)"]].tail(10))
        else:
            st.warning("No data available.")
    
    elif menu == "🚨 Emergency Alerts":
        st.title("🚨 Emergency Alert System (GSM900A)")
        alerts = user_data[user_data["Emergency Alert"] == 1]
        if not alerts.empty:
            st.warning("⚠️ Emergency alerts detected! 🚨")
            st.dataframe(alerts[["Timestamp", "Emergency Alert"]])
        else:
            st.success("✅ No emergency alerts detected.")
    
    elif menu == "💊 Tablet Reminder":
        st.title("💊 Tablet Reminder & History")
        reminders = user_data[user_data["Tablet Reminder"] == 1]
        if not reminders.empty:
            st.info("📌 Tablet reminders found!")
            st.dataframe(reminders[["Timestamp", "Tablet Reminder"]])
        else:
            st.success("✅ No pending reminders.")
    
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
