#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import typing 
import requests
from habanero import Crossref

class CrossrefAPI:

    def petition ( pub_authors: str, pub_year:str, pub_title: str, num: int, verbose:bool ) -> str:
        """
        Query to Crossref database.
        ------------------------------------
            :param pub_authors: Paper authors
            :param pub_year:    Year of paper
            :param pub_title:   Title of paper
            :param verbose:     Show messages

        """
        if (verbose): 
            #sys.stdout.write(f"Crossref query for: {num}) {pub_title[:60]}...")
            print(f"Crossref qury for: {num} {pub_title[:60]}...", end='', flush=True)

        try:
            # Query to Crossref to retrieve doi for each entry
            cr = Crossref()
            response = cr.works(query=str(pub_authors.replace(';', ',').replace('"', '').lower() + ' ' +
                                        pub_year + ' "' + pub_title.lower() + '"'), select='DOI,author', limit=1)['message']['items'][0]


            # Validate response
            crossref_doi = response['DOI'] if 'DOI' in response else ''
            crossref_author = response['author'] if 'author' in response else [{'given': 'NA', 'family': 'NA'}]
            
            # Validate query and response are the same
            scholarly_first_surname = pub_authors.split(';')[0].split(' ')[-1]
            chrossref_first_surname = crossref_author[0]['family'].split(' ')[-1] \
                                        if ' ' in crossref_author[0]['family'] else crossref_author[0]['family']

            if scholarly_first_surname != chrossref_first_surname:
                crossref_author = [{'given':pub_author.rsplit(" ", 1)[0].strip(),'family':pub_author.rsplit(" ", 1)[-1].strip()} \
                                    for pub_author in pub_authors.split(';')] 
                STATUS = 'MISSING'
            elif '.' in crossref_author[0].get('given', '') or '.' in crossref_author[0].get('family', ''):
                STATUS = 'REVIEW'
            else:
                STATUS = 'PASS'

        except Exception as e:
                print('\n{}'.format(e))
                print(
                    '[ Connection Error ] There was a problem scraping a Crossref entry.')
                raise

        if (verbose): 
            print(f"...[{STATUS}]\n")
            #sys.stdout.write('\r' + f"Crossref query for: {num}) {pub_title[:60]}...[{STATUS}]\n")
            #print(f"\rCrossref qury for: {num}) {pub_title[:60]}...[{STATUS}]")
            #print(f"Crossref qury for: {num}) {pub_title[:60]}...[{STATUS}]")

        return crossref_doi, crossref_author, STATUS


    def get_doi ( doi: str ) -> str:
        """ Doi from paper """
        return '' if not doi else 'https://doi.org/' + doi


    def get_fullname_authors ( authors: str ) -> str:
        """ Fullname from authors """   
        fullname_authors = []
        for author in authors:
            if 'given' in author:
                full_name = f"{author['given']} {author['family']}"
                fullname_authors.append(full_name)
            else:
                full_name = author['family']
                fullname_authors.append(full_name)
        return ', '.join(fullname_authors)


    def get_fist_author ( authors: str, google_authors: str ) -> str:
        """ Name and surname from first author """
        for author in authors:
            if 'given' in author:
                return author['given'], author['family']
            else:
                google_surnames = [ fullname_google.split()[-1] for fullname_google in google_authors.split(';') ]
                surname = list(filter(lambda surn: surn in author['family'], google_surnames))[0].strip()
                name = author['family'].replace(surname, "").strip()
                return name, surname


    def get_last_author ( authors: str, google_authors:str ) -> str:
        """ Name and surname from last author """
        for author in reversed(authors):
            if 'given' in author:
                return author['given'], author['family']
            else: 
                google_surnames = [ fullname_google.split()[-1] for fullname_google in google_authors.split(';') ]
                surname = list(filter(lambda surn: surn in author['family'], google_surnames))[-1].strip()
                name = author['family'].replace(surname, "").strip()
                return name, surname

    # def get_bibtex( doi: str) -> str:
    #     """ """
    #     try:
    #         url_bibtex = "http://api.crossref.org/works/" + DOI + "/transform/application/x-bibtex"
    #         x = requests.get(url_bibtex)
    #         if x.status_code == 404:
    #             return ""
    #         return str(x.text)
    #     except Exception as e:
    #         print(e)
    #         return ""


        
