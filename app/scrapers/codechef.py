import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timedelta

class CodeChef:

    contests = {}
    url = ""

    def __init__(self):

        #self.url = 'https://www.codechef.com/contests'
        #self.url = 'https://www.stopstalk.com/contests'
        self.url = 'https://clist.by:443/api/v1/contest/?end__gt='
        

        self.contests = {
            "Code":[],
            "Name":[],
            "Start":[],
            "End":[]
        }
        self.contestData=[]
    

    def __scrape(self):
        stTime = datetime.today() - timedelta(hours=6, minutes=0)
        enTime = datetime.today() - timedelta(hours=6, minutes=0) + timedelta(hours=480, minutes=0)

        begin = str(stTime.year) + "-" + str(stTime.month) + "-" + str(stTime.day) + "T" + str(stTime.hour) + "%3A" + str(stTime.minute) + "%3A" + str(stTime.second)
        endd = str(enTime.year) + "-" + str(enTime.month) + "-" + str(enTime.day) + "T" + str(enTime.hour) + "%3A" + str(enTime.minute) + "%3A" + str(enTime.second)
        # print(begin)
        # print(endd)
        url3 = "https://clist.by:443/api/v1/contest/?end__gt=" + begin + "&" + "end__lt=" + endd

        # print(url3)
        # print(url)
        res = requests.get(url3,headers={'Authorization': 'ApiKey Ahb_arif:e746f33d1dca698bf9e578774d86dafb916fe288'})
        # print(res.text)
        jsonData = res.json()
        objects = jsonData["objects"]
        #contestData = []
        for x in objects:

            siteName = x["resource"]["name"]
            contestName = x["event"]
            startTime = str(x["start"])
            startTime.replace("T", " , ")
            endTime = str(x["end"])
            endTime.replace("T", " , ")
            sortKey = str(x["end"])
            sortKey =  sortKey.replace("T", " ")
            link = x["href"]
            duration = int(float(x["duration"]) * 0.000277778)

            if duration >=24:
                d = int(duration/24)
                h = duration % 24
                duration = str(d) + " days "
                if h >0:
                    duration+= str(h) + " hours "

            else:
                duration = str(duration) + " hours"

            if siteName == "kaggle.com" or siteName == "toph.co" or siteName == "codingcompetitions.withgoogle.com" or siteName == "codeforces.com" or siteName == "csacademy.com" or siteName == "hackerrank.com" or siteName=="codechef.com" or siteName=="spoj.com" or siteName=="hackerearth.com" or siteName=="lightoj.com" or siteName=="atcoder.jp" or siteName=="projecteuler.net" or siteName=="e-olymp.com":
                temp = {}
                temp["sitename"] = siteName
                temp["contest_name"] = contestName
                temp["startTime"] = startTime.replace("T",", ") +" (GMT)"
                temp["endTime"] = endTime.replace("T",", ") +" (GMT)"
                temp["sortKey"] = sortKey
                temp["link"] = link
                temp["duration"] = duration

                # print(temp)
                self.contestData.append(temp)

        self.contestData = sorted(self.contestData, key=lambda k: datetime.strptime(str(k["sortKey"]), "%Y-%m-%d %H:%M:%S"),
                               reverse=False)
        #print(self.contestData)

        # page = requests.get(self.url)

        # soup = BeautifulSoup(page.content,'html.parser')#page.text(?)
        #print(soup)
        # quotes1=[]
        # tables = soup.find_all('table',{'class': 'dataTable'})
        #imgs = soup.find_all('img',{'title': 'CodeChef'})
        #print(tables)
        # contests1 = tables[1].findAll('td')
        #rows = tables[2].findAll('tr')
        #print(tables[1].find("tbody").find_all("tr"))

        # activeContests = tables[0]
        # upcomingContests = tables[1]
        # ignoredContests = ['INOIPRAC', 'ZCOPRAC', 'IARCSJUD']

        # requiredContests = []
        # requiredContests.extend(activeContests.find("tbody").find_all("tr"))
        # requiredContests.extend(upcomingContests.find("tbody").find_all("tr"))
        # i=0
        # quote1={}
        # for row in contests1:
        #     if(i%4 == 1):
        #         quote1['name'] = row.text.strip().replace('#', "")
        #     if(i%4 == 2):
        #         quote1['start'] = row.text.strip().replace('#', "")
        #     if(i%4 == 3):
        #         quote1['end'] = row.text.strip().replace('#', "")
        #     if(i%4 == 3):
        #         quotes1.append(quote1)
        #         quote1 = {} 
        #     i += 1
        # print(str(quotes1))
        # for i in range(1,len(rows)):
        #     td = rows[i].findAll('td')
        #     self.contests["Code"].append(td[0].text)
        #     self.contests["Name"].append(td[1].text.replace("\n",""))
        #     self.contests["Start"].append(td[2].text)
        #     self.contests["End"].append(td[3].text)

        #return contest_list
        #events = []
        # for contest in requiredContests:
        #     tds = contest.find_all("td")
        #     currentContest = {
        #         'contestCode': tds[0].text,
        #         'contestLink': 'https://www.codechef.com{0}'.format(tds[1].next.next.attrs['href'].split('?')[0]),
        #         'contestTitle': tds[1].text.split('\n')[1],
        #         'contestStartDate': tds[2].attrs['data-starttime'],
        #         'contestEndDate': tds[3].attrs['data-endtime']
        #     }

        #     if currentContest['contestCode'] in ignoredContests:
        #         continue

        #     if int(currentContest['contestEndDate'][:4]) - int(currentContest['contestStartDate'][:4]) > 0:
        #         continue
        
        #     self.contests.append(currentContest)
        #     print(self.contests)
    
    def getFutureContests(self):

        self.__scrape()
        #return self.contests
        return self.contestData

if __name__ == "__main__":
    cc = CodeChef()
    print(cc.getFutureContests())