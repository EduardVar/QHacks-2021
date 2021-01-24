from server.models import db, User, House
import json
import os

"""
This file defines all backend logic that interacts with database and other services
"""

def get_available_tickets(user):

    return House.query.all()

#Commit House to db
def save_houses():
    # Read json file
    with open(os.getcwd() + '/server/output.json', 'r') as f:
        for entry in json.load(f):
            data = entry
            name = data['title'] or None
            price = data['price'] or None
            address = data['address'] or None
            #bedrooms = data['bedrooms'] or None
            #bathrooms = data['bathrooms'] or None
            description = data['description'] or None
            url = data['url'] or None
            #landlord = data['landlord'] or None
            date = data['date-available'] or None
            imgs = data['images'] or None
            img_urls = ','.join(imgs)
            #update db with new ticket info
            house = House(name = name, price = price, address = address, description = description, url = url, date = date, img_urls = img_urls)
            db.session.add(house)
            db.session.commit()
            

def clean_database():
    db.session.query(House).delete()
    db.session.commit()



def startScrape(toDo=None):

    if toDo is None:

        pass
        # do all

    else:

        for scraper in toDo:

            pass
            #do that specific one