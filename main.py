import datetime

import requests
from bs4 import BeautifulSoup
import re
import pymongo
from constants import *


db = pymongo.MongoClient(CONNECTION_LINK)
db = db['apartments']['olx']


def main():
    try:
        apt_list = get_all_apartments()
        already_scraped = 0
        for apt in apt_list:
            scrape_apt(f'{BASE_OLX_URL}{apt}', len(apt_list), already_scraped)
            already_scraped += 1

        return {
            'status': 'success',
            'apts scraped': len(apt_list),
        }

    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

def get_all_apartments():
    """Get all apartments from the site"""
    all_apartments = []
    for page in range(1, 10):
        r = requests.get(f'{OLX_URL}&page={page}')
        if page != 1 and r.url != f'{OLX_URL}&page={page}':
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        apartments = soup.find_all('a', class_='css-rc5s2u')
        apartments = [apt['href'] for apt in apartments if apt['href'] != '#' and not re.match(r'.*storia.*', apt['href'])]
        # go through all apartments and check if the md5 hash of the link is in the database already
        for apt in apartments:
            if db.find_one({'link': apt}) is not None:
                print(f'Already in database: {apt}')
                apartments.remove(apt)
        all_apartments.extend(apartments)
    return all_apartments


def get_month(param):
    months = {
        'ianuarie': 1,
        'februarie': 2,
        'martie': 3,
        'aprilie': 4,
        'mai': 5,
        'iunie': 6,
        'iulie': 7,
        'august': 8,
        'septembrie': 9,
        'octombrie': 10,
        'noiembrie': 11,
        'decembrie': 12
    }
    return months[param]


def scrape_apt(apt_url, total_number=0, already_scraped=0):
    # if the apartment is already in the database, skip it
    if db.find_one({'link': apt_url}) is not None:
        print(f'Already in database: {apt_url}')
        return
    """Scrape the apartment"""
    r = requests.get(apt_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    date_posted = soup.find('span', class_='css-19yf5ek').text
    # if date_posted starts with 'Azi la' remove 'Azi la' and add the current date
    if date_posted.startswith('Azi la'):
        date_posted = date_posted.replace('Azi la ', '')
        date_posted = f'{datetime.datetime.now().strftime("%d/%m/%Y")}'
    else:
        # date is in format '24 decembrie 2022' for example
        date_posted = date_posted.split(' ')
        date_posted = f'{date_posted[0]}/{get_month(date_posted[1])}/{date_posted[2]}'

    # get the price
    price = soup.find('h3', class_='css-19cr6mc-TextStyled er34gjf0').text
    # if price doesn't start with Schimb
    if not re.match(r'Schimb.*', price):
        price = price.split(' ')
        try:
            price = f'{price[0]},{price[1]}€'
        except IndexError:
            price = f'{price[0]}€'
        price = int(re.sub(r'\D', '', price))
    else:
        return

    # get the title
    title = soup.find('h1', class_='css-swd4zc-TextStyled er34gjf0').text

    # get attributes
    attributes = soup.find_all('li', class_='css-ox1ptj')
    attributes = [attr.text for attr in attributes if attr.text != 'Persoana fizica']

    attributes = [attr.split(':') for attr in attributes]
    try:
        attributes = {attr[0]: attr[1].strip() for attr in attributes}
    except IndexError:
        attributes = {attr[0]: '' for attr in attributes}


    # get raw_date
    raw_date = ''
    if attributes.get('An constructie'):
        i = attributes['An constructie']
        if 'Dupa' in i:
            raw_date = i.split(' ')
            raw_date = f'{raw_date[1]}'
            raw_date = f'01/01/{raw_date}'
        elif 'inainte de' in i:
            raw_date = i.split(' ')
            raw_date = f'{raw_date[2]}'
            raw_date = f'01/01/{raw_date}'
        elif '–' in i:
            # date is of format 1977 - 2000
            raw_date = i.split('–')
            raw_date = f'01/01/{raw_date[0].strip()}'
        else:
            raw_date = f'01/01/{i}'

        raw_date = datetime.datetime.strptime(raw_date, '%d/%m/%Y').timestamp()

    # get description
    description = soup.find('div', class_='css-12l22jb-TextStyled er34gjf0').text

    # get location from title
    lower_title = title.lower()
    lower_title = lower_title.replace('ș', 's').replace('ț', 't').replace('ă', 'a').replace('â', 'a').replace('î', 'i')
    location = ''
    for al in aliases:
        if al in lower_title:
            location = aliases[al]
            break

    for loc in IASI_LOCATIONS:
        if loc in lower_title:
            location = loc
            break

    # insert everything into a document
    document = {
        'title': title,
        'price': price,
        'location': location,
        'date_posted': date_posted,
        'description': description,
        'link': apt_url,
        'attributes': attributes,
        'raw_date': raw_date,
        'date_scraped': datetime.datetime.now().strftime("%d/%m/%Y")
    }

    db.insert_one(document)
    print(document)
    print(f'Inserted {apt_url} into database, left to scrape: {total_number - already_scraped}')


if __name__ == '__main__':
    main()


