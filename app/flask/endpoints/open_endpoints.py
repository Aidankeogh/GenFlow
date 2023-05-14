from __main__ import app
from flask import request
import json
from utils.api_utils.api_utils import endpoint_handler
from src.settings import settings as ST
from src.core.home import home
from src.core.s_data import s_data


@app.route("/home")
@endpoint_handler
def experiments():
    res = home.get_df(json.loads(request.args.get('spec')))
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/home-spec")
@endpoint_handler
def run_spec():
    res = home.get_run_spec(json.loads(request.args.get('spec')))
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/save-setting", methods=['POST'])
@endpoint_handler
def save_data_setting():
    res = s_data.save_setting(request.json)
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/delete-setting", methods=['POST'])
@endpoint_handler
def delete_data_setting():
    res = s_data.delete_setting(request.json)
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/get-settings")
@endpoint_handler
def get_data_settings():
    res = s_data.get_settings()
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/load-setting/<setting_name>")
@endpoint_handler
def load_data_setting(setting_name):
    res = s_data.load_setting(setting_name)
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}
