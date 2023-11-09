#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict
from pyagify.agify import GenderizeClient, NationalizeClient

class GenderPredictor:

    def get_gender ( author_name: str, author_surname: str, nationality: str ) -> Dict[str,Dict[str,str]]:
        """
        Predict gender of the name.
        ------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname
            :param nationality:    Author's surname nation

        """
        AUTHOR_GENDER = {'genderize':{ 'name':{'gender':"", 'probability':""}}}

        gender = GenderizeClient()
        author = f"{author_name} {author_surname}"
        gender_authors = { author : AUTHOR_GENDER['genderize'] }
        
        # Exceptions
        if "-"  in author_name.replace("‐", "-"):
            author_name = author_name.replace("‐", "-").split("-")[0]
        
        if "." in author_name.replace(".", "."):
            author_name = author_name.replace(".", ".").split(".")[0]

        if author != ' ' :
            nation = nationality[author]
            gender_authors[author]['name']['gender'] = gender.get_raw(author_name, nation['surname']['country_id'])['gender']
            gender_authors[author]['name']['probability'] = gender.get_raw(author_name, nation['surname']['country_id'])['probability']
        else:
            gender_authors[author]['name']['gender'] = ""
            gender_authors[author]['name']['probability'] = ""

        return gender_authors


    def get_nation( author_name: str, author_surname: str ) -> Dict[str,Dict[str,str]]:
        """
        Predict nation of surname. If fails, use name.
        ------------------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname

        """
        AUTHORS_NATION = {'nationalize':{'surname':{'country_id':"",'probability':""}}}

        nation = NationalizeClient()
        author = f"{author_name} {author_surname}"
        nation_author = { author : AUTHORS_NATION['nationalize'] }

        # Exceptions
        if "-"  in author_surname.replace("‐", "-"):
            author_surname = author_surname.replace("‐", "-").split("-")[0]

        if author != ' ' :
            if not nation.get_raw(author_surname)['country']:
                country = nation.get_raw(author_name)['country']
                nation_author[author]['surname']['country_id'] = country[0]['country_id'] if country else ""
                nation_author[author]['surname']['probability'] = country[0]['probability'] if country else  0.0
                
            else:
                country = nation.get_raw(author_surname)['country']
                nation_author[author]['surname']['country_id'] = country[0]['country_id'] if country else ""
                nation_author[author]['surname']['probability'] = country[0]['probability'] if country else 0.0
        
        return nation_author
