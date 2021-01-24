import requests
import json
import re
import datetime

from bs4 import BeautifulSoup

base_url = 'https://mackinnondev.ca'
output = 'mckinnon-output.json'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def getResults(search, pageNum=0):

    page = requests.get("https://mackinnondev.ca/available-rentals/", headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    results = []

    for link in soup.find("ul", class_="rentals").find_all("a"):

        postUrl = link["href"]
        pageReq = requests.get(postUrl, headers=headers)
        pageSoup = BeautifulSoup(pageReq.content, "html.parser")

        address = ' '.join(list(pageSoup.find("div", id="postTitle").strings)).replace('\n', '').strip()
        price = ''.join(list(pageSoup.find("ul", id="metaPrice").strings)[1:3]).strip()
        bedrooms = pageSoup.find("li", class_="propertyBed").string
        bathrooms = pageSoup.find("li", class_="propertyBath").string
        images = list(set([img["src"] for img in pageSoup.find("ul", class_="propertyImagesPager").find_all("img")]))

        description = ''
        for para in pageSoup.find("div", id="propertyContent").strings:

            if (not (para in description)):
                description += para

        results.append({
            'url': postUrl,
            'address': address,
            'title': address,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'date-posted': str(datetime.datetime),
            'images': images,
            'landlord': 'Mckinnon Dev',
            'description': description
        })

    return results

def execute():

    print("Starting Mckinnon")

    search = '/available-rentals/'
    results = getResults(search)

    with open(f'server/scrapers/output/{output}', 'w') as file:
        file.write(json.dumps(results, sort_keys=True, indent=4))
        print(f'Wrote {len(results)} to "output/{output}')
