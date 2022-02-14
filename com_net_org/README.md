### Overview of Files

No additional files required.

- `asn_cdns.csv`: CDI <-> ASN mappings
- `[xyz]_by_asn.csv`: numbers of domains in the [xyz] TLD namespace, whose `A` records for apex/`www.` domains resolves to the ASN denoted in the column, by day (row)
- `[xyz]_by_asn_processed.csv`: previous file with aggregated counts and mapped to each CDI (generated through `_aux-comnetorg-asn-processing.ipynb`)
- `[xyz]stats.csv`: total number of domains in [xyz] TLD namespace
- `1-comnetorg-asn-plots.ipynb`: analysis notebook; generates time series plot to visualize CDI penetration for `.com`, `.net`, and `.org` over the years
  - `./comnetorg_plots/`: plot(s) saved as `.pdf`
