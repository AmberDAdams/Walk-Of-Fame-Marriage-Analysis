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

def scrape_star_pages():
    stars_dict = load_stars_dict()
    for star in stars_dict.keys():
        #include greater than 1 second delay between wikipedia hits
        time.sleep(1.2)
        html = get_star_html(stars_dict[star]["Link"])
        if is_fictional(html):
            del stars_dict[star]
        elif is_group(html):
            members = get_members(html)
            for member in members.keys():
                html = get_star_html(members[member])
                export_html(member, html)
        else:
            export_html(star, str(html))

def load_stars_dict():
    stars = pd.read_csv(config.STARS_OUTPUT)
    stars_dict = stars.set_index(["Name"]).to_dict()["Link"]
    stars_dict = {star:{"Link": stars_dict[star]} for star in stars_dict.keys()}
    return stars_dict

def get_star_html(link):
    req = requests.get(link)
    return BeautifulSoup(req.content, "html.parser")

def export_html(name, html_str):
    with open(config.HTML_OUTPUT_PATH + name +".txt", "w", encoding="utf-8") as file:
        file.write(html_str)

def is_group(html):
    catlinks = html.find("div", {"class": "mw-normal-catlinks"})
    categories = " ".join([cat.text for cat in catlinks.find_all("li")])
    if "births" not in categories and "fictional characters" not in categories:
        return True
    else:
        return False

def get_members(html):
    return {}

def is_fictional(html):
    catlinks = html.find("div", {"class": "mw-normal-catlinks"})
    categories = " ".join([cat.text for cat in catlinks.find_all("li")])
    if "fictional characters" in categories:
        return True
    else:
        return False

if __name__ == "__main__":
    scrape_star_pages()
