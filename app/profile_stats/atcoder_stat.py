import time
import json
import requests
from bs4 import BeautifulSoup
import re

class AtCoderScrapper:

    def get_user_submission_count(self, username):
        url = 'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user='+str(username)+'&from_second=1560046356'
        req = requests.get(url).json()
        #print(req)
        ac_count = 0
        wa_count = 0
        tle_count = 0
        mle_count = 0
        rte_count = 0
        cpe_count = 0 
        others_count = 0
        for item in req:
            verdict = item['result']
            print(item['result'])
            if verdict == 'AC':
                ac_count = ac_count + 1
            elif verdict == 'WA':
                wa_count = wa_count + 1
            elif verdict == 'CE':
                cpe_count = cpe_count + 1
            elif verdict == 'RE':
                rte_count = rte_count + 1
            elif verdict == 'TLE':
                tle_count = tle_count + 1
            elif verdict == 'MLE':
                mle_count = mle_count + 1
            else:
                others_count = others_count + 1
        return {
            'platform': 'atcoder',
            'user_name': username,
            'solved_count': ac_count,
            'wrong_answer_count': wa_count,
            'time_limit_exceeded_count': tle_count,
            'memory_limit_exceeded_count': mle_count,
            'runtime_error_count': rte_count,
            'compilation_error_count': cpe_count,
            'other_verdict_count': others_count
        }

    def onlyRated(self, his):
        ratedHis = []
        pefdic = {}
        for i in range(len(his)):
            if i >= len(his):
                break
            #print(his[i])
            if his[i]["IsRated"]==True:
                ratedHis.append(his[i])
        return ratedHis

    def get_user_ratings(self, username):
        url = 'https://atcoder.jp/users/'+str(username)+'?graph=rating'
        req = requests.get(url)
        data = BeautifulSoup(req.text,"html.parser")
        #print(data)
        ret = data.find_all("script")
        his = requests.get('https://atcoder.jp/users/'+str(username)+'/history/json').json()
        tmp = json.loads(str(ret[12])[27:-10])

        for i in range(len(tmp)):
            tmp[i]["StandingsU"]=tmp[i]["StandingsUrl"]
            tmp[i]["StandingsUrl"]="https://atcoder.jp"+tmp[i]["StandingsUrl"]
            tmp[i]["low"]=0
            tmp[i]["high"]=10000
        return tmp,self.onlyRated(his)

if __name__ == '__main__':
    print('START RUNNING ATCODER SCRAPPER SCRIPT\n')
    atcoder_scrapper = AtCoderScrapper()
    # resp = spoj_scrapper.get_user_info('tarango_khan')
    #resp = atcoder_scrapper.get_user_submission_count('fsshakkhor')
    #print(resp)
    lol1,lol2 = atcoder_scrapper.get_user_ratings('Starscream')
    #print(lol1)
    #print(lol2)
    ratings = []
    for item in lol2:
        ratings.append(item['NewRating'])
    print(ratings)