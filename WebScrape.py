import csv

import requests as req
from bs4 import BeautifulSoup as BSup


class WebScraper:

    def __init__(self, department=None):
        try:
            if department is None:
                self.userin()
                self.scrape()
            else:
                self.buildscraper(department)
                self.scrape()
        except req.exceptions.RequestException as e:
            print("an error occurred while getting webpage: " + str(e))

    def buildscraper(self, department):
        self.url = "https://www.shepherd.edu/" + department + "/staff"
        self.csvname = department + "DeptInfo.csv"
        self.page = req.get(self.url)
        self.soup = BSup(self.page.content, "html.parser")

    def userin(self):
        h = True
        while h is True:
            intext = input("type Scrape to scrape a new department, or Exit to close:\n")
            if (intext == "Scrape"):
                department = input("What department would you like faculty data for?\n")
                self.buildscraper(department)
                self.scrape()
            elif(intext == "Exit"):
                h = False

    def checkvalidity(self):
        if (self.page.url == self.url):
            return True
        else:
            print("Department Not Found")
            return False

    def dicttolist(self, dict, list):
        list[0] = dict.get("Name", "None Listed")
        list[1] = dict.get("Title", "None Listed")
        list[2] = dict.get("Email", "None Listed")
        list[3] = dict.get("Phone", "None Listed")
        list[4] = dict.get("Office", "None Listed")
        list[5] = dict.get("Bio", "None, Listed")
        list[6] = dict.get("Contact For", "None Listed")
        return list

    def writecsv(self, headers, data):
        with open(self.csvname, 'w', newline='') as fi:
            wr = csv.writer(fi)
            wr.writerow(headers)
            wr.writerows(data)

    def scrape(self):
        if self.checkvalidity():
            content = self.soup.find(class_="content")
            staffmembers = content.find_all("div", class_="staff-item")
            csv_data = []
            headers = ["Name", "Title", "Email", "Phone", "Office", "Bio", "Contact For"]
            for item in staffmembers:
                memberinfodict = {"Name": item.find('h2').text}
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
                    elif th is None:
                        if td is not None:
                            memberinfodict["Bio"] = td.text.strip()

                memberinfo = ['None', 'None', 'None', 'None', 'None', "None", "None"]
                csv_data.append(self.dicttolist(memberinfodict, memberinfo))
            self.writecsv(headers, csv_data)

if __name__ == '__main__':
    ws = WebScraper()
