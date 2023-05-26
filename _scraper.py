#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import csv
import time
import requests
from pathlib import Path
from ._proxy import Proxy
from bs4 import BeautifulSoup
from scholarly import scholarly
from ._crossref import CrossrefAPI
from typing import List, Dict, Iterator
from ._demografix import GenderPredictor

class ScraperGooleScholar:

    # Main Params
    AUTHOR_KEY = 'AUTHOR'
    AUTHOR_ID = 'AUTHOR_ID'
    FULL_AUTHORS = 'AUTHOR'
    FIRST_AUTHOR = 'FIRST_AUTHOR'
    LAST_AUTHOR = 'LAST_AUTHOR'
    PUB_YEAR_KEY = 'PUB_YEAR'
    TITLE_KEY = 'TITLE'
    SCHOLAR_LINK_KEY = 'SCHOLAR_LINK'
    PUB_URL_KEY = 'PUB_URL'
    GSRANK_KEY = 'GSRANK'
    NUM_CITATIONS_KEY = 'NUM_CITATIONS'
    DOI_KEY = 'SUGGESTED_DOI'
    FIRST_AUTHOR_GENDER = 'FIRST_AUTHOR_GENDER'
    FIRST_AUTHOR_NATION = 'FIRST_AUTHOR_NATION'
    FIRST_AUTHOR_GENDER_PROBABILITY = 'FIRST_AUTHOR_GENDER_PROBABILITY'
    FIRST_AUTHOR_NATION_PROBABILITY = 'FIRST_AUTHOR_COUNTRY_PROBABILITY'
    LAST_AUTHOR_GENDER = 'LAST_AUTHOR_GENDER'
    LAST_AUTHOR_NATION = 'LAST_AUTHOR_NATION'
    LAST_AUTHOR_PROBABILITY = 'LAST_AUTHOR_PROBABILITY'
    LAST_AUTHOR_GENDER_PROBABILITY = 'LAST_AUTHOR_GENDER_PROBABILITY'
    LAST_AUTHOR_NATION_PROBABILITY = 'LAST_AUTHOR_COUNTRY_PROBABILITY'
    NUM_ATTEMPTS = 20


    def scrapeGS( self, query:str, numentries: int, outdir: str, verbose:bool ) -> object:
        """
        Submit query to GS in order to retrieve the search results from
        the webpage.
        --------------------------------------------------------------------
            query:      Words to search in GS
            numentries: Number of entries to save in csv
            outdir:     Where file is going to be saved
            verbose:    Show messages

        """
        for attempt in range(ScraperGooleScholar.NUM_ATTEMPTS):
            try:

                # Query to GS
                print('Connecting to the server to scrap query results.')

                # search_query = self._scholarly.search_pubs(query, patents=False)
                search_query = scholarly.search_pubs(query, patents=False)

            except Exception as e:
                print('\n{}'.format(e))
                print(
                    '[ Query Error ] There was a problem scraping Google Scholar publications. Attempt {}/{}'.format(attempt + 1, ScraperGooleScholar.NUM_ATTEMPTS))
                attempt = attempt + 1

                # If connection fails because of the proxy, try to find and connect a new one
                print(' '.join("[ Connection Error ]: Connecting to a new proxy. This process can takes times. \
                                                Retrying in 15 seconds once we find a new proxy.".split()))
                Proxy.set_new_proxy()
            else:
                break
        else:
            raise ConnectionError('[ Critical Error ] Too many failed attempts at scraping Google Scholar. Please run the program again.')

        if (verbose): 
            print("Success sending query to Google Scholar.\n")

        return search_query

    def check_availability( self, query:str, verbose: bool ) -> int:
        """
        Check if all sheets are available to be consulted in Google Scholar for a query. 
        This function only works when numentries is 1000.
        ------------------------------------
            :param query:   Search query to GS
            :param verbose: Show messages

        """

        url = f"https://scholar.google.com/scholar?start=940&q={query}"
        count = 940
        page = 940
        
        while True:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            if page == 1000:
                    break

            try:
                next_page_div = soup.find_all('div', {'id': 'gs_n'})
                next_page = next_page_div[0].find_all('a')[-1]
                url = f"https://scholar.google.com{next_page['href']}"
                time.sleep(15)
                count += 10  
                page += 10

            except:
                print(f"[ Numentries Error ] sheet {page} could not be founded")
                time.sleep(15)
                page += 10
                continue
            
        if (verbose): 
            print(f"Total number of links for query '{query}': {count}")
        
        return count


    def get_entries( self, search_query:Iterator, numentries:int, verbose:bool ) -> List[Dict[str,str]]:
        """
        Process data information from Google Scholar query.
        Cross-reference the DOIs and authors' names with the Crossref database.
        Predict gender of the authors.
        ------------------------------------
            :param search_query: Object with Google Scholar query result
            :param numentries:   Number of entries to recover 
            :param verbose:      Show messages

        """

        attempt = 0
        entries = [dict() for x in range(numentries)]
        for i in range(numentries):
            for attempt in range(ScraperGooleScholar.NUM_ATTEMPTS):
                try:
                    # Accessing to the each element of the query object 
                    entrydict = next(search_query)
                   
                    # Authors info
                    authors = re.sub(r'[\[\]\']', '', str(
                        entrydict['bib'][ScraperGooleScholar.AUTHOR_KEY.lower()]).replace(',', ';'))

                    # Authors IDs
                    authors_ids = re.sub(r'[\[\]\']', '', str(
                        entrydict[ScraperGooleScholar.AUTHOR_ID.lower()]).replace(',', ';'))

                    # Year of publication info
                    pubyear = str(entrydict['bib'][ScraperGooleScholar.PUB_YEAR_KEY.lower()])

                    # Title of the article
                    title = str(entrydict['bib'][ScraperGooleScholar.TITLE_KEY.lower()])

                    # Publication URL
                    if (not ('pub_url' in entrydict)):
                        entrydict['pub_url'] = ''

                    crossref_doi, crossref_author = CrossrefAPI.petition( authors, pubyear, title, i, verbose )

                    # DOIs 
                    doi = CrossrefAPI.get_doi( crossref_doi )
     
                    # All authors
                    authors_fullnames = CrossrefAPI.get_fullname_authors( crossref_author )
                    
                    # First author
                    fauthor_name, fauthor_surname = CrossrefAPI.get_fist_author( crossref_author )
                    fauthor_nation = GenderPredictor.get_nation( fauthor_name, fauthor_surname ) 
                    fauthor_gender = GenderPredictor.get_gender( fauthor_name, fauthor_surname, fauthor_nation) 
                   
                    first_author = f"{fauthor_name} {fauthor_surname}"

                    # Last author 
                    lauthor_name, lauthor_surname = CrossrefAPI.get_last_author( crossref_author )
                    lauthor_nation = GenderPredictor.get_nation( lauthor_name, lauthor_surname ) 
                    lauthor_gender = GenderPredictor.get_gender( lauthor_name, lauthor_surname, lauthor_nation ) 

                    last_author = f"{lauthor_name} {lauthor_surname}"
                    
                    # Save information of each row in the csv
                    entries[i] = {
                        # ScraperGooleScholar.AUTHOR_KEY: authors,
                        ScraperGooleScholar.FULL_AUTHORS: authors_fullnames,
                        ScraperGooleScholar.FIRST_AUTHOR: first_author,
                        ScraperGooleScholar.LAST_AUTHOR: last_author,
                        ScraperGooleScholar.PUB_YEAR_KEY: pubyear,
                        ScraperGooleScholar.TITLE_KEY: title,
                        ScraperGooleScholar.SCHOLAR_LINK_KEY: 'https://scholar.google.com' + entrydict['url_scholarbib'].replace('?q=info:', '?cluster=').replace(':scholar.google.com/&output=cite&scirp=' + str(i), ''),
                        ScraperGooleScholar.PUB_URL_KEY: str(entrydict[ScraperGooleScholar.PUB_URL_KEY.lower()]),
                        ScraperGooleScholar.GSRANK_KEY: str(entrydict[ScraperGooleScholar.GSRANK_KEY.lower()]),
                        ScraperGooleScholar.NUM_CITATIONS_KEY: str(
                            entrydict[ScraperGooleScholar.NUM_CITATIONS_KEY.lower()]),
                        ScraperGooleScholar.DOI_KEY: doi,
                        ScraperGooleScholar.FIRST_AUTHOR_GENDER: fauthor_gender[first_author]['name']['gender'],
                        ScraperGooleScholar.FIRST_AUTHOR_GENDER_PROBABILITY: fauthor_gender[first_author]['name']['probability'],
                        ScraperGooleScholar.FIRST_AUTHOR_NATION: fauthor_nation[first_author]['surname']['country_id'],
                        ScraperGooleScholar.FIRST_AUTHOR_NATION_PROBABILITY:  fauthor_nation[first_author]['surname']['probability'],
                        ScraperGooleScholar.LAST_AUTHOR_GENDER: lauthor_gender[last_author]['name']['gender'],
                        ScraperGooleScholar.LAST_AUTHOR_GENDER_PROBABILITY: lauthor_gender[last_author]['name']['probability'],
                        ScraperGooleScholar.LAST_AUTHOR_NATION: lauthor_nation[last_author]['surname']['country_id'],
                        ScraperGooleScholar.LAST_AUTHOR_NATION_PROBABILITY: lauthor_nation[last_author]['surname']['probability']
                    }

                    # Show messages that informs you about the number of entries processed
                    if ((i + 1) % 10 == 0 or (i + 1) == numentries):
                        print('{} entries scraped'.format(i + 1))
                     
                    # if (verbose and (i + 1) % 10 == 0 or (i + 1) == numentries):
                    #     print('{} entries scraped'.format(i + 1))
                        
                except Exception as e:
                    print('\n{}'.format(e))
                    print(
                        '[ Save Error ] There was a problem scraping a Google Scholar entry. Retrying. Attempt {}/{}'.format(attempt + 1, ScraperGooleScholar.NUM_ATTEMPTS))
                    attempt = attempt + 1

                    # If connection fails because of the proxy, try to find and connect a new one
                    print(' '.join("[ Connection Error ]: Connecting to a new proxy. This process can takes times. \
                                                Retrying in 15 seconds once we find a new proxy.".split()))
                    Proxy.set_new_proxy()
                else:
                    break
            else:
                print(
                    '[ Critical Error ] Too many failed attempts at scraping Google Scholar. Please run the program again in 24h.')
        
        return entries


    def write( self, query:str, entries: List[Dict[str,str]], numentries:int, outdir:str ) -> None:
        """
        Write CSV with data.
        ------------------------------------
            :param query:      Search query to GS
            :param entires:    Dict with data
            :param numentries: Number of entries to recover 
            :param outdir:     Folder where store CSV with results

        """

        # Final csv file
        date = time.strftime('%Y-%m-%dT%H%M%S', time.localtime(time.time()))
        regex = re.compile('[^a-zA-Z]')
        outfile = Path(outdir) / (date + '_' +
                                    regex.sub('', query.lower())[:15] + '.csv')

        # Create and save information in csv
        with open(str(outfile), 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                ScraperGooleScholar.FULL_AUTHORS, 
                ScraperGooleScholar.FIRST_AUTHOR, 
                ScraperGooleScholar.LAST_AUTHOR, 
                ScraperGooleScholar.AUTHOR_ID, 
                ScraperGooleScholar.PUB_YEAR_KEY,
                ScraperGooleScholar.TITLE_KEY, 
                ScraperGooleScholar.SCHOLAR_LINK_KEY, 
                ScraperGooleScholar.PUB_URL_KEY,
                ScraperGooleScholar.GSRANK_KEY, 
                ScraperGooleScholar.NUM_CITATIONS_KEY,
                ScraperGooleScholar.DOI_KEY,
                ScraperGooleScholar.FIRST_AUTHOR_GENDER,
                ScraperGooleScholar.FIRST_AUTHOR_GENDER_PROBABILITY,
                ScraperGooleScholar.FIRST_AUTHOR_NATION,
                ScraperGooleScholar.FIRST_AUTHOR_NATION_PROBABILITY,
                ScraperGooleScholar.LAST_AUTHOR_GENDER,
                ScraperGooleScholar.LAST_AUTHOR_GENDER_PROBABILITY,
                ScraperGooleScholar.LAST_AUTHOR_NATION,
                ScraperGooleScholar.LAST_AUTHOR_NATION_PROBABILITY
            ]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for i in range(numentries):
                writer.writerow(entries[i])

        # return outfile