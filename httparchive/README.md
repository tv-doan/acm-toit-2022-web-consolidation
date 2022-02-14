### Overview of Files

Before running the scripts, download the raw measurement data from Google Cloud Storage:

E.g., multithreaded (`-m`) copying (`cp`) of all files from a bucket (`gs://httparchive/[...]/*`) to local directory (`[dst]`)  
```
# gsutil -m cp gs://httparchive/[...]/* [dst]
```  
or, e.g., with rsync  
```
# gsutil -m rsync -r gs://httparchive/[...]/ [dst]
```  

- `1-httparchive-extract.py`: reads and unpacks `WebPagetest` measurement data from HTTP Archive (zipped `.har` files); extracts relevant information for all pages and resources
  - Usage, e.g.: `python3 -u ./httparchive-extract.py [/path/to/raw/data/] [/path/for/extracted/data/] [number of processes to use] > [/path/to/save/output/]`
  - This will create separate `.csv` files for each process, which all need to be imported into a `sqlite` database
  - `1a-import_csv_to_sqlite_db.sql`: example script (needs to be adjusted for number of files/processes) for importing into single database:
    ```
    # in directory with extracted CSVs from processes:
    # sqlite3 [/some/database/name].db < 1a-import_csv_to_sqlite_db.sql
    ```

  - `./as-identification/`: scripts to map ASNs to IP addresses occurring in HTTP Archive data
    - `1b-ip-to-asn-2020.sh`: shell script that downloads BGP data for ASN mapping (using `pyasn`); fetches AS names (using `pyasn`); queries unique IP addresses from assets database; executes the lookup/mapping
      - outputs: `rib.20200101.0000.bz2 ip-asn-2020.dat`, `ip-asn-2020.dat`, `as-names.json`, `ip-addr-2020.csv`, `ip-asn-map-full-2020.csv`
    - `ip-as-ident.py`: Python script which maps IP addresses to ASNs based on BGP information
    - `asn_cdns.csv`: CDI <-> ASN mappings

- `2-process-httparch-assets.py`: go through all extracted page resources (also page assets) and add/modify information for analysis

- `3a-extract-basepages-from-assets.sql`: extract additional base page information from resources/assets into separate database table
- `3b-process-httparch-basepages.py`: go through all base pages and base pages extracted from resources (`3a`) and add/modify information for analysis

- `4-main-analyses.ipynb`: loads pre-processed data and performs most analyses presented in the paper, including some case studies 
  - `./dills/`: stored Python objects to save intermediate results for sharing (provided in this repository)
  - `./cdfs/`: values and percentiles for calculated CDFs
  - `./plots/`: plots from notebooks below saved as `.pdf`
  - `plots+tables.ipynb`: notebook for visualization of data (plots and tables) presented in paper; uses `.dill` files
  - `shared-asset-analyses.ipynb`: analyses on shared resources, see &sect;4.2.3 of paper
  - `misc-analyses.ipynb`: some (additional) analyses for case studies in &sect;5.2 and &sect;5.4 of paper
  - `performance-analyses.ipynb`: analyses for case study in &sect;5.5 of paper
