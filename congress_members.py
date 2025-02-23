import secrets
import pymysql.cursors
import requests
import json
import datetime

DB_IP = secrets.DB_IP
DB_USER = secrets.DB_USER
DB_PASS = secrets.DB_PASS
DB_NAME = secrets.DB_NAME
PPAPI_Key = secrets.API_Key

version = "v1"
congress_start = '115'

url = "https://api.propublica.org/congress/{version}/"

payload = {}
headers = {"Auhtorization": PPAPI_Key}