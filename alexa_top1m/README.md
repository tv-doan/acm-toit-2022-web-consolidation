### Overview of Files

Download of DNS measurement data and Alexa Top 1M toplists required, see below.

- `alexatop1m-dir-tree.txt`: overview of directory structure as an example
- `1a-download-alexa.py`: download Alexa Top 1M DNS measurements from OpenINTEL
- `1b-unpack_alexa_toplists.py`: unpacks Alexa Top 1M toplists of observed month from archives (data not provided in this repository; formats may vary depending on sources)
  - `num-alexa-sites.csv`: number of domains in Alexa Top 1M per day for observed month
- `1c-process_alexa.py`: pre-processing relevant Alexa Top 1M data from `.avro` files for specified date range (here: one month) into a single database
- `2-hybrid-identification-alexa.py`: identification of CDIs through regexes and ASNs; counts unique domains for each CDI per day (one database for each day)
  - `asn_cdns.csv`: CDI <-> ASN mappings
- `3-merge-identifications.py`: merges daily databases for whole month together into one
- `4-add-ranking-information.py`: adds alexa rank to each domain, based on unpacked Alexa Top 1M toplists (from `1b-unpack_alexa_toplists.py`)
- `5-Aggregate_CDNPenetration_ALEXA-HYBRID.ipynb`: aggregation and calculation of CDI penetration
- `6-alexatop1m-CDN-pen-plots.ipynb`: visualization of aggregations
  - `./plots/`: plots saved as `.pdf`
