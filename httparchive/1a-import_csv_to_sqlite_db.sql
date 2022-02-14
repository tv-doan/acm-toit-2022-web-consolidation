.mode csv
.separator |
.import 1_base_pages.csv base_pages
.import "|tail -n +2 2_base_pages.csv" base_pages
.import "|tail -n +2 3_base_pages.csv" base_pages
.import 1_assets.csv assets
.import "|tail -n +2 2_assets.csv" assets
.import "|tail -n +2 3_assets.csv" assets
.exit
