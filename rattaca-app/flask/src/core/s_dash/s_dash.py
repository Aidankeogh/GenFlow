import json
import os

PATH = 'models/dashboards'


def get_files(path):
    return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]


def save_setting(params):
    with open(f'{PATH}/{params["setting_name"]}.json', 'w') as f:
        json.dump(params['setting_data'], f, indent=4)

    return {'success': True}


def delete_setting(params):
    file_path = f'{PATH}/{params["setting_name"]}.json'
    
    if os.path.exists(file_path):
        os.remove(file_path)

    return {'success': True}


def get_settings():
    settings = []

    for f in get_files(PATH):
        if not ('.json' in f):
            continue

        setting = f.split('.')[0]
        settings.append({'label': setting, 'value': setting})

    return {'settings': settings}


def load_setting(setting_name):
    with open(f'{PATH}/{setting_name}.json', 'r') as f:
        data = json.load(f)

    return {'setting': data}
