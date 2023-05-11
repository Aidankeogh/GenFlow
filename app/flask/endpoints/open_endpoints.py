from __main__ import app
from flask import request
import json
from utils.api_utils.api_utils import endpoint_handler
from src.settings import settings as ST
from src.core.home import home
from src.core.pca import pca


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


