# import libraries
import pandas as pd

#read dataset:
def extract_data(file):
    data = pd.read_csv(file)
    
    return data

data = extract_data('/Volumes/MINTTEA/tw-dataeng-home-assignment /data/activity.csv')
