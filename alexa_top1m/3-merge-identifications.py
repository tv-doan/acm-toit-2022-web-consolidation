import pandas as pd
import sqlite3
import re
import numpy as np
import datetime
import multiprocessing as mp
import os
from datetime import timedelta, date

#############################
start_date = date(2019, 12, 1)
end_date = date(2019, 12, 31)
daterange = pd.date_range(start_date, end_date)
#############################

target_db_plots = sqlite3.connect('[...PATH...]/data/openintel-alexa1m/processed/dns_analyzed_for_plots-HYBRID.db')
target_db_long = sqlite3.connect('[...PATH...]/data/openintel-alexa1m/processed/dns_analyzed_longitudinal-HYBRID.db')

plots_c = target_db_plots.cursor()
plots_c.execute('''
                   CREATE TABLE "df_all" (
                   "date" TEXT,
                   "query_type" TEXT,
                   "query_name" INTEGER
                   );
                ''')

plots_c.execute('''
                   CREATE TABLE "df_all_cdn" (
                   "date" TEXT,
                   "query_type" TEXT,
                   "query_name" INTEGER
                   );
                ''')

plots_c.execute('''
                   CREATE TABLE "df_none" (
                   "date" TEXT,
                   "query_type" TEXT,
                   "query_name" INTEGER
                   );
                ''')

plots_c.execute('''
                   CREATE TABLE "df_cdn" (
                   "cdn_name" TEXT,
                   "date" TEXT,
                   "query_type" TEXT,
                   "query_name" INTEGER
                   );
                ''')
target_db_plots.commit()


long_c = target_db_long.cursor()
long_c.execute('''
                    CREATE TABLE "dns_ana" (
                    "query_name" TEXT,
                    "query_type" TEXT,
                    "as" TEXT,
                    "cname_name" TEXT,
                    "response_type" TEXT,
                    "response_name" TEXT,
                    "cdn_name" TEXT,
                    "cdn" INTEGER,
                    "date" TEXT
                    );
                ''')
target_db_long.commit()

for day in daterange:
    
    db_path_plots = '[...PATH...]/data/openintel-alexa1m/processed/analyzed/dns_analyzed_for_plots-HYBRID-' + day.strftime("%Y-%m-%d") + '.db'

    plots_c.execute("ATTACH '%s' AS db_to_merge;" % db_path_plots)
    plots_c.execute("INSERT INTO df_all SELECT * FROM db_to_merge.[df_all];")
    plots_c.execute("INSERT INTO df_all_cdn SELECT * FROM db_to_merge.[df_all_cdn];")
    plots_c.execute("INSERT INTO df_none SELECT * FROM db_to_merge.[df_none];")
    plots_c.execute("INSERT INTO df_cdn SELECT * FROM db_to_merge.[df_cdn];")
    target_db_plots.commit() 
    plots_c.execute("DETACH db_to_merge;")

    db_path_long = '[...PATH...]/data/openintel-alexa1m/processed/analyzed/dns_analyzed_longitudinal-HYBRID-' + day.strftime("%Y-%m-%d") + '.db'

    long_c.execute("ATTACH '%s' AS db_to_merge;" % db_path_long)
    long_c.execute("INSERT INTO dns_ana SELECT * FROM db_to_merge.[dns_ana];")
    target_db_long.commit() 
    long_c.execute("DETACH db_to_merge;")

target_db_plots.close()
target_db_long.close()
