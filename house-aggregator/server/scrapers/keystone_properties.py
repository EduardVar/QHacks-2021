import requests
import json
import re

from bs4 import BeautifulSoup

base_url = 'http://www.keyprop.com/listings/'
output = 'keystone_properties-output.json'

def getResults(search, pageNum=0):

    page = requests.get(base_url + search)
    soup = BeautifulSoup(page.content, "html.parser")
    results = []

    for post in soup.find("ul", id="listingsResults").find_all("li", type="1"):

        postLink = post.select_one("a", href=re.compile('$listing.html\?id=[0-9]+$'))["href"]
        
        postSoup = requests.get(base_url + postLink)

        title = post.find("div", class_="listInformation").find('h2').find_next(string=True)
        address = ' '.join(list(filter(lambda x: isinstance(x, str), post.find("div", class_="listAddress").find('p').contents)))
        price = post.find("div", class_="listAvailability").find("span").string
        bedrooms = postSoup.find("div", class_="specsCol").find
        print(bedrooms)

        utilites = {
            'heat': bool(post.find("img", alt="Heat")),
            'electric': bool(post.find("img", alt="Utilities")),
            'A/C': bool(post.find("img", alt="ac"))
        }

        results.append({
            'title': title,
            'address': address,
            'price': price,
            'utilites': utilites,
            'bedrooms': bedrooms,
            'landlords': "Keystone Properties"
        })

        break

    return results

search = ''
results = getResults(search)

print(results)

with open(f'output/{output}', 'w') as file:
    file.write(json.dumps(results, sort_keys=True, indent=4))
    print(f'Wrote {len(results)} to "output/{output}')
