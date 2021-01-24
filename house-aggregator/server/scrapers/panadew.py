import requests
import json
import re
import os

from bs4 import BeautifulSoup

base_url = 'https://www.panadew.ca/property_type/student-rentals#headeranchor'
output = 'panadew_properties-output.json'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
def getResults(search, pageNum=0):

    page = requests.get(base_url + search)
    soup = BeautifulSoup(page.content, "html.parser")
    results = []
    
    #for post in soup.find("div", class="listingsResults").find_all("li", type="1"):
    #for post in soup.find("div", id="content").findAll("div",class_="listingblock"):
    for link in soup.find("div", class_="listingblocksection").find_all("a"):
        # Url
        postUrl = link["href"]
        print(postUrl)
        pageReq = requests.get(postUrl)
        break
        pageSoup = BeautifulSoup(pageReq.content, "html.parser")
        # Scrape Address
        address = pageSoup.find("h2", id="title").find_next(string=True)
       
        # Name
        name = address
       
        # Scrape price
        price = pageSoup.find("span", class_="featuresprice").find_next(string=True).strip()

        # Date 
        date = pageSoup.find("ul", class_="specslist").find_all("li")[4].string.replace("Date Available:", "").strip()

        # Scrape Bedrooms
        bedrooms = int(pageSoup.find("ul", class_="specslist").find_all("li")[2].string.replace("Bedroom:", ""))
        # Scrape Bedrooms
        bathrooms = int(pageSoup.find("ul", class_="specslist").find_all("li")[3].string.replace("Bathroom:", ""))

        # Description
        description = pageSoup.find("div", id="listingcontent").find_all("p")[0].find_next(string=True)
        # img_urls
        img_url = pageSoup.find("img", itemprop="image")["src"]
        
        results.append({
            'title': name,
            'address': address,
            'price': price,
            'date': date,
            'bathrooms': bathrooms,
            'bedrooms': bedrooms,
            'description': description,
            'img_url': img_url,
            'landlords': "Panadew Properties"
        })

    return results

def execute():

    print("Starting Panadew")

    search = '/available-rentals/'
    results = getResults(search)

    with open(f'output/{output}', 'w') as file:
        file.write(json.dumps(results, sort_keys=True, indent=4))
        print(f'Wrote {len(results)} to "output/{output}"')

if __name__ == "__main__":
    execute()