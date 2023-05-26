#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup

class Proxy: 
    """ """

    def set_new_proxy():
        """
        Set new proxy if the request to Google Scholar fails 
        because of too many queries to the website.
        --------------------------------------------------------------------
        """
        while True:
            inp = input('You have been blocked, try changing your IP or using a VPN. '
                    'Press Enter to continue downloading, or type "exit" to stop and exit....')
            if inp.strip().lower() == "exit":
                sys.exit()
                #return False

            elif not inp.strip():
                print("Wait 15 seconds...")
                time.sleep(15)
                return True
