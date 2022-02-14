import pandas as pd
import sqlite3
import re
import numpy as np
import datetime
import multiprocessing as mp
import os
from datetime import timedelta, date

#############################
base_directory = '[...PATH...]/data/openintel-alexa1m/'
base_data_directory = '[...PATH...]/data/openintel-alexa1m/processed/'

start_date = date(2019, 12, 1)
end_date = date(2019, 12, 31)
daterange = pd.date_range(start_date, end_date)

NUM_POOL = 1
#############################


def add_rank_info(day):
    print("Started at "+ str(datetime.datetime.now()))

    print('Adding Alexa rank information for day ' + day.strftime("%Y-%m-%d"))

    db2 = sqlite3.connect(base_data_directory+"analyzed/dns_analyzed_longitudinal-HYBRID-" + day.strftime("%Y-%m-%d") + '.db')
    df = pd.read_sql('select * from dns_ana', con=db2)
    db2.close()

    df_alexa = pd.DataFrame()

    df_alexa = pd.read_csv(base_directory+'toplists/'+day.strftime("%Y-%m-%d")+'.csv', header=None, names=['rank', 'query_name'])
    
    # Append www. for the join
    df_alexa['query_name'] = np.where(df_alexa['query_name'].str.startswith('www.'), df_alexa['query_name']+'.', 'www.'+df_alexa['query_name']+'.')

    # Join with IPv4 data
    df_day = df[df['query_type'] == 'A']
    df_day = df_day[['query_name', 'cdn_name', 'cdn', 'date']]
    df_tmp = pd.merge(df_alexa, df_day, how='left', on=['query_name'])

    # Join with IPv6 data
    df_day_6 = df[df['query_type'] == 'AAAA']
    df_day_6 = df_day_6[['query_name', 'cdn_name', 'cdn', 'date']]
    df_tmp_6 = pd.merge(df_alexa, df_day_6, how='left', on=['query_name'])

    with sqlite3.connect(base_directory+'processed/dns_with_alexa-HYBRID.db') as db3:
        df_tmp.to_sql(name='dns_alexa_v4', con=db3, if_exists='append', index=False)
        df_tmp_6.to_sql(name='dns_alexa_v6', con=db3, if_exists='append', index=False)

    print("Finished "+day.strftime("%Y-%m-%d")+' at '+str(datetime.datetime.now()))

    # =============================================================================================
    # =============================================================================================
    # =============================================================================================


pool = mp.Pool(processes=NUM_POOL)
pool.map(add_rank_info, daterange)
pool.close()
pool.join()