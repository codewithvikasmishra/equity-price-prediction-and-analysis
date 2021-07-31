import pandas as pd
import requests
from requests import NullHandler, status_codes
import datetime
from db_connection.sql_cnxn import *
from typing import Collection
from flask import Flask, request, jsonify,abort, after_this_request
from config.logger import *


logger = logging.getLogger('dbconfig')
setup_logger(logger,'logs/url.logs')


A=Cnxn
sql_cnxn=A.sql_conn()

# app = Flask(__name__)

# holidays = ['21-02-2020','10-03-2020','02-04-2020','06-04-2020','10-04-2020','14-04-2020','01-05-2020',
#             '25-05-2020','10-10-2020','16-11-2020','30-11-2020','25-12-2020'
#             ,'26-01-2021','11-03-2021','29-03-2021','02-04-2021','14-04-2021','21-04-2021','13-05-2021'
#             ,'21-05-2021','19-08-2021','10-09-2021','15-10-2021','04-11-2021','05-11-2021','19-10-2021']

class NSE():
    def __init__(self,year,leaves,dt):
        self.year = year
        self.leaves = leaves
        self.dt = dt

    def get_url(self):
        logger.info(self.dt.strftime("%A"))
        try:
            if self.dt<datetime.datetime.now() and self.dt not in self.leaves:
                if self.dt.day in (1,2,3,4,5,6,7,8,9) or self.dt.month in (1,2,3,4,5,6,7,8,9):
                    url = "https://archives.nseindia.com/products/content/sec_bhavdata_full_"+"0"+str(self.dt.day)+"0"+str(self.dt.month)+str(self.dt.year)+".csv"
                else:
                    url = "https://archives.nseindia.com/products/content/sec_bhavdata_full_"+str(self.dt.day)+str(self.dt.month)+str(self.dt.year)+".csv"
            return url
        except Exception as e:
            logger.error(f"get_url.{e}")
            return abort(400,"Please verify url method")

    def get_data(self):
        A = NSE(self.year,self.leaves,self.dt)
        try:
            url = A.get_url()
            data = pd.read_csv(url)
            return data
        except Exception as e:
            logger.error(f"get_data.{e}")
            return abort(400,"Please verify either url method or get Data method")

    def put_data_into_db(self):
        cursor=sql_cnxn.cursor()
        cursor.fast_executemany = True
        A = NSE(self.year,self.leaves,self.dt)
        df = A.get_data()

        for col in df.columns:
            if col not in ('SYMBOL',' SERIES',' DATE1'):
                df[col].replace(to_replace=' -',value=12345678,regex=True,inplace=True)
                df[col].replace(to_replace=' ',value=12345678,regex=True,inplace=True)

        try:
            logger.info("Started data insertion"+A.get_url())
            for index,row in df.iterrows():
                cursor.execute('''INSERT INTO nse_data_set (symbol, series, date1, prev_close, open_price, high_price
                , low_price, last_price, close_price, avg_price, ttl_trd_qnty, turnover_lacs, no_of_trades, deliv_qty, deliv_per)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''',
                row[0],
                row[1],
                row[2],
                float(row[3]),
                float(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                int(row[10]),
                float(row[11]),
                int(row[12]),
                int(row[13]),
                float(row[14]))

            logger.info(A.get_url() + " data insertion completed")
            return "Data Inserted into nse_data_set table in ds_dataset database"

        except Exception as e:
            logger.error(f"put_data_into_db.{e}"+A.get_url()+str(row))
            return abort(400,"Please verify put data into db method")