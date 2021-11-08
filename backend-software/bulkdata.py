import sqlite3
import os
import gzip
import csv
import datetime

db_filename = "db.sqlite3"
counter = 1
query_resources = """
INSERT INTO resource (dsp_id, title, artists, isrc, usages, revenue, dsrs_id)
VALUES (?,?,?,?,?,?,?) 
"""
query_dsrs = """
INSERT INTO dsr (path, period_start, period_end, status, currency_id, territory_id)
VALUES (?,?,?,?,?,?)
"""

query_currency="""
INSERT INTO currency (code)
VALUES (?)
"""

query_territory="""
INSERT INTO territory (code_2, local_currency_id)
VALUES (?,?)
"""

files = os.listdir("data")


print("LOADING DATA INTO THE DATABASE ...")

for f in files:

    print(f"LOADING DATA FROM {f}")

    name,plan,country_code,currency_code,dates = str(f).split('_')
    period_start = datetime.datetime.strptime(dates.split('-')[0],"%Y%m%d").date()
    period_end = datetime.datetime.strptime(dates.split('-')[-1].split('.')[0],"%Y%m%d").date()
    dsr_list = [f,period_start,period_end, "Ingested", currency_code, country_code]
    currency_list = [currency_code]
    country_list = [country_code, currency_code]

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(query_currency, currency_list)
        cursor.execute(query_territory, country_list)
        cursor.execute(query_dsrs, dsr_list)

    list_lines = []
    with gzip.open('data/'+f,) as file:
        list_lines = [line.decode('utf-8').split('\t') for line in file.read().splitlines()]
    
    for line in list_lines[1:]:
        line.append(counter)
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(query_resources, line)
    counter += 1

print("LOADING FINISHED SUCCESSFULLY")