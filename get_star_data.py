# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 21:07:03 2020

@author: Amber
"""

import re
import pandas as pd
import config
from glob import glob
from bs4 import BeautifulSoup


def get_star_data():
    stars_dict = {}
    html_files = glob(HTML_OUTPUT_PATH + "*")
    for html_file in html_files:
            stars_dict[html_file.split("\\")[-1][:-4]] = {
                    "Link": html_file}
            html = import_html(html_file)
            stars_dict[star] = add_data(stars_dict[star], html)

def import_html(file_path):
    with open(file_path, "r") as file:
        return BeautifulSoup(file.read(), "html.parser")

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
    infobox = html.find("table", {"class": "infobox"})
    for row in infobox.find_all("tr"):
        if row.th is not None and row.th.text=="Born":
            born_data = row.td.text
    pattern = re.compile("(January|February|March|April|May|June|July|August" +
                         "|September|October|November|December) +\\d{1,2}, +\\d{1,4}")
    match = pattern.search(born_data.text)
    return match.group()

def get_deathdate(html):
    infobox = html.find("table", {"class": "infobox"})
    for row in infobox.find_all("tr"):
        if row.th is not None and row.th.text=="Died":
            born_data = row.td.text
    pattern = re.compile("(January|February|March|April|May|June|July|August" +
                         "|September|October|November|December) +\\d{1,2}, +\\d{1,4}")
    match = pattern.search(born_data.text)
    if match is not None:
        return match.group()
    else:
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
    filled_dataframe = get_star_data()
    filled_dataframe.to_csv(config.FILLED_DATA_OUTPUT, index=False)