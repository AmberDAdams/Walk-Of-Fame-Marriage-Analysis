# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:17:35 2020

@author: Amber
"""

import requests
import pandas as pd
import config
from bs4 import BeautifulSoup

def scrape_star_pages(redownload=False):
    stars_dict = load_stars_dict()
    stars_dict = {star:{"Link": stars_dict[star]} for star in stars_dict.keys()}
    for star in stars_dict.keys():
        if redownload:
            #include 1 second delay between wikipedia hits
            html = scrape_star(star, stars_dict[star]["Link"])
            export_html(star, html)
        else:
            html = import_html(star)
            
        stars_dict[star]["Birthdate"] = get_birthdate(html)
        stars_dict[star]["Deathdate"] = get_deathdate(html)
        stars_dict[star]["Spouses"] = get_spouses(html)
        stars_dict[star]["Children"] = get_children(html)
        stars_dict[star]["NetWorth"] = get_networth(html)
        stars_dict[star]["Nationality"] = get_nationality(html)
        stars_dict[star]["Gender"] = get_gender(html)
        
    return pd.DataFrame(stars_dict)

def load_stars_dict():
    stars = pd.read_csv(config.STARS_OUTPUT)
    return stars.set_index(["Name"]).to_dict()["Link"]

def scrape_star(name, link):
    pass

def get_star_html(link):
    pass

def export_html(name, link):
    pass

def is_group(html):
    pass

def is_fictional(html):
    pass

def import_html(name):
    pass

def get_birthdate(html):
    pass

def get_deathdate(html):
    pass

def get_spouses(html):
    pass

def get_children(html):
    pass

def get_networth(html):
    pass

def get_nationality(html):
    pass

def get_gender(html):
    pass

