from __main__ import app
from flask import request
import json
from utils.api_utils.api_utils import endpoint_handler
from src.settings import settings as ST
from src.core.home import home
from src.core.pca import pca


@app.route("/home")
@endpoint_handler
def health():
    res = home.get_df()
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}


@app.route("/pca")
@endpoint_handler
def pca_get():
    res = pca.get_df()
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}
