import os
import time
from DIPPID import SensorUDP
import pandas as pd


# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)
activity_started = False
name = input("Enter your name: ")
activity = input("Enter your activity:(running, rowing, lifting, jumpingjacks)")

#creates folder with name and saves csv files in that folder
def save_data(data):
    df = pd.DataFrame(data)
    #chatgpt to save file
    counter = 1
    file_name_base = f"{name}-{activity}"

    while os.path.exists(f"{name}/{file_name_base}-{counter}.csv"):
        counter += 1
    file_path = f"{name}/{file_name_base}-{counter}.csv"
    if not os.path.exists(name):
        os.makedirs(name)
    df.to_csv(file_path, index=False)
    print(f"Saved {file_path}")


idnum = -1
data = []
#when button 1 pressed starts tracking activity for about 10 seconds, after that button can be pressed again to
#record more datasets
while True:
    if sensor.has_capability("button_1"):
        if sensor.get_value("button_1") == 1 and not activity_started:
            activity_started = True
            print("activity started")
        if activity_started and sensor.has_capability('gyroscope') and ('accelerometer'):
            gyr_x = float(sensor.get_value('gyroscope')['x'])
            gyr_y = float(sensor.get_value('gyroscope')['y'])
            gyr_z = float(sensor.get_value('gyroscope')['z'])
            acc_x = float(sensor.get_value('accelerometer')['x'])
            acc_y = float(sensor.get_value('accelerometer')['y'])
            acc_z = float(sensor.get_value('accelerometer')['z'])
            idnum += 1
            data.append({"id": idnum, "timestamp": time.time(),
                         "acc_x": acc_x, "acc_y": acc_y, "acc_z": acc_z,
                         "gyro_x": gyr_x, "gyro_y": gyr_y, "gyro_z": gyr_z})
            time.sleep(0.001)
            if idnum == 10000: # when 10k datarows reached saves data and resets to allow new data
                save_data(data)
                activity_started = False
                data.clear()
                idnum = -1
