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

as_info = './asn_cdns.csv'  # '[...PATH...]/data/openintel-alexa1m/processed/asn_cdns.csv'

start_date = date(2019, 12, 1)
end_date = date(2019, 12, 31)
daterange = pd.date_range(start_date, end_date)

NUM_POOL = 2
#############################


def identify_keywords(keywords, haystack):
    '''Description:
    Match keywords against haystack, return after first match
    Keyword arguments:
        keywords -- List of Tuples with Regex as value to match against
        haystack -- Value (string) to search in
    Returns:
        Key of the value that matched against haystack
    '''
    #Default: None
    newcdnname = "None"
    for k,v in keywords:
        if v.search(haystack):
            #Stops after the first match, returns key of matched regex
            newcdnname = k
            break
    return newcdnname

def do_identify(day):
    print("Started at "+ str(datetime.datetime.now()))
    print("With "+day.strftime("%Y-%m-%d"))

    db1 = sqlite3.connect(base_data_directory+"dns_agg-"+day.strftime("%Y-%m")+".db")

    # =============================================================================================
    # =============================================================================================
    # =============================================================================================

    print('Reading day' + day.strftime("%Y-%m-%d"))
    df = pd.read_sql("SELECT * FROM data WHERE date == '"+day.strftime("%Y-%m-%d")+"'", db1)
    db1.close()


    # =============================================================================================
    # =============================================================================================
    # =============================================================================================

    print('Pre-processing day' + day.strftime("%Y-%m-%d"))
    df['cname_name'].fillna(value='', inplace = True)
    df['response_name'].fillna(value='', inplace = True)
    df['ip4_address'].fillna(value=np.nan, inplace = True)
    df['ip6_address'].fillna(value=np.nan, inplace = True)
    df['as'].fillna(value=np.nan, inplace = True)
    
    df = df.groupby(['query_name', 'query_type', 'date']).agg({'as':'first', 'cname_name':', '.join, 'ip4_address':'first', 'ip6_address':'first', 'response_name':', '.join, 'response_type':'first'}).reset_index()

    # based on https://github.com/WPO-Foundation/wptagent/blob/master/internal/optimization_checks.py
    keywords = [
        ('Cedexis', re.compile(r'\.cedexis\.net')),
        ('Advanced Hosters CDN', re.compile(r'\.pix\-cdn\.org')),
        ('afxcdn.net', re.compile(r'\.afxcdn\.net')),
        ('Akamai', re.compile(r'\.akamai\.net|\.akamaized\.net|\.akamaiedge\.net|\.akamaihd\.net|\.edgesuite\.net|\.edgekey\.net|\.srip\.net|\.akamaitechnologies\.com|\.akamaitechnologies\.fr')),
        ('Akamai China CDN', re.compile(r'\.tl88\.net')),
        ('Alimama', re.compile(r'\.gslb\.tbcache\.com')),
        ('Amazon CloudFront', re.compile(r'\.cloudfront\.net')),
        ('Aryaka', re.compile(r'\.aads1\.net|\.aads\-cn\.net|\.aads\-cng\.net')),
        ('AT&T', re.compile(r'\.att\-dsa\.net')),
        ('Azion', re.compile(r'\.azioncdn\.net|\.azioncdn\.com|\.azion\.net')),
        ('BelugaCDN', re.compile(r'\.belugacdn\.com|\.belugacdn\.link')),
        ('Bison Grid', re.compile(r'\.bisongrid\.net')),
        ('BitGravity', re.compile(r'\.bitgravity\.com')),
        ('Blue Hat Network', re.compile(r'\.bluehatnetwork\.com')),
        ('BO.LT', re.compile(r'bo\.lt')),
        ('BunnyCDN', re.compile(r'\.b\-cdn\.net')),
        ('Cachefly', re.compile(r'\.cachefly\.net')),
        ('Caspowa', re.compile(r'\.caspowa\.com')),
        ('CDN77', re.compile(r'\.cdn77\.net|\.cdn77\.org')),
        ('CDNetworks', re.compile(r'\.cdngc\.net|\.gccdn\.net|\.panthercdn\.com')),
        ('CDNsun', re.compile(r'\.cdnsun\.net')),
        ('CDNvideo', re.compile(r'\.cdnvideo\.ru|\.cdnvideo\.net')),
        ('ChinaCache', re.compile(r'\.ccgslb\.com')),
        ('ChinaNetCenter', re.compile(r'\.lxdns\.com|\.wscdns\.com|\.wscloudcdn\.com|\.ourwebpic\.com')),
        ('Cloudflare', re.compile(r'\.cloudflare\.com|\.cloudflare\.net')),
        ('Cotendo CDN', re.compile(r'\.cotcdn\.net')),
        ('cubeCDN', re.compile(r'\.cubecdn\.net')),
        ('Edgecast', re.compile(r'edgecastcdn\.net|\.systemcdn\.net|\.transactcdn\.net|\.v1cdn\.net|\.v2cdn\.net|\.v3cdn\.net|\.v4cdn\.net|\.v5cdn\.net')),
        ('Facebook', re.compile(r'\.facebook\.com|\.facebook\.net|\.fbcdn\.net|\.cdninstagram\.com')),
        ('Fastly', re.compile(r'\.fastly\.net|\.fastlylb\.net|\.nocookie\.net')),
        ('GoCache', re.compile(r'\.cdn\.gocache\.net')),
        ('Google', re.compile(r'\.google\.|googlesyndication\.|youtube\.|\.googleusercontent\.com|googlehosted\.com|\.gstatic\.com|\.doubleclick\.net')),
        ('HiberniaCDN', re.compile(r'\.hiberniacdn\.com')),
        ('Highwinds', re.compile(r'hwcdn\.net')),
        ('Hosting4CDN', re.compile(r'\.hosting4cdn\.com')),
        ('ImageEngine', re.compile(r'\.imgeng\.in')),
        ('Incapsula', re.compile(r'\.incapdns\.net')),
        ('Instart Logic', re.compile(r'\.insnw\.net|\.inscname\.net')),
        ('Internap', re.compile(r'\.internapcdn\.net')),
        ('jsDelivr', re.compile(r'cdn\.jsdelivr\.net')),
        ('KeyCDN', re.compile(r'\.kxcdn\.com')),
        ('KINX CDN', re.compile(r'\.kinxcdn\.com|\.kinxcdn\.net')),
        ('LeaseWeb CDN', re.compile(r'\.lswcdn\.net|\.lswcdn\.eu')),
        ('Level 3', re.compile(r'\.footprint\.net|\.fpbns\.net')),
        ('Limelight', re.compile(r'\.llnwd\.net|\.llnw\.net|\.llnwi\.net|\.lldns\.net')),
        ('MediaCloud', re.compile(r'\.cdncloud\.net\.au')),
        ('Medianova', re.compile(r'\.mncdn\.com|\.mncdn\.net|\.mncdn\.org')),
        ('Microsoft Azure', re.compile(r'\.vo\.msecnd\.net|\.azureedge\.net|\.azurefd\.net|\.azure\.microsoft\.com|\-msedge\.net')),
        ('Mirror Image', re.compile(r'\.instacontent\.net|\.mirror\-image\.net')),
        ('NetDNA', re.compile(r'\.netdna\-cdn\.com|\.netdna\-ssl\.com|\.netdna\.com')),
        ('Netlify', re.compile(r'\.netlify\.com')),
        ('NGENIX', re.compile(r'\.ngenix\.net')),
        ('NYI FTW', re.compile(r'\.nyiftw\.net|\.nyiftw\.com')),
        ('OnApp', re.compile(r'\.r\.worldcdn\.net|\.r\.worldssl\.net')),
        ('Optimal CDN', re.compile(r'\.optimalcdn\.com')),
        ('PageCDN', re.compile(r'pagecdn\.io')),
        ('PageRain', re.compile(r'\.pagerain\.net')),
        ('Pressable CDN', re.compile(r'\.pressablecdn\.com')),
        ('PUSHR', re.compile(r'\.pushrcdn\.com')),
        ('Rackspace', re.compile(r'\.raxcdn\.com')),
        ('Reapleaf', re.compile(r'\.rlcdn\.com')),
        ('Reflected Networks', re.compile(r'\.rncdn1\.com|\.rncdn7\.com')),
        ('ReSRC.it', re.compile(r'\.resrc\.it')),
        ('Rev Software', re.compile(r'\.revcn\.net|\.revdn\.net')),
        ('Roast.io', re.compile(r'\.roast\.io')),
        ('Rocket CDN', re.compile(r'\.streamprovider\.net')),
        ('section.io', re.compile(r'\.squixa\.net')),
        ('SFR', re.compile(r'cdn\.sfr\.net')),
        ('SwiftyCDN', re.compile(r'\.swiftycdn\.net')),
        ('Simple CDN', re.compile(r'\.simplecdn\.net')),
        ('Singular CDN', re.compile(r'\.singularcdn\.net\.br')),
        ('Sirv CDN', re.compile(r'\.sirv\.com')),
        ('StackPath', re.compile(r'\.stackpathdns\.com')),
        ('SwiftCDN', re.compile(r'\.swiftcdn1\.com|\.swiftserve\.com')),
        ('Taobao', re.compile(r'\.gslb\.taobao\.com|tbcdn\.cn|\.taobaocdn\.com')),
        ('Telenor', re.compile(r'\.cdntel\.net')),
        ('TRBCDN', re.compile(r'\.trbcdn\.net')),
        ('Twitter', re.compile(r'\.twimg\.com')),
        ('UnicornCDN', re.compile(r'\.unicorncdn\.net')),
        ('Universal CDN', re.compile(r'\.cdn12\.com|\.cdn13\.com|\.cdn15\.com')),
        ('VegaCDN', re.compile(r'\.vegacdn\.vn|\.vegacdn\.com')),
        ('VoxCDN', re.compile(r'\.voxcdn\.net')),
        ('WordPress', re.compile(r'\.wp\.com|\.wordpress\.com|\.gravatar\.com')),
        ('XLabs Security', re.compile(r'\.xlabs\.com\.br|\.armor\.zone')),
        ('Yahoo', re.compile(r'\.ay1\.b\.yahoo\.com|\.yimg\.|\.yahooapis\.com')),
        ('Yottaa', re.compile(r'\.yottaa\.net')),
        ('Zenedge', re.compile(r'\.zenedge\.net'))
    ]

    print('CNAME identification for day' + day.strftime("%Y-%m-%d"))

    df['ip6_address'].fillna(value='Error', inplace = True)
    df = df[((df.ip6_address !='Error') & (df.query_type=='AAAA')) | (df.query_type=='A')]

    df = df[((df.response_type !='AAAA') & (df.query_type=='A')) | (df.query_type=='AAAA')]

    df['cdn_name'] = df['cname_name'].apply(lambda x: identify_keywords(keywords,x))

    # =============================================================================================
    # =============================================================================================
    # =============================================================================================
    
    # merge AS information
    print('AS identification for day' + day.strftime("%Y-%m-%d"))
    df2 = pd.read_csv(as_info, sep=';')
    df2 = df2.drop_duplicates(['cdn_name', 'asn'])
    df2 = df2.rename(columns={'asn' : 'as', 'cdn_name' : 'query_term'})
    df2['as'] = df2['as'].astype(str)
    df2 = df2[['query_term', 'as']]
    df = pd.merge(df, df2, on='as', how='left')
    df['query_term'] = df['query_term'].fillna('None')

    # fill in CDNs that have not been identified via regexes with their ASN matched CDN
    df.loc[df['cdn_name'] == 'None', 'cdn_name'] = df['query_term']

    # set cdn_name based on AS matching
    df = df.drop(columns=['query_term'])

    # =============================================================================================
    # =============================================================================================
    # =============================================================================================

    print('Counting unique domains for day' + day.strftime("%Y-%m-%d"))

    df['cdn'] = np.where((df['cdn_name']=="None"), False, True)

    df_all = df.groupby(['date','query_type']).agg({'query_name':pd.Series.nunique}).reset_index()
    df_all_cdn = df[df['cdn_name']!='None'].groupby(['date', 'query_type']).agg({"query_name":pd.Series.nunique}).reset_index()
    df_none = df[df['cdn_name']=='None'].groupby(["date","query_type"]).agg({"query_name":pd.Series.nunique}).reset_index()
    df_cdn = df.groupby(['cdn_name','date','query_type']).agg({'query_name':pd.Series.nunique}).reset_index()

    db_for_plots = sqlite3.connect(base_data_directory+"analyzed/dns_analyzed_for_plots-HYBRID-" + day.strftime("%Y-%m-%d") + '.db')
    df_all.to_sql(name='df_all', con=db_for_plots, if_exists='append', index=False)
    df_all_cdn.to_sql(name='df_all_cdn', con=db_for_plots, if_exists='append', index=False)
    df_none.to_sql(name='df_none', con=db_for_plots, if_exists='append', index=False)
    df_cdn.to_sql(name='df_cdn', con=db_for_plots, if_exists='append', index=False)
    db_for_plots.close()

    df = df[['query_name', 'query_type', 'as', 'cname_name', 'response_type', 'response_name', 'cdn_name', 'cdn', 'date']]
    
    db2 = sqlite3.connect(base_data_directory+"analyzed/dns_analyzed_longitudinal-HYBRID-" + day.strftime("%Y-%m-%d") + '.db')
    df.to_sql(name='dns_ana', con=db2, if_exists='append', index=False)
    db2.close()



pool = mp.Pool(processes=NUM_POOL)
pool.map(do_identify, daterange)  # per day
pool.close()
pool.join()