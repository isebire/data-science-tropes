# this code extracts all the western animation listed in the animated films
# index on tv tropes, to be filtered out of dataset

import requests
import re
from bs4 import BeautifulSoup
import pickle
import pandas
import time

url = 'https://tvtropes.org/pmwiki/pmwiki.php/Main/AnimatedFilms'
r = requests.get(url).content
soup = BeautifulSoup(r, features="lxml")
div = soup.find("div", {"id": "main-article"})

film_locators = []
for link in div.findAll('a'):
    link_suffix = link.get('href')
    film_locator = link_suffix.split('/')[-1]
    print(film_locator)
    film_locators.append(film_locator)

print(len(film_locators))

with open('western_animated_film_locators.pkl', 'wb') as f:
    pickle.dump(film_locators, f)
