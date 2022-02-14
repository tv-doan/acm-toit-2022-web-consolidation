### An Empirical View of Consolidation on the Web

Trinh Viet Doan<sup>&sect;</sup> | Roland van Rijswijk-Deij<sup>&para;</sup> | Oliver Hohlfeld<sup>&Dagger;</sup> | Vaibhav Bajpai<sup>&sect;</sup>  

<sup>&sect;</sup> Technical University of Munich, <sup>&para;</sup> University of Twente \& NLnet Labs, <sup>&Dagger;</sup> Brandenburg University of Technology   

[ACM TOIT 2022](https://dl.acm.org/journal/toit), accepted for publication in 2022. [Pre-print TBD]()  
DOI: [10.1145/3503158](https://doi.org/10.1145/3503158).

---

### Datasets

The datasets analyzed in this study cover three different aspects and were measured from two different vantage points:  
- Aggregates of daily DNS measurements for all `.com`, `.net`, and `.org` domains, measured from NL by OpenINTEL [[1]](https://openintel.nl/coverage/)
- Daily DNS measurements for `A` and `AAAA` records of Alexa Top 1M webpages, measured from NL by OpenINTEL (publicly available) [[2]](https://data.openintel.nl/data/alexa1m/)
- Page load measurements of Google CrUX webpages via `WebPagetest`, measured from US by HTTP Archive (publicly available)
[[3]](https://httparchive.org/faq)
[[4]](https://console.cloud.google.com/bigquery?project=httparchive&d=pages&p=httparchive&page=dataset)
[[5]](https://console.cloud.google.com/storage/browser/httparchive;tab=objects?prefix=&forceOnObjectsSortingFiltering=false)

### Requirements

[`requirements.txt`](https://github.com/tv-doan/acm-toit-2022-web-consolidation/blob/master/requirements.txt) lists most of the required Python dependencies, which can, e.g., be installed using `pip3 install -r requirements.txt`.  

For the calculation of CDFs, [`Pmf.py`](http://greenteapress.com/thinkstats/Pmf.py) and [`Cdf.py`](http://greenteapress.com/thinkstats/Cdf.py) from [Think Stats](https://greenteapress.com/wp/think-stats-2e/) are used.

### Repeating the Analysis

This repository contains most of the required scripts to repeat the analysis presented in the paper. The scripts for each of the datasets listed above are separated into different directories of in this repository.  
These scripts include (pre-)processing, analysis, and visulization of the data. Note that the code has to be adjusted (in particular paths) and does not necessarily run "out-of-the-box", which is why we do not provide a single batch script to execute.  
Instead, **the code should treated as ***reference*** for repeating the analyses.**

To repeat the analysis, first download the data from the above mentioned sources.  
For the HTTP Archive data in particular, the download from the respective Google Cloud Storage bucket [[5]](https://console.cloud.google.com/storage/browser/httparchive;tab=objects?prefix=&forceOnObjectsSortingFiltering=false)
via `gsutil` [[6]](https://cloud.google.com/storage/docs/gsutil) is recommended (this will require multiple TB of disk space).  
Alternatively, you can also analyze the data and create dumps through the Google BigQuery.

With the raw data, adjust the number of processes, paths (most denoted by `[...PATH...]`), ... in the Python scripts and `jupyter` notebooks accordingly,  
then run them in numerical order (by filename, see READMEs in the respective directories) to process the data
(some intermediate steps might be necessary).  
**Note that these processes can run for a very long time**.  

### Other Notes and Disclaimers

- Variables in the code might be named `*cdn*` (as in Content Delivery Network) but typically refer to CDIs (Content Delivyer Infrastructures) instead, i.e., they also include cloud providers/DDoS protection infrastructures.
- The used auxiliary and meta data (e.g., ASNs and regular expressions for CDIs, or options for adblock expressions) can be adjusted or complemented to improve the identification process.
- The analyses were performed on multiple machines with different hardware specs, so there might be some naming inconsistencies.
- The analyses are not optimized for resource consumption or runtime efficiency; use at own risk.
- Synchronizing the data from the Google Storage bucket via `gsutil` to local storage creates millions of small files, which can result in partial failures (connection and/or disk). 

### Contributors / Acknowledgments

The majority of the code basis for the Alexa Top 1M analysis was written by Justus Fries<sup>&sect;</sup>.

### Contact

Please feel welcome to contact the corresponding author (Trinh Viet Doan [<doan@in.tum.de>]) for further details.