import gzip
import glob
import json
import numpy as np
import csv
import datetime

import sys

from multiprocessing import Pool, current_process



def extract(file_list):
    process_id = current_process()._identity[0]

    with open('%s/%s_base_pages.csv' % (DIR, process_id), 'w', encoding='utf-8') as csv_base_pages:

        writer_base_pages = csv.writer(csv_base_pages,
                                       delimiter='|', quotechar='"',
                                       quoting=csv.QUOTE_ALL)
        writer_base_pages.writerow(["base_page", "base_page_cdn", "score_cdn",
                                    "load_time", "ttfb", "visual_complete", "dom_interactive",
                                    "first_contentful_paint", "first_meaningful_paint", "connections", 
                                    "effectiveBps", "effectiveBpsDoc", "num_scripts", "server_rtt", "requests", 
                                    "visualComplete85", "visualComplete90", "visualComplete95", "visualComplete99",
                                    "detected", "detected_apps", "third-parties", "base_page_dns_server", "base_page_cname"
                                    ]
                                  )

        with open('%s/%s_assets.csv' % (DIR, process_id), 'w', encoding='utf-8') as csv_assets:

            writer_assets = csv.writer(csv_assets,
                                       delimiter='|', quotechar='"',
                                       quoting=csv.QUOTE_ALL)
            writer_assets.writerow(["base_page", "asset_url", "asset_content_type", "asset_cdn",
                                    "object_size",
                                    "total_time",
                                    "dns_time", "connect_time", "ssl_time", "ttfb", "download_time", "protocol", 
                                    "securityDetails", "ip_addr"
                                    ]
                                  )

            for file_name in file_list:
                try:
                    with gzip.open(file_name, 'rt', encoding='utf-8') as f:
                        content = json.loads(f.read())

                        base_page = ""
                        base_page_cdn = ""
                        score_cdn = -2
                        load_time = -2
                        ttfb = -2
                        visual_complete = -2
                        dom_interactive = -2
                        first_contentful_paint = -2
                        first_meaningful_paint = -2
                        connections = -2
                        effectiveBps = -2
                        effectiveBpsDoc = -2
                        num_scripts = -2
                        server_rtt = -2
                        requests = -2
                        visualComplete85 = -2
                        visualComplete90 = -2
                        visualComplete95 = -2 
                        visualComplete99 = -2
                        detected = ""
                        detected_apps = ""
                        third_parties = ""
                        base_page_dns_server = ""
                        base_page_cname = ""

                        try:
                            base_page = content['log']['pages'][0]['_URL']
                        except:
                            pass
                        try:
                            base_page_cdn = content['log']['pages'][0]['_base_page_cdn']
                        except:
                            pass
                        try:
                            score_cdn = content['log']['pages'][0]['_score_cdn']
                        except:
                            pass
                        try:
                            load_time = content['log']['pages'][0]['_loadTime']
                        except:
                            pass
                        try:
                            ttfb = content['log']['pages'][0]['_TTFB']
                        except:
                            pass
                        try:
                            visual_complete = content['log']['pages'][0]['_visualComplete']
                        except:
                            pass

                        try:
                            dom_interactive = content['log']['pages'][0]['_domInteractive']
                        except:
                            pass
                        try:
                            first_contentful_paint = content['log']['pages'][0]['_firstContentfulPaint']
                        except:
                            pass
                        try:
                            first_meaningful_paint = content['log']['pages'][0]['_firstMeaningfulPaint']
                        except:
                            pass
                        try:
                            connections = content['log']['pages'][0]['_connections']
                        except:
                            pass
                        try:
                            effectiveBps = content['log']['pages'][0]['_effectiveBps']
                        except:
                            pass
                        try:
                            effectiveBpsDoc = content['log']['pages'][0]['_effectiveBpsDoc']
                        except:
                            pass
                        try:
                            num_scripts = content['log']['pages'][0]['_num_scripts']
                        except:
                            pass
                        try:
                            server_rtt = content['log']['pages'][0]['_server_rtt']
                        except:
                            pass
                        try:
                            requests = content['log']['pages'][0]['_requests']
                        except:
                            pass
                        try:
                            visualComplete85 = content['log']['pages'][0]['_visualComplete85']
                        except:
                            pass
                        try:
                            visualComplete90 = content['log']['pages'][0]['_visualComplete90']
                        except:
                            pass
                        try:
                            visualComplete95 = content['log']['pages'][0]['_visualComplete95']
                        except:
                            pass
                        try:
                            visualComplete99 = content['log']['pages'][0]['_visualComplete99']
                        except:
                            pass
                        try:
                            detected = content['log']['pages'][0]['_detected']
                        except:
                            pass
                        try:
                            detected_apps = content['log']['pages'][0]['_detected_apps']
                        except:
                            pass
                        try:
                            third_parties = content['log']['pages'][0]['_third-parties']
                        except:
                            pass
                        try:
                            base_page_cname = content['log']['pages'][0]['_base_page_cname']
                        except:
                            pass
                        try:
                            base_page_dns_server = content['log']['pages'][0]['_base_page_dns_server']
                        except:
                            pass

                        writer_base_pages.writerow(
                            [base_page, base_page_cdn, score_cdn,
                            load_time, ttfb, visual_complete,
                            dom_interactive, first_contentful_paint, first_meaningful_paint, 
                            connections, effectiveBps, effectiveBpsDoc, num_scripts, server_rtt, 
                            requests, visualComplete85, visualComplete90, visualComplete95, 
                            visualComplete99, detected, detected_apps, third_parties, base_page_cname, base_page_dns_server]
                            )

                        print('[%d] Processing base_page: %s\t[%s]' % (process_id, base_page, file_name), flush=True)

                        for asset_index in range(len(content['log']['entries'])):

                            asset_url = ""
                            asset_content_type = ""
                            asset_cdn = ""
                            asset_object_size = -2
                            asset_total_time = -2
                            asset_dns_time = -2
                            asset_connect_time = -2
                            asset_ssl_time = -2
                            asset_ttfb = -2
                            asset_download_time = -2
                            asset_protocol = ""
                            asset_securityDetails = ""
                            asset_ip_addr = ""

                            try:
                                asset_url = content['log']['entries'][asset_index]['request']['url']
                                # if asset_url == base_page:  # if base_page is in the requests, skip it to not get duplicates
                                #     continue
                            except:
                                pass
                            try:
                                asset_content_type = content['log']['entries'][asset_index]['response']['content']['mimeType']
                            except:
                                pass
                            try:
                                asset_cdn = content['log']['entries'][asset_index]['_cdn_provider']
                            except:
                                pass
                            try:
                                asset_object_size = content['log']['entries'][asset_index]['_objectSize']
                            except:
                                pass
                            try:
                                asset_total_time = content['log']['entries'][asset_index]['_all_ms']
                            except:
                                pass
                            try:
                                asset_dns_time = content['log']['entries'][asset_index]['_dns_ms']
                            except:
                                pass
                            try:
                                asset_connect_time = content['log']['entries'][asset_index]['_connect_ms']
                            except:
                                pass
                            try:
                                asset_ssl_time = content['log']['entries'][asset_index]['_ssl_ms']
                            except:
                                pass
                            try:
                                asset_ttfb = content['log']['entries'][asset_index]['_ttfb_ms']
                            except:
                                pass
                            try:
                                asset_download_time = content['log']['entries'][asset_index]['_download_ms']
                            except:
                                pass
                            try:
                                asset_protocol = content['log']['entries'][asset_index]['_protocol']
                            except:
                                pass
                            try:
                                asset_securityDetails = content['log']['entries'][asset_index]['_securityDetails'] ['protocol']
                            except:
                                pass
                            try:
                                asset_ip_addr = content['log']['entries'][asset_index]['_ip_addr']
                            except:
                                pass

                            writer_assets.writerow(
                                [base_page, asset_url, asset_content_type, asset_cdn,
                                 asset_object_size,
                                 asset_total_time, asset_dns_time, asset_connect_time, asset_ssl_time, asset_ttfb, asset_download_time,
                                 asset_protocol, asset_securityDetails, asset_ip_addr])

                except Exception as e:
                    print(e)
                    with open('%s/errors.txt' % DIR, 'a', encoding='utf-8') as err_file:
                        err_file.write("[%s] %s: %s\n" % (datetime.datetime.now(), file_name, e))
                    continue

        print("[%s] %s finished." % (datetime.datetime.now(), process_id), flush=True)



if __name__ == "__main__":
    global PATH, DIR, NUM_PROCS

    PATH = sys.argv[1]  # read path
    DIR = sys.argv[2]  # out dir
    NUM_PROCS = int(sys.argv[3])

    pool = Pool(processes = NUM_PROCS)

    print("[%s] Getting list of files..." % datetime.datetime.now(), flush=True)
    files = glob.glob('%s/*.har.gz' % PATH)

    print("[%s] Splitting files for workers..." % datetime.datetime.now(), flush=True)
    chunked_list = np.array_split(files, NUM_PROCS)

    print("[%s] Starting workers..." % datetime.datetime.now(), flush=True)
    pool.map(extract, chunked_list)


