import streamlit as st
import pandas as pd
import numpy as np
import time

# Simulating sensor data
def generate_temperature():
    return round(np.random.uniform(36.0, 38.5), 2)

def generate_heart_rate():
    return np.random.randint(60, 100)

def get_emergency_alert():
    return "🚨 Alert: Emergency detected! SMS sent via GSM900A."

def audio_alert():
    return "🔊 Playing emergency voice alert via ISD1820."

def get_tablet_reminder():
    return "💊 Reminder: Take your medicine at 8:00 AM."

# Login Page
def login_page():
    st.title("🔐 MedGuard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state["logged_in"] = True
        st.experimental_rerun()

# Main App
def main_app():
    st.sidebar.title("MedGuard Dashboard")
    selection = st.sidebar.radio("Go to", ["Body Temperature", "Heart Rate", "Emergency Alerts", "Audio Alerts", "Tablet Reminders"])
    
    if selection == "Body Temperature":
        st.title("🌡 Real-time Body Temperature Monitoring")
        temp = generate_temperature()
        st.metric(label="Body Temperature (°C)", value=temp)
        time.sleep(1)
    
    elif selection == "Heart Rate":
        st.title("❤️ Real-time Heart Rate Monitoring")
        heart_rate = generate_heart_rate()
        st.metric(label="Heart Rate (BPM)", value=heart_rate)
        time.sleep(1)
    
    elif selection == "Emergency Alerts":
        st.title("🚨 Emergency Alert System")
        if st.button("Trigger Emergency Alert"):
            alert = get_emergency_alert()
            st.warning(alert)
    
    elif selection == "Audio Alerts":
        st.title("🔊 Audio Alert System")
        if st.button("Play Alert Audio"):
            st.success(audio_alert())
    
    elif selection == "Tablet Reminders":
        st.title("💊 Tablet Reminder & History")
        reminder = get_tablet_reminder()
        st.info(reminder)
        history = pd.DataFrame({"Date": ["2025-02-27", "2025-02-26"], "Medicine": ["Paracetamol", "Vitamin C"]})
        st.table(history)

# Main Execution
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    main_app()
