from __main__ import app
from flask import request
import json
from utils.api_utils.api_utils import endpoint_handler
from src.settings import settings as ST
from src.core.pca import pca


@app.route("/health")
@endpoint_handler
def health():
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: {ST.MSG: 'Aloha', ST.SUCCESS: True}}


@app.route("/pca")
@endpoint_handler
def pca_get():
    res = pca.get_df()
    return {ST.HTTP_STATUS: 200, ST.PAYLOAD: res}
