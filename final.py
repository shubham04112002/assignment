import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
# Connecting mongo to our python program using inbuilt python driver
client=MongoClient()
client=MongoClient("mongodb://localhost:27017/")
scrapedatabase=client["scrape"]
mycollection = scrapedatabase.homepages
mycollection = scrapedatabase.thesubpages
pages={}
subpages={}

# make a request to the site and get it as a string
articleimages=[]
articlelinks=[]
def thesubpages(url):
    page=requests.get(url).text
    soup=BeautifulSoup(page,'html.parser')
    mainpageimages=[]
    links=[]
    for element in soup.find_all(class_="article-img"):
        images=element.findChildren('img',recursive=False)
        for image in images:
            mainpageimages.append('https:'+image['data-src'])

    for link in soup.find_all("a"):
        links.append(link.get('href'))

    
    articleimages.append(mainpageimages)
    articlelinks.append(links)



def homepage(url):
    page = requests.get(url).text

    # Pass the string to a BeautifulSoup object
    soup = BeautifulSoup(page,'html.parser')

    # titles will be stored here
    titles=[]
    images=[]
    links=[]
    for element in soup.find_all(class_="main-title"):
        children=element.findChildren("a",recursive=False)
        for child in children:
            thesubpages(child.get('href'))

            titles.append(child.get_text())


    for item in soup.find_all(class_="thumb-img"):
        children=item.findChildren('img',recursive=False)
        for child in children:
            images.append('https:'+child['data-src'])

    for link in soup.find_all('a'):
        links.append(link.get('href'))
        
    pages["titles"]=titles
    pages["images"]=images
    pages["links"]=links
    scrapedatabase.homepages.insert_one(pages)
    # print(pages)
homepage("https://www.firstpost.com/category/india")
subpages["subpagelinks"] = articlelinks
subpages["subpageimages"] = articleimages
scrapedatabase.thesubpages.insert_one(subpages)
print("done")
