import pyasn
import pandas as pd
import sys
import json


def lookup_asn(ip):
    asn, prefix = asndb.lookup(ip)
    return asn

if __name__=='__main__':
    asndb = pyasn.pyasn(sys.argv[1])
    
    df = pd.read_csv(sys.argv[2], header=None, names=['ip_addr'])

    for val in df['ip_addr'].unique():
        try:
            lookup_asn(val)
        except:
            print(val)

    try:
        df['asn'] = df['ip_addr'].map(lookup_asn)
    except Exception as e:
        print(e)

    with open('as-names.json') as f:
        as_names_dict = json.load(f)
    as_names_df = pd.DataFrame.from_dict(as_names_dict, orient='index').reset_index(level=0)
    as_names_df.rename(columns={'index' : 'asn', 0: 'as_holder'}, inplace=True)
    as_names_df['asn'] = as_names_df['asn'].astype(int)

    df = df.merge(as_names_df, how='left', on='asn')

    asn_cdns = pd.read_csv('asn_cdns.csv', sep=';')
    asn_cdns = asn_cdns[['cdn_name', 'asn']]
    asn_cdns.drop_duplicates(inplace=True)

    df = df.merge(asn_cdns, how='left', on='asn')
    df.rename(columns={'cdn_name' : 'cdn_asn'}, inplace=True)

    df.to_csv('ip-asn-map-full-%s.csv' % sys.argv[1].split('.')[0][-4:], index=False, sep=';')
