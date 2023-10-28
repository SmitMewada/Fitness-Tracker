import pandas as pd
from glob import glob

files = glob("../../data/raw/MetaMotion/*.csv")

# Function to read all the data
def data_from_files(files):
    
    # Read all the files
    acc_df = pd.DataFrame()
    gyro_df = pd.DataFrame()

    acc_set = 1
    gyro_set = 1

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
            
    
    # Handle date time
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"], unit="ms")


    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyro_df["epoch (ms)"]
    del gyro_df["time (01:00)"]
    del gyro_df["elapsed (s)"]

    return acc_df, gyro_df


acc_df, gyro_df = data_from_files(files=files)
    
    
# Merging the datasets

'''
    Here, the gyroscope has higher frequency in caputring the data. As a result, there will be many null values in the merged dataset.
'''
data_merged = pd.concat([acc_df.iloc[:, :3], gyro_df], axis=1)

# Renaming the columns

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "label",
    "category",
    "participant",
    "set"
]

# Resampling data (frequency conversion)

'''
    Accelerometer: 12.500HZ
    Gyroscope:     25.00HZ
'''

sampling = {
    "acc_x": "mean", 
    "acc_y": "mean",
    "acc_z": "mean", 
    "gyro_x": "mean", 
    "gyro_y": "mean", 
    "gyro_z": "mean", 
    "label": "last",
    "category": "last",
    "participant": "last",
    "set": "last"
}

data_merged[:1000].resample(rule="200ms").apply(sampling)

# Split by day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat([data_merged[:1000].resample(rule="200ms").apply(sampling).dropna() for df in days])

data_resampled["set"] = data_resampled["set"].astype("int")

# Export dataset
data_resampled.to_pickle("../../data/interim/01_dataprocessed.pkl")



