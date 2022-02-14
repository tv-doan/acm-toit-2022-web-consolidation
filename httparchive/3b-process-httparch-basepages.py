import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
from multiprocessing import Pool, current_process

import mimetypes

# PATHS
db_path = '[...PATH...]/httparchive_processed/2020-01/basepages.db'
ip_asn_mapping = '[...PATH...]/as-identification/ip-asn-map-full-2020.csv'

# hybrid identification
def hybrid_identification_assets(row):
    if row['cdn_1']:  # row['asset_cdn']:
        return row['cdn_1']  # row['asset_cdn']
    elif row['cdn_asn']:
        return row['cdn_asn']
    else:
        return ''


def classify_asset(value, asset_url):
    value = value.lower()
    if 'javascript' in value:
        return 'javascript'
    elif 'html' in value:
        return 'html'
    elif any(substring in value for substring in ['img', 'image', 'jpg', 'jpeg', 'png', 'gif', 'bmp']):
        return 'image'
    elif 'audio' in value:
        return 'audio'
    elif 'video' in value:
        return 'video'
    elif 'font' in value:
        return 'font'
    elif 'application' in value:
        return 'application'
    elif 'text' in value:
        return 'text'
    elif not value:
        if asset_url:
            asset_url = asset_url.split('#')[0].split('?')[0]
            type, _ = mimetypes.guess_type(asset_url)
            if type:
                return classify_asset(type, '')
            else:
                return 'no type'  # specified/identifiable
    return 'unidentified'  # value.split('/')[0]  # 'other'


def process():
    conn = sqlite3.connect(db_path)

    print("Reading @ %s." % datetime.now())
    df = pd.read_sql('''
        select *
        from base_pages_extracted
        ''', 
        con=conn)

    as_df = pd.read_csv(ip_asn_mapping, sep=';', dtype={'ip' : str,
                                                        'asn' : str,
                                                        'holder' : str,
                                                        'cdn_asn' : str})


    print("Processing @ %s." % datetime.now())

    # reduce data by removing and marking duplicates
    x = df[df[['base_page', 'asset_url', 'asset_cdn']].duplicated(keep=False)].copy()
    x['asset_content_type'] = 'DUPL_REQUEST'
    x['mime_type'] = 'DUPL_REQUEST'
    df.update(x)
    df = df.sort_values('asset_cdn', ascending=False
                ).drop_duplicates(['base_page', 'asset_url'], keep='first'
                                ).sort_index()

    # identify and classify MIME type
    df['mime_type'] = df.apply(lambda x: classify_asset(x['asset_content_type'], x['asset_url']), axis=1)

    # split stacked CDNs
    split = df.asset_cdn.str.split(",", expand=True).replace({'' : None})
    try:
        df['cdn_1'] = split[0].str.strip()
    except:
        df['cdn_1'] = None
    try:
        df['cdn_2'] = split[1].str.strip()
    except:
        df['cdn_2'] = None
    try:
        df['cdn_3'] = split[2].str.strip()
    except:
        df['cdn_3'] = None

    df = df.merge(as_df, on=['ip_addr'], how='left')
    df['hybrid_ident'] = df.apply(hybrid_identification_assets, axis=1)

    # saving
    conn.text_factory = str
    df.to_sql('base_pages_from_assets_processed', con=conn, if_exists = 'replace', index=False)
    conn.close()

    print("Finished @ %s." % datetime.now())



if __name__ == "__main__":

    print('Start processing @ %s' % datetime.now())
    process()
