#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import time
import typing 
from pathlib import Path
from ._scraper import ScraperGooleScholar


def run ( query: str, numentries: int, outdir: str, verbose:bool ):
    """
    General options management
    --------------------------------------------------------------------
        :param query:      Search query to GS
        :param numentries: Number of entries to recover 
        :param outdir:     Folder where store CSV with results
        :param verbose:    Show messages

    """

    scraper = ScraperGooleScholar()

    # Check if previous download was runed
    dwonloaded_entries = scraper.get_downloaded_entries(query, outdir) 
    entries_to_download = [ str(i+1)  for i in range(numentries) if not str(i+1) in dwonloaded_entries ]
   
    if (verbose): 
        print(f"Number of entries to download ({len(entries_to_download)}/{numentries})")


    # Query to Google Scholar web
    response = scraper.scrapeGS(query, numentries, outdir, verbose)

    # Check if all the sheets are availables to consult
    if numentries == 1000:
        numentries = scraper.check_availability( query, verbose )

    for numentry in range(numentries):

        # Main info from the query entries
        entry = scraper.get_entry( response, numentry + 1, numentries, entries_to_download, verbose)
       
        # Export to csv
        if entry is not None:
            scraper.write(query, entry, numentry, outdir)


def main():

    # CMD Arguments
    parser = argparse.ArgumentParser(
        description='GSraper is python tool to search and scrap metadata from scientific papers using Google Scholar, Crossref')

    parser.add_argument('-q', '--query', type=str, default=None,
                        help='Set a custom in-line query with the search to Google Scholar.')
    
    parser.add_argument('-n', '--numentries', type=int, default=1000,
                        help='Set of entries to be retrieved from the query.')

    parser.add_argument('-od', '--outdir', type=str, default=".",
                        help='Set a custom path for the directory where the search .CSV files should be stored.')

    parser.add_argument('-v', '--verbose', type=bool, default=True,
                        help='Verbose mode.')

    args = parser.parse_args()
 

    # Arguments validation
    if args.query is None:
        print("[ Input Error ] Provide at least one of the following arguments: --query or -q")
        sys.exit()

    if args.numentries is None and args.numentries > 1000:
        print("[ Input Error ] Provide a number in a range of 0-1000 or provide at \
                    least one of the following arguments: --numentries or -n")
        sys.exit()

    if args.outdir is None:
        print("[ Input Error ] Provide at least one of the following arguments: --outdir or -od")
        sys.exit()
    else:
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        outdir = Path(os.path.join(args.outdir, date))
        outdir.mkdir(parents=True,exist_ok=True)

    if args.verbose is None:
        print("[ Input Error ] Provide at least one of the following arguments: --verbose or -v")
        sys.exit()


    if (args.verbose):
        print("Google Scholar Scraper.")
        print("Query processed:")
        print(f"query: {args.query} - {args.numentries} entries.")
        print(f"Output path: {args.outdir}")

    # Execution
    run ( args.query, args.numentries, outdir, args.verbose )

if __name__ == "__main__":
    main()
    print("""\nWork completed!\n""")