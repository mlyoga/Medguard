import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import hashlib
import os

# Number of original and new users
num_users = 10
num_easy_users = 5
num_samples_per_user = 100  # Data points per user

# Define new user IDs
user_ids = ["alpha01", "beta02", "gamma03", "delta04", "epsilon05", 
            "zeta06", "eta07", "theta08", "iota09", "kappa10"]

easy_user_ids = ["easyUserA", "easyUserB", "easyUserC", "easyUserD", "easyUserE"]

# Generate hashed passwords with salt
def hash_password(password, salt="secure_salt"):
    return hashlib.sha256((password + salt).encode()).hexdigest()

passwords = [hash_password(f"pass_{name}") for name in user_ids]
easy_passwords = [hash_password(f"easy{name[-1]}23") for name in easy_user_ids]  # easy passwords

# Combine user IDs and passwords
all_user_ids = user_ids + easy_user_ids
all_passwords = passwords + easy_passwords

# Create a user login DataFrame
user_data = pd.DataFrame({"User ID": all_user_ids, "Password": all_passwords})

# Generate sensor data with more realistic timestamping
data_records = []
start_time = datetime.now() - timedelta(days=2)  # Start data generation 2 days ago

for user in all_user_ids:
    for i in range(num_samples_per_user):
        timestamp = start_time + timedelta(minutes=i * 10)  # Simulate data every 10 minutes
        body_temp = round(np.random.uniform(35.5, 38.5), 1)  # Wider range
        heart_rate = np.random.randint(55, 110)  # More realistic range
        emergency_alert = np.random.choice([0, 1], p=[0.97, 0.03])  # Reduced alerts
        tablet_reminder = np.random.choice([0, 1], p=[0.92, 0.08])  # Adjusted probability

        data_records.append([user, timestamp, body_temp, heart_rate, emergency_alert, tablet_reminder])

# Create DataFrame for sensor data
sensor_data = pd.DataFrame(data_records, columns=["User ID", "Timestamp", "Body Temperature (°C)", 
                                                  "Heart Rate (BPM)", "Emergency Alert", "Tablet Reminder"])

# Ensure directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Save login credentials and sensor data to CSV files with timestamps
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
user_data.to_csv(f"data/user_data_{timestamp_str}.csv", index=False)
sensor_data.to_csv(f"data/sensor_data_{timestamp_str}.csv", index=False)

print(f"✅ Synthetic login and sensor data generated successfully! Files saved with timestamp: {timestamp_str}")
