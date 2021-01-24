from server.models import db, User, House
from server.scrapers import scrapers

import json
import os

"""
This file defines all backend logic that interacts with database and other services
"""

output_path = 'server/scrapers/output/'

def get_available_tickets(user):

    return House.query.all()

#Commit House to db
def save_houses(file):

    print("Loading " + file)
    # Read json file
    with open(output_path + file, 'r') as jsonLike:

        for entry in json.load(jsonLike):

            name = entry['title'] or None
            price = entry['price'] or None
            address = entry['address'] or None
            #bedrooms = data['bedrooms'] or None
            #bathrooms = data['bathrooms'] or None
            description = entry['description'] or None
            url = entry['url'] or None
            #landlord = data['landlord'] or None
            date = entry['date-posted'] or None
            imgs = entry['images'] or None
            img_urls = ','.join(imgs) if imgs else ''
            #update db with new ticket info
            house = House(name = name, price = price, address = address, description = description, url = url, date = date, img_urls = img_urls)
            db.session.add(house)
            db.session.commit()
            
def clean_database():
    db.session.query(House).delete()
    db.session.commit()

def startScrape(toDo=None):

    if toDo is None:

        for func in scrapers:

            #scrapers[func]()
            pass

        clean_database()
        loadJSON()

    else:

        for func in toDo:

            scraper[func]()

    return 'scrape started'

def loadJSON():

    toLoad = [file for file in os.listdir(output_path) if os.path.isfile(os.path.join(output_path+file))]
    for file in toLoad:
        save_houses(file)