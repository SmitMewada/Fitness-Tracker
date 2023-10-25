import pandas as pd
from glob import glob

## Read all the files.

acc_df = pd.DataFrame()
gyro_df = pd.DataFrame()

acc_set = 1
gyro_set = 1

files = glob("../../data/raw/MetaMotion/*.csv")

for file in files:
    data_path = "../../data/raw/MetaMotion/"
    
    participant = file.split("-")[0].replace(data_path, "")
    label = file.split("-")[1]
    category = file.split("-")[2].rstrip("2").rstrip("_MetaWear_2019")
    
    df = pd.read_csv(file)

    df["participant"] = participant
    df["label"] = label
    df["category"] = category   
    
    if "Accelerometer" in file:
        df["set"] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df])
    
    if "Gyroscope" in file:
        df["set"] = gyro_set
        gyro_set += 1
        gyro_df = pd.concat([gyro_df, df])
        
        
# Working with datetimes