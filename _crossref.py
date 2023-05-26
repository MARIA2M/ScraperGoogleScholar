#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
            print(f"Query to Crossref for: {num}) {pub_title[:60]}...")

        try:
            # Query to Crossref to retrieve doi for each entry
            cr = Crossref()
            response = cr.works(query=str(pub_authors.replace(';', ',').replace('"', '').lower() + ' ' +
                                        pub_year + ' "' + pub_title.lower() + '"'), select='DOI,author', limit=1)['message']['items'][0]
            
            # Validate response
            crossref_doi = response['DOI'] if 'DOI' in response else ''
            crossref_author = response['author'] if 'author' in response else [{'given': 'NA', 'family': 'NA'}]

        except Exception as e:
                print('\n{}'.format(e))
                print(
                    '[ Connection Error ] There was a problem scraping a Crossref entry.')
                raise

        return crossref_doi, crossref_author


    def get_doi ( doi: str ) -> str:
       """ Doi from paper """
       return '' if not doi else 'https://doi.org/' + doi


    def get_fullname_authors ( authors: str ) -> str:
        """ Fullname from authors """   
        fullname_authors = []
        for author in authors:
            if 'given' in author:
                full_names = f"{author['given']} {author['family']}"
                fullname_authors.append(full_names)

        return ', '.join(fullname_authors)


    def get_fist_author ( authors: str ) -> str:
        """ Name and surname from first author """
        for author in authors:
            if 'given' in author:
                return author['given'], author['family']


    def get_last_author ( authors: str ) -> str:
        """ Name and surname from last author """
        for author in reversed(authors):
            if 'given' in author:
                return author['given'], author['family']
       

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


        
