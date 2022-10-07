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
            memberinfodict = {"Name":item.find('h2').text}
            lines = item.find_all('tr')
            for line in lines:
                th = line.find('th')
                td = line.find('td')
                if th is not None:
                    if td is not None:
                        if th.text == "Email":
                            text = td.text
                            text = text.strip()
                            text = text[0:text.index('@')+12]
                            memberinfodict[th.text] = text
                        else:
                            memberinfodict[th.text] = td.text.strip()
            memberinfo = ['None', 'None', 'None', 'None', 'None']
            memberinfo[0] = memberinfodict.get("Name", "None")
            memberinfo[1] = memberinfodict.get("Title", "None")
            memberinfo[2] = memberinfodict.get("Email", "None")
            memberinfo[3] = memberinfodict.get("Phone", "None")


            csv_data.append(memberinfo)
        with open('FacultyInfo.csv', 'w', newline='') as fi:
            wr = csv.writer(fi)
            wr.writerow(headers)
            wr.writerows(csv_data)



if __name__ == '__main__':
    ws = WebScraper()