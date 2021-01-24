import requests
import re
import json
import time
import os

from bs4 import BeautifulSoup
from functools import reduce

base_url = "https://www.kijiji.ca"

def getResults(pageURL, pageNum=1):

    page = requests.get(base_url + pageURL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = []

    listings = soup.find_all("div", class_="search-item")

    for listing in listings:

        search = listing.find("a", class_="title")['href']

        if (bool(re.match(r'^.*(/student-housing/|/v-apartments-condos/|/v-room-rental-roommate/).*$', search))):

            try:
                postPage = requests.get(base_url + search)
                post = BeautifulSoup(postPage.content, "html.parser")

                title = post.find("h1", class_=re.compile('^title.*')).string
                price = post.find("span", class_=re.compile('^currentPrice.*')).span.string
                address = post.find("span", class_=re.compile('^address.*')).string
                date_posted = post.find("div", class_=re.compile('^datePosted.*')).find("time")["datetime"]
                images = [img["src"] for img in post.find("div", id="mainHeroImage").parent.find_all("img")] if post.find("div", id="mainHeroImage") else []
                description = reduce(lambda a, b: a + b.string, [''] + post.find("div", class_=re.compile('^descriptionContainer.*')).find_all("p"))

                results.append({
                    'title': title,
                    'price': price,
                    'address': address,
                    'date-posted': date_posted,
                    'images': images,
                    'description': description,
                    'url': base_url + search
                })

            except Exception as e:
                print(f'Currently on {search}')
                print(e)

        time.sleep(2)

    nextAnchor = soup.find("a", href=re.compile(f'^.*/page-{pageNum+4}/.*$'))

    if (not nextAnchor is None):
        results += getResults(nextAnchor["href"], page+1)

    return results

def execute():

    print("Starting Kijiji")

    search = "/b-kingston-on/student-housing/k0l1700183"
    results = getResults(search)

    with open('server/scrapers/output/kijiji-output.json', 'w') as file:
        file.write(json.dumps(results, sort_keys=True, indent=4))
        print(f'wrote {len(results)} to "output/kijiji-output.json"')
