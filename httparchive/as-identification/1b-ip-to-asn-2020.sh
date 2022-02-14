curl -O http://archive.routeviews.org/route-views.isc/bgpdata/2020.01/RIBS/rib.20200101.0000.bz2

echo "[>>>] Converting RIB to database"
pyasn_util_convert.py --single rib.20200101.0000.bz2 ip-asn-2020.dat

echo "[>>>] Fetching AS names"
pyasn_util_asnames.py -o as-names.json

echo "[>>>] Getting unique IP addresses from assets.db"
sqlite3 [...PATH...]/httparchive_processed/2020-01/assets.db 'select distinct ip_addr from assets' >> ip-addr-2020.csv

echo "[>>>] Merging ASN Identification to IP addresses"
python3 ip-as-ident.py ip-asn-2020.dat ip-addr-2020.csv

