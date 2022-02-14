import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
from multiprocessing import Pool, current_process

import mimetypes
from adblockparser import AdblockRules


# PATHS
db_in_path = '[...PATH...]/httparchive_processed/2020-01/assets.db'
out_path = '[...PATH...]/httparchive_processed/2020-01/processed'
ip_asn_mapping = '[...PATH...]/as-identification/ip-asn-map-full-2020.csv'

NUM_PROC = 30

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


def process(lims):
    process_id = current_process()._identity[0]
    (start_row, end_row) = lims
    
    conn = sqlite3.connect(db_in_path)

    print('[%d] %s - start processing rows [%s, %s]' % (process_id, datetime.now(), start_row, end_row))

    assets = pd.read_sql('''
        select *
        from assets
        where base_page != asset_url
        and rowid >= %s
        and rowid < %s
        ''' % (start_row, end_row), 
        con=conn, 
        chunksize=6000000)

    i = 0

    with open('[...PATH...]/easylist.txt', 'r') as ad_rules_list, open('[...PATH...]/easyprivacy.txt', 'r') as tracker_rules_list:
        ad_rules = AdblockRules(ad_rules_list,
                                use_re2=True
                                )

        tracker_rules = AdblockRules(tracker_rules_list, use_re2=True
                                    )

    as_df = pd.read_csv(ip_asn_mapping, sep=';', dtype={'ip' : str,
                                                        'asn' : str,
                                                        'holder' : str,
                                                        'cdn_asn' : str})


    for df in assets:
        print('[%02d] Processing chunk no. %d @ %s' % (process_id, i, datetime.now()))

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


        # # ad and tracker identification
        df['is_ad'] = df.apply(lambda row: ad_rules.should_block(
            row['asset_url']),
            axis=1
            )
        df['is_tracker'] = df.apply(lambda row: tracker_rules.should_block(
            row['asset_url']),
            axis=1
            )

        df = df.merge(as_df, on=['ip_addr'], how='left')
        df['hybrid_ident'] = df.apply(hybrid_identification_assets, axis=1)

        # saving
        con_out = sqlite3.connect('[...PATH...]/%s/%s_NEW.db' % (out_path, process_id))
        con_out.text_factory = str
        df.to_sql('assets_processed', con=con_out, if_exists = 'append')  # keep index for eventual sorting later on
        con_out.close()

        del x
        del df

        i = i+1

    print("[%02d] Finished @ %s." % (process_id, datetime.now()))

    conn.close()


if __name__ == "__main__":

    print('Start processing @ %s' % datetime.now())
    conn = sqlite3.connect(db_in_path)
    assets_num = pd.read_sql('select max(rowid) from assets', con=conn)
    conn.close()
    
    bounds = np.linspace(0, assets_num.values[0][0], num=NUM_PROC+1, dtype=int)
    bounds[-1] = bounds[-1] + 1  # adjust for last row of the whole db
    lims = [(bounds[i], bounds[i+1]) for i in range(len(bounds)) if i < NUM_PROC]
    
    pool = Pool(processes = NUM_PROC)

    print("[%s] Starting workers..." % datetime.now())
    pool.map(process, lims)
