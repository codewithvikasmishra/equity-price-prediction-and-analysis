import pandas as pd
import requests
from requests import status_codes
import datetime
from typing import Collection
from flask import Flask, request, jsonify,abort, after_this_request
from config.logger import *
from .main import *


logger = logging.getLogger('dbconfig')
setup_logger(logger,'logs/data_insert.logs')
logger.info("Started data_insert.py")

app = Flask(__name__)

@app.route('/all_year/insert', methods = ['POST'])
def sql_insert_year():
    yr = request.get_json(['year'])
    leaves = request.get_json(['bank_holidays'])
    if request.get_json().keys() != {'year','bank_holidays'}:
        return abort(400, "Please pass the key as year and bank_holidays.")
    elif request.get_json('year')['year']=='':
        return abort(400, "Please pass key and value.")
    elif request.get_json('bank_holidays')['bank_holidays']=='':
        return abort(400, "Please pass key and value.")
    
    dt = datetime.datetime(yr['year'], 1, 1)
    if yr['year']%4 == 0:
        dt = datetime.datetime(yr['year'], 1, 1)
        for i in range(0, 366):
            if dt.strftime("%A") not in ('Saturday', 'Sunday'):
                A = NSE(yr['year'],leaves['bank_holidays'],dt)
                A.put_data_into_db()
            dt = dt + datetime.timedelta(days=1)
        return jsonify({'status': 'All Data Inserted'})
    else:
        dt = datetime.datetime(yr['year'], 1, 1)
        for i in range(0, 365):
            if dt.strftime("%A") not in ('Saturday', 'Sunday'):
                A = NSE(yr['year'],leaves['bank_holidays'],dt)
                A.put_data_into_db()
            dt = dt + datetime.timedelta(days=1)
        return jsonify({'status': 'All Data Inserted'})

@app.route('/one_day/insert', methods = ['POST'])
def sql_insert_day():
    day = request.get_json(['day'])
    if request.get_json().keys()!={'day'}:
        return abort(400, "Please pass the key as day.")
    elif request.get_json('day')['day']=='':
        return abort(400, "Please pass key and value.")
    
    dt = datetime.datetime(day['day'], 1, 1)
    A = NSE(day['day'])
    A.put_data_into_db()