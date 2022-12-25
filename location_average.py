import datetime

import requests
from constants import *
from bs4 import BeautifulSoup
import re
import pymongo

db = pymongo.MongoClient(CONNECTION_LINK)
db = db['apartments']['olx']


prices_avg = {}
nr_of_apts = {}
for apt in db.find({}):
    if not apt['location'] or not apt['price'] or apt['price'] == 'Schimb':
        continue

    nr_of_apts[apt['location']] = nr_of_apts.get(apt['location'], 0) + 1
    if apt['location'] not in prices_avg:
        prices_avg[str(apt['location'])] = int(apt['price'])
    else:
        prices_avg[apt['location']] = int(prices_avg[str(apt['location'])] + int(apt['price'])) / 2

prices_avg = {k: v for k, v in sorted(prices_avg.items(), key=lambda item: item[1], reverse=True)}

for k, v in prices_avg.items():
    print(f'{k}: {v} ({nr_of_apts[k]} apts)')







