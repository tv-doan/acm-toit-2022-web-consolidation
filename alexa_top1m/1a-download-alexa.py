#!/usr/bin/env python3
import sys
import os
import shutil
import fastavro
from datetime import timedelta, date
import requests
import pandas as pd
import numpy as np
import sqlite3
import tarfile
import multiprocessing.dummy as mp
import glob

#############################
base_directory = './data/openintel-alexa1m/'
 
start_date = date(2019, 12, 1)
end_date = date(2019, 12, 31)

NUM_POOL = 2

year_dict = {}
year_dict[2019] = 'https://data.openintel.nl/data/alexa1m/2019/openintel-alexa1m-'
# and so on for other years

#############################

def download(url, file_path):
    #Open in binary mode
    with open(file_path, "wb") as file:
        #Get request
        response = requests.get(url)
        #Write to file
        file.write(response.content)


def download_alexa(single_date):
    base_url = year_dict.get(single_date.year)
    print("Processing "+single_date.strftime("%Y%m%d"))
    if not os.path.isdir(base_directory+'data/'+single_date.strftime("%Y%m%d")):
        os.makedirs(base_directory+'data/'+single_date.strftime("%Y%m%d"))
        url = base_url + single_date.strftime("%Y%m%d") + '.tar'
        file_path = base_directory+'data/'+single_date.strftime("%Y%m%d")+'/openintel-alexa1m-'+single_date.strftime("%Y%m%d")+'.tar'
        download(url, file_path)
        print("Finished downloading: "+url)
        tar = tarfile.open(file_path)
        tar.extractall(base_directory+'data/'+single_date.strftime("%Y%m%d"))
        tar.close()
        print("Finished untar: "+file_path)
    else:
        print("Path already exists")


pool = mp.Pool(NUM_POOL)
pool.map(download_alexa, list(pd.date_range(start_date, end_date)))
print("Done")
pool.close()
pool.join()



