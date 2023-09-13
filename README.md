
# ScraperGoogleScholar

ScraperGoogleScholar is a Python tool designed to predict the gender information of authors in scientific papers available on Google Scholar. This tool utilizes scraping methods to extract metadata information from the papers and cross-references the DOIs and authors' names with the Crossref database. To perform the gender predictions, ScraperGoogleScholar leverages APIs such as Genderize and Nationalize.


## Installation

### Module installation 
``` 
    git clone https://github.com/MARIA2M/ScraperGoogleScholar.git
```

### VPN installation 

Frequent searches on the web using Google Scholar may result in temporary bans lasting 24-48 hours. To prevent such situations, we have implemented a solution to bypass this issue and switch to a different proxy server during tool execution. To accomplish this, you will need a VPN service that allows you to switch between various servers. We recommend utilizing https://protonvpn.com/ for this purpose.


## How to use

ScraperGoogleScholar arguments:

| Arguments           | Description                                                                   | Type    |
| ------------------- | ------------------------------------------------------------------------------| ------- |
| \-q, \-\-query      | Query to make on Google Scholar or Google Scholar page link. Default: None    | string  |
| \-n, \-\-numentries | Number of entries to retrieve from the search query. Default: 1000            | integer |
| \-od,\-\-outdir     | Directory where save the output CSV. Default: '.'                             | string  |
| \-v, \-\-verbose    | Shows messages to follow the process execution. Default: True                 | boolean |
| \-h                 | Shows the help                                                                |    --   |


### Steps
    
1. Connect through the vpn to a random server.
2. Execute ScraperGoogleScholar in terminal. The argument **--query**  is required. 
3. If connection fails, switch the proxy manually and press enter to continue.


## Example

In the folder which contains the clonned repository:

Simple execution: 
``` bash
    python -m ScraperGoogleScholar --query "Sex and gender bias in artificial intelligence"
```

Recomended execution:
``` bash
    python -m ScraperGoogleScholar --query "Sex and gender bias in artificial intelligence" --numentries 5 --outdir output 
```


## References 

This tool has been developed based on the following git project: https://github.com/ac-jorellanaf/Google-Scholar-Scraper


## Future updates:

- Search alternative ways to change the proxy server automatically.
- Speed up tool performing.
- Implement other gender predictors.
- Write setup.py.
- Import module to PyPI.
- Implement better error messages.
- Detect error in names format for a proper prediction
