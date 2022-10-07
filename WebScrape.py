import csv

import requests as req
from bs4 import BeautifulSoup as BSup


class WebScraper:

    def __init__(self):
        department = input("What department would you like faculty data for?\n")
        url = "https://www.shepherd.edu/"+department+"/staff"
        self.page = req.get(url)
        self.soup = BSup(self.page.content, "html.parser")
        self.scrape()


    def scrape(self):
        content = self.soup.find(class_="content")
        staffmembers = content.find_all("div", class_="staff-item")
        csv_data=[]
        headers = ["Name", "Title", "Email", "Phone", "Bio"]
        for item in staffmembers:
            memberinfo = ['None', 'None', 'None', 'None', 'None']
            lines = item.find_all('tr')
            name = item.find('h2').text
            memberinfo[0] = name
            csv_data.append(memberinfo)
        with open('FacultyInfo.csv', 'w', newline='') as fi:
            wr = csv.writer(fi)
            wr.writerow(headers)
            wr.writerows(csv_data)



if __name__ == '__main__':
    ws = WebScraper()