import requests
import re
import json
import time

from bs4 import BeautifulSoup
from functools import reduce


base_url = "https://www.kijiji.ca"
search = "/b-kingston-on/student-housing/k0l1700183"

page = requests.get(base_url + search)
soup = BeautifulSoup(page.content, "html.parser")

listings = soup.find_all("div", class_="search-item")

results = []

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
                'date_posted': date_posted,
                'images': images,
                'description': description,
                'url': base_url + search
            })

        except Exception as e:
            print(f'Currently on {search}')
            print(e)

    time.sleep(2)

with open('/output/kijiji-output.json', 'w') as file:
    file.write(json.dumps(results, sort_keys=True, indent=4))
