import pandas as pd
import os
import yaml
from datetime import datetime

ml_folder = 'mlruns'


def extract_exp_fields(exp):
    with open(f'{ml_folder}/{exp}/meta.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    return {
        'Emperiment Id': exp,
        'Experiment Name': data['name'],
        'Experiment Created': datetime.fromtimestamp(data['creation_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S"),
        'Experiment Updated': datetime.fromtimestamp(data['last_update_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_df():
    dir_list = os.listdir(ml_folder)
    exps = [
        d
        for d in dir_list 
        if len(os.listdir(f'{ml_folder}/{d}')) > 1
        and d != '.trash'
    ]
    
    data = []
    for exp in exps:
        data.append(extract_exp_fields(exp))

    df = pd.DataFrame(data)
    return {
        'rows': df.to_dict(orient='records'),
        'columns': [{'text': col, 'value': col, 'sortable': True} for col in df.columns]
    }