import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import hashlib

# Number of original and new users
num_users = 10
num_easy_users = 5
num_samples_per_user = 100  # Data points per user

# Define new user IDs
user_ids = [f"user_{i}" for i in range(1, num_users + 1)]
easy_user_ids = [f"easyUser{i}" for i in range(1, num_easy_users + 1)]

# Generate hashed passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Creating strong and weak passwords
passwords = {user: f"NewPass{user[-1]}#@!" for user in user_ids}
easy_passwords = {user: f"easy{user[-1]}23" for user in easy_user_ids}  # easy passwords

# Hash passwords
hashed_passwords = {user: hash_password(passwords[user]) for user in user_ids}
hashed_easy_passwords = {user: hash_password(easy_passwords[user]) for user in easy_user_ids}

# Combine user IDs and passwords
all_user_ids = user_ids + easy_user_ids
all_passwords = {**hashed_passwords, **hashed_easy_passwords}

# Create a user login DataFrame
user_data = pd.DataFrame({"User ID": all_user_ids, "Password": [all_passwords[user] for user in all_user_ids]})

# Generate sensor data
data_records = []
for user in all_user_ids:
    for i in range(num_samples_per_user):
        timestamp = datetime.now() - timedelta(seconds=i * 30)
        body_temp = round(np.random.uniform(36.0, 38.0), 1)
        heart_rate = np.random.randint(60, 100)
        emergency_alert = np.random.choice([0, 1], p=[0.95, 0.05])
        tablet_reminder = np.random.choice([0, 1], p=[0.90, 0.10])

        data_records.append([user, timestamp, body_temp, heart_rate, emergency_alert, tablet_reminder])

# Create DataFrame for sensor data
sensor_data = pd.DataFrame(data_records, columns=["User ID", "Timestamp", "Body Temperature (°C)", 
                                                  "Heart Rate (BPM)", "Emergency Alert", "Tablet Reminder"])

# Save login credentials and sensor data to CSV files
user_data.to_csv("user_data.csv", index=False)
sensor_data.to_csv("sensor_data.csv", index=False)

print("✅ Synthetic login and sensor data generated successfully!")
print("User credentials saved in user_data.csv")
