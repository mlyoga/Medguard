import pandas as pd
import numpy as np
import hashlib
from datetime import datetime, timedelta

# Number of users and samples per user
num_users = 10
num_samples_per_user = 100  # Data points per user

# Generate user IDs and passwords
user_ids = [f"user{i}" for i in range(1, num_users + 1)]
passwords = [f"pass{i}" for i in range(1, num_users + 1)]

# Hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

hashed_passwords = [hash_password(pw) for pw in passwords]

# Create User Data DataFrame
user_data = pd.DataFrame({"User ID": user_ids, "Password": hashed_passwords})

# Generate synthetic sensor data
data_records = []
for user in user_ids:
    for i in range(num_samples_per_user):
        timestamp = datetime.now() - timedelta(seconds=i * 30)
        body_temp = round(np.random.uniform(36.0, 38.0), 1)
        heart_rate = np.random.randint(60, 100)
        emergency_alert = np.random.choice([0, 1], p=[0.95, 0.05])
        tablet_reminder = np.random.choice([0, 1], p=[0.90, 0.10])
        data_records.append([user, timestamp, body_temp, heart_rate, emergency_alert, tablet_reminder])

# Create Sensor Data DataFrame
sensor_data = pd.DataFrame(data_records, columns=["User ID", "Timestamp", "Body Temperature (°C)", 
                                                  "Heart Rate (BPM)", "Emergency Alert", "Tablet Reminder"])

# Save data to CSV files
user_data.to_csv("user_data.csv", index=False)
sensor_data.to_csv("sensor_data.csv", index=False)

print("✅ User and sensor data generated successfully!")
