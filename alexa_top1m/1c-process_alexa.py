import os
import sys
import fastavro
from datetime import timedelta, date
import requests
import pandas as pd
import tarfile
import sqlite3
import multiprocessing as mp

#############################
base_directory = './data/openintel-alexa1m/'
parent_directory = base_directory+'data/'
base_data_directory = './data/openintel-alexa1m/processed/'

start_date = date(2019, 12, 1)
end_date = date(2019, 12, 31)
daterange = pd.date_range(start_date, end_date)

NUM_POOL = 2
#############################

def process(single_date):
    '''Description:
    Process and filter data from a single day
    Keyword arguments:
        single_date -- date to process and filter
    Returns:
    	Void
    '''
    directory = parent_directory + single_date.strftime("%Y%m%d")
    print(directory)

    #Write to sqlite db of the month
    db = sqlite3.connect(base_data_directory+"dns_agg-"+single_date.strftime("%Y-%m")+".db")

    for f in [f for f in os.listdir(directory) if fastavro.is_avro(directory+"/"+f)]:
            print(directory+"/"+f)
            with open(directory+"/"+f, 'rb') as fo:
                reader = fastavro.reader(fo)
                #We only look at a+www and aaaa+www and the status code has to be 0 aka successs
                records = [r for r in reader if ((r.get('query_type') == "A" or r.get('query_type') == "AAAA") and r.get('query_name').startswith("www.")) and r.get('status_code') == 0]
                df = pd.DataFrame.from_records(records)
                #Some avro files are empty for whatever reason
                if not df.empty:
                    #Select the columns we want
                    df = df[['query_name', 'query_type', 'as', 'cname_name', 'response_type', 'response_name', 'ip4_address', 'ip6_address']]
                    #Avro files have a timestamp however the fastavro package converts it to int,
                    # which means it pads it with 0 at the end, which makes it not suitable for conversion to a date
                    df['date'] = single_date.strftime("%Y-%m-%d")
                    df.to_sql('data', db, if_exists='append', index=False)

    print('### Finished'+single_date.strftime("%Y-%m-%d"))

    db.close()
    

pool = mp.Pool(processes=NUM_POOL)
pool.map(process, daterange)  # process day
pool.close()
pool.join()