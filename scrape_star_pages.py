# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:17:35 2020

@author: Amber
"""

import requests
import time
import pandas as pd
import config
from bs4 import BeautifulSoup

def scrape_star_pages(redownload=False):
    stars_dict = load_stars_dict()
    stars_dict = {star:{"Link": stars_dict[star]} for star in stars_dict.keys()}
    for star in stars_dict.keys():
        if redownload:
            #include 1 second delay between wikipedia hits
            time.sleep(1)
            html = scrape_star(star, stars_dict[star]["Link"])
            if is_fictional(html):
                del stars_dict[star]
            elif is_group(html):
                members = get_members(html)
                for member in members.keys():
                    html = scrape_star(member, members[member])
                    stars_dict[star] = add_data(stars_dict[star], html)
            else:
                stars_dict[star] = add_data(stars_dict[star], html)
        else:
            html = import_html(star)
            stars_dict[star] = add_data(stars_dict[star], html)
        
    return pd.DataFrame(stars_dict).transpose().reset_index(drop=False)

def load_stars_dict():
    stars = pd.read_csv(config.STARS_OUTPUT)
    return stars.set_index(["Name"]).to_dict()["Link"]

def scrape_star(name, link):
    html = get_star_html(link)
    export_html(name, html)
    return html

def get_star_html(link):
    req = requests.get(link)
    return str(BeautifulSoup(req.content, "html.parser"))

def export_html(name, html):
    with open(config.HTML_OUTPUT_PATH + name +".txt", "w") as file:
        file.write(html)

def is_group(html):
    pass

def get_members(html):
    pass

def is_fictional(html):
    pass

def import_html(name):
    pass

def add_data(star_dict, html):        
    star_dict["Birthdate"] = get_birthdate(html)
    star_dict["Deathdate"] = get_deathdate(html)
    star_dict["Spouses"] = get_spouses(html)
    star_dict["Children"] = get_children(html)
    star_dict["NetWorth"] = get_networth(html)
    star_dict["Nationality"] = get_nationality(html)
    star_dict["Gender"] = get_gender(html)
    return star_dict

def get_birthdate(html):
    return ""

def get_deathdate(html):
    return ""

def get_spouses(html):
    return ""

def get_children(html):
    return ""

def get_networth(html):
    return ""

def get_nationality(html):
    return ""

def get_gender(html):
    return ""

if __name__ == "__main__":
    filled_dataframe = scrape_star_pages(redownload=False)
    filled_dataframe.to_csv(config.FILLED_DATA_OUTPUT, index=False)