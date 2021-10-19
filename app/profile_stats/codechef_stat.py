import requests
from bs4 import BeautifulSoup as BS
import json

class CodeChefScrapper:
    # def getWebpage(url):
    #     return requests.get(url).content
    def getRatingHistory(self, handle):
        temp = "https://www.codechef.com/users/{}".format(handle)
        r = requests.get(temp).content
        r = str(r)
        idx = r.find("date_versus_rating")
        new_r = r[idx-1:]
        idx = new_r.find("}]")
        new_r = new_r[:-(len(new_r)-idx)-1]
        new_r = "{" + new_r + "\"}]}}"
        new_r.replace("null","\"null\"")
        new_r = new_r.replace("\\",'')
        new_r = new_r.replace("\'",'')
        data = json.loads(new_r)
        return data

    
    
if __name__ == '__main__':
    codechef_scrapper = CodeChefScrapper()
    var = codechef_scrapper.getRatingHistory('fsshakkhor')
    ratings = []
    for item in var['date_versus_rating']['all']:
        #print(item['rating'])
        ratings.append(item['rating'])
    print(ratings)