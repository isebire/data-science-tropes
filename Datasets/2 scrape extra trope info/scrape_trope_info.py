# getting the descriptions AND the alternative titles of a trope

import requests
import re
from bs4 import BeautifulSoup
import pickle
import pandas
import time


def check_trope_exists(soup):
    div = soup.find("div", {"id": "main-article"})
    content = str(div)
    if content.find("We don't have an article named") != -1 or content.find("This page was cut") != -1:
        return False
    else:
        return True


def get_description(soup):
    div = soup.find("div", {"id": "main-article"})
    if div.find("div", {"class": "acaptionright"}):
        div.find("div", {"class": "acaptionright"}).decompose()
    content = str(div)
    content = content.split("<h2>", 1)[0]
    content = content.split("<h1>", 1)[0]
    content = content.replace("<sup>note", ".")
    content = BeautifulSoup(content, "lxml").text
    content = content.replace("Advertisement:", "")
    content = content.replace('\n', '')
    return content


def get_alt_titles(soup):
    div = soup.find("div", {"class": "alt-titles section section-fact"})
    alt_titles = str(div)
    alt_titles.strip()
    alt_titles = alt_titles.split('<span>')[1:]
    for i in range(len(alt_titles)):
        alt_titles[i] = alt_titles[i].split('</span>')[0].replace(' ', '').lower()
    return alt_titles


def get_description_laconic(trope):
    # url = 'https://tvtropes.org/pmwiki/pmwiki.php/Laconic/MegaNeko'
    url = 'https://tvtropes.org/pmwiki/pmwiki.php/Laconic/' + trope
    r = requests.get(url).content
    soup = BeautifulSoup(r, features="lxml")
    div = soup.find("div", {"id": "main-article"})
    content = str(div)
    if content.find("We don't have an article named") == -1:
        content = content.split("</p>", 1)[0]
        content = BeautifulSoup(content, "lxml").text
        content = content.replace('\n', '')
    else:
        # for some tropes no laconic page exists
        content = '/'
    return content


def get_related(trope):
    # url = 'https://tvtropes.org/pmwiki/relatedsearch.php?term=Main/MegaNeko'
    url = 'https://tvtropes.org/pmwiki/relatedsearch.php?term=Main/' + trope
    r = requests.get(url).content
    soup = BeautifulSoup(r, features="lxml")
    div = soup.find("div", {"id": "main-article"})
    content = str(div)
    content = content.split('people to the wiki from non-search engine links.')[1]
    content = content.split('</ul>')[1]
    content = content.split('<li>')[1:]
    for i in range(len(content)):
        content[i] = BeautifulSoup(content[i], "lxml").text.replace(' ', '').lower().strip('\n')
    return content


for i in range(74):

    filename = 'trope_name_chunk_' + str(i) + '.pkl'

    print('Reading: ' + filename)

    with open(filename, 'rb') as f:
        trope_names = pickle.load(f)

    # build a dict for desc. and alt_titles
    descriptions = {}
    alt_titles = {}
    descriptions_short = {}
    related_tropes = {}
    non_tropes = []

    for trope in trope_names:

        print('Downloading: ' + trope)

        # ping the webpage
        url = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/' + trope
        # url = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/meganeko'
        r = requests.get(url).content
        soup = BeautifulSoup(r, features="lxml")

        if check_trope_exists(soup):

            # get the list of alt titles in lowercase format
            alt_titles_current = get_alt_titles(soup)

            if trope not in alt_titles_current:
                if len(alt_titles_current) > 0:
                    alt_titles[trope] = alt_titles_current
                    print(alt_titles[trope])
                descriptions[trope] = get_description(soup)
                time.sleep(0.5)
                descriptions_short[trope] = get_description_laconic(trope)
                time.sleep(0.5)
                related_tropes[trope] = get_related(trope)

            else:
                print('This is an alternative name')

        else:
            print('No entry exists for this trope.')
            non_tropes.append(trope)

        time.sleep(0.5)

    print('Saving the data')

    filename = 'alt_trope_titles_dict_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(alt_titles, f)

    filename = 'trope_descriptions_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(descriptions, f)

    filename = 'trope_descriptions_laconic_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(descriptions_short, f)

    filename = 'related_tropes_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(related_tropes, f)

    filename = 'non_tropes_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(non_tropes, f)

    print(descriptions_short)
    print(alt_titles)
