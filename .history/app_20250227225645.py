import streamlit as st
import pandas as pd
import hashlib
import time

# Load user login data
@st.cache_data
def load_user_data():
    return pd.read_csv("user_data.csv")

# Load sensor data
@st.cache_data
def load_sensor_data():
    return pd.read_csv("sensor_data.csv")

# Hash function for password verification
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication function
def authenticate(user_id, password, users_df):
    hashed_password = hash_password(password)
    user_match = users_df[(users_df["User ID"] == user_id) & (users_df["Password"] == hashed_password)]
    return not user_match.empty

# UI - Login Page
st.title("🔐 MedGuard Login")

# User Input Fields
user_id = st.text_input("User ID", key="user")
password = st.text_input("Password", type="password", key="pass")
login_btn = st.button("Login")

# Load Data
users_df = load_user_data()
sensor_df = load_sensor_data()

# Login Authentication
if login_btn:
    if authenticate(user_id, password, users_df):
        st.success(f"✅ Welcome, {user_id}!")
        st.session_state["authenticated"] = True
        st.session_state["user_id"] = user_id
        time.sleep(1)
        st.experimental_rerun()
    else:
        st.error("❌ Invalid credentials. Please try again.")

# App Navigation (Only after login)
if st.session_state.get("authenticated", False):

    st.sidebar.title("📌 MedGuard Features")
    menu = st.sidebar.radio(
        "Select a Feature",
        ["📊 Body Temperature Monitoring", "💓 Heart Rate Monitoring", "🚨 Emergency Alerts", "💊 Tablet Reminder"]
    )

    # Filter user data
    user_data = sensor_df[sensor_df["User ID"] == st.session_state["user_id"]]

    # Body Temperature Monitoring Page
    if menu == "📊 Body Temperature Monitoring":
        st.title("🌡️ Real-time Body Temperature Monitoring (DHT11)")
        st.line_chart(user_data.set_index("Timestamp")["Body Temperature (°C)"])
        st.dataframe(user_data[["Timestamp", "Body Temperature (°C)"]].tail(10))

    # Heart Rate Monitoring Page
    elif menu == "💓 Heart Rate Monitoring":
        st.title("❤️ Real-time Heart Rate Monitoring (MAX30100)")
        st.line_chart(user_data.set_index("Timestamp")["Heart Rate (BPM)"])
        st.dataframe(user_data[["Timestamp", "Heart Rate (BPM)"]].tail(10))

    # Emergency Alerts Page
    elif menu == "🚨 Emergency Alerts":
        st.title("🚨 Emergency Alert System (GSM900A)")
        alerts = user_data[user_data["Emergency Alert"] == 1]
        if not alerts.empty:
            st.warning("⚠️ Emergency alerts detected!")
            st.dataframe(alerts[["Timestamp", "Emergency Alert"]])
        else:
            st.success("✅ No emergency alerts detected.")

    # Tablet Reminder Page
    elif menu == "💊 Tablet Reminder":
        st.title("💊 Tablet Reminder & History")
        reminders = user_data[user_data["Tablet Reminder"] == 1]
        if not reminders.empty:
            st.info("📌 Tablet reminders found!")
            st.dataframe(reminders[["Timestamp", "Tablet Reminder"]])
        else:
            st.success("✅ No pending reminders.")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
