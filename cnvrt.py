import datetime

import requests
from constants import *
from bs4 import BeautifulSoup
import re
import pymongo

db = pymongo.MongoClient(CONNECTION_LINK)
db = db['apartments']['olx']

for i in db.find({}):
    # if price doesn't start with Schimb
    if not re.match(r'Schimb.*', i['price']):
        price = int(re.sub(r'\D', '', i['price']))
        db.update_one({'_id': i['_id']}, {'$set': {'price': price}})