import json
import numpy as np
import pandas as pd
import os
import yaml
from datetime import datetime


def get_ml_folder():
    with open(f'settings.json', 'r') as f:
        data = json.load(f)
        return data['mlflow-path']

def list_folders(path):
    """
    Returns a list of all directories in the given path.
    """
    dir_list = next(os.walk(path))[1]
    return dir_list


def extract_exp_fields(exp):
    ml_folder = get_ml_folder()
    with open(f'{ml_folder}/{exp}/meta.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    return {
        'exp_id': exp,
        'exp_name': data['name'],
        'exp_created': datetime.fromtimestamp(data['creation_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S"),
        'exp_updated': datetime.fromtimestamp(data['last_update_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
    }


def extract_run_fields(exp, run):
    ml_folder = get_ml_folder()
    with open(f'{ml_folder}/{exp}/{run}/meta.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    run_start = None
    if data['start_time'] is not None:
        run_start = datetime.fromtimestamp(data['start_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

    run_end = None
    if data['start_time'] is not None:
        run_end = datetime.fromtimestamp(data['start_time'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

    return {
        'run_id': run,
        'run_name': data['run_name'],
        'run_start': run_start,
        'run_end': run_end
    }


def get_df(params={}):
    ml_folder = get_ml_folder()

    dir_list = list_folders(ml_folder)
    
    exps = [
        d
        for d in dir_list 
        if 
        len(os.listdir(f'{ml_folder}/{d}')) > 1 and 
        d[0] != '.' and 
        not ('models' in d)
    ]

    spec_exp_ids = params.get('exp_ids', [])
    if spec_exp_ids:
        exps = [exp for exp in exps if exp in spec_exp_ids]

    data = []
    for exp in exps:
        exp_fields = extract_exp_fields(exp)
        run_list = list_folders(f'{ml_folder}/{exp}')
        for run in run_list:
            if run[0] == '.':
                continue
            run_fields = extract_run_fields(exp, run)
            
            if params.get('get_params'):
                run_params = {f'param_{k}': v for k, v in get_params(exp, run).items()}
                run_fields = {**run_fields, **run_params}

            if params.get('get_metrics'):
                run_metrics = {f'metric_{k}': v for k, v in get_metrics(exp, run).items()}
                run_fields = {**run_fields, **run_metrics}

            data.append({**exp_fields, **run_fields})
    
    df = pd.DataFrame(data).fillna(np.nan).replace([np.nan], [None])
    df = df.rename(columns=lambda x: x.replace('.', '_'))
    df['ix'] = df.index + 1
    show = [col for col in params['show'] if col in df.columns]


    return {
        'rows': df[show].to_dict(orient='records'),
        'columns': [{'text': params['rename'].get(col, col), 'value': col, 'sortable': True} for col in show]
    }


def get_run_spec(row):
    exp_id = row['exp_id']
    run_id = row['run_id']

    return {
        'params': get_params(exp_id, run_id),
        'metrics': get_metrics(exp_id, run_id),
        'row': {'exp_id': exp_id, 'run_id': run_id}
    }


def get_metrics(exp_id, run_id):
    ml_folder = get_ml_folder()
    folder_path = f'{ml_folder}/{exp_id}/{run_id}/metrics'
    
    metrics = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:        
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as f:
            metrics[file_name] = f.read().split(' ')[1]

    return metrics


def get_params(exp_id, run_id):
    ml_folder = get_ml_folder()

    folder_path = f'{ml_folder}/{exp_id}/{run_id}/params'
    
    params = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:        
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as f:
            params[file_name] = f.read()
    
    return params