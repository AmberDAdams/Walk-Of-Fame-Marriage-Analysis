# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 22:59:28 2020

@author: Amber
"""
import requests
import pandas as pd
import config
from bs4 import BeautifulSoup

def scrape_walk_of_fame():
    soup = get_soup(config.WALK_OF_FAME_URL)
    links = extract_links(soup)
    stars = get_star_table(soup)
    stars = add_links_to_table(stars, links, "Actor")
    return stars

def get_soup(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup

def extract_links(soup):
    a_tags = soup.find_all("a")
    links = {link.text:config.WIKIPEDIA_URL+get_href(link) for link in a_tags}
    return links

def get_href(a_tag):
    #there isn't always a link, we have to go through and filter/ add links after
    try:
        return a_tag["href"]
    except KeyError:
        return ""

def get_star_table(soup):
    soup_tables = soup.find_all("table", {"class": "sortable"})
    tables = pd.read_html(str(soup_tables))
    star_table = tables[0].rename(columns={"Unnamed: 1": "Gender"})
    blank_replace_map = {"Died": "Living", "At age": "Posthumously", "Oscar": ""}
    star_table = star_table.replace("~", blank_replace_map)
    star_table = star_table.replace("Nom", {"Oscar": "Nominated"})
    return star_table

def add_links_to_table(table, links, map_col):
    table["Link"] = table.loc[:, map_col].map(links)
    return table

if __name__ == "__main__":
    stars = scrape_walk_of_fame()
    stars.to_csv(config.STARS_OUTPUT, index=False)
    #after output, fill in empty links
