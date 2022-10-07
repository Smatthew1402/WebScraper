import requests as req
from bs4 import BeautifulSoup as BSup


class WebScraper:

    def __init__(self):
        department = input("What department would you like faculty data for?\n")
        url = "https://www.shepherd.edu/"+department+"/staff"
        self.page = req.get(url)
        self.soup = BSup(self.page.content, "html.parser")

    def scrape(self):
        pass

if __name__ == '__main__':
    ws = WebScraper()