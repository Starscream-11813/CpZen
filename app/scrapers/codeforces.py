import requests
import urllib3
from bs4 import BeautifulSoup

class CodeForces:

    contests = {}
    url = ""

    def __init__(self):

        self.url = 'https://codeforces.com/contests'

        self.contests = {
            "Name":[],
            "Start":[],
            "Length":[]
        }
    
    def __scrape(self):

        page = requests.get(self.url)

        soup = BeautifulSoup(page.content,'html.parser')

        tables = soup.find_all('table')
        #print(tables)

        rows = tables[0].findAll('tr')

        for i in range(1,len(rows)):
            td = rows[i].findAll('td')
            self.contests["Name"].append(td[0].text.replace("\n","").replace("\r","").strip())
            self.contests["Start"].append(td[2].text.replace("\n","").replace("\r","").strip())
            self.contests["Length"].append(td[3].text.replace("\n","").replace("\r","").strip())

    
    def getFutureContests(self):

        self.__scrape()
        #print(self.contests)
        return self.contests

if __name__ == "__main__":
    cc = CodeForces()
    print(cc.getFutureContests())