import time
import json
import requests
from bs4 import BeautifulSoup
import re
import pytz
from datetime import datetime


class AtCoderUnsolvedProblems:

    def get_unsolved_problems(self, username):
        url = 'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=' + \
            str(username)+'&from_second=1560046356'
        req = requests.get(url).json()
        # print(req)
        unsolved_problems = []
        solved_problems = []
        for item in req:
            verdict = item['result']
            # print(item['result'])
            if verdict == 'AC':
                if item['problem_id'] not in solved_problems:
                    solved_problems.append(item['problem_id'])

        for item in req:
            verdict = item['result']
            # print(item['result'])
            if verdict != 'AC':
                if item['problem_id'] not in solved_problems:
                    unsolved_problems.append(item['problem_id'])
        # print(unsolved_problems)
        unsolved_problems_res1 = []
        for item2 in unsolved_problems:
            if item2 not in unsolved_problems_res1:
                unsolved_problems_res1.append(item2)
        print(unsolved_problems_res1)
        unsolved_problems_res = []
        req1 = requests.get(
            'https://kenkoooo.com/atcoder/resources/problems.json').json()
        for item in unsolved_problems_res1:
            for item1 in req1:
                if item == item1['id']:
                    problem_info = []
                    problem_link = 'https://atcoder.jp/contests/' + \
                        str(item1['contest_id']) + '/tasks/' + str(item1['id'])
                    problem_info.append(item1['id'])
                    problem_info.append(problem_link)
                    problem_info.append(item1['title'])
                    unsolved_problems_res.append(problem_info)

        return {
            'platform': 'atcoder',
            'user_name': username,
            'unsolved_problems': unsolved_problems_res
        }

    def get_submission_count_per_day(self, username):
        url = 'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=' + \
            str(username)+'&from_second=1560046356'
        req = requests.get(url).json()
        subcountmap = {}
        subcountmaplist = []
        tz = pytz.timezone('America/Los_Angeles')
        for item in req:
            unixTimestamp = item['epoch_second']
            submissionDate = datetime.fromtimestamp(
                unixTimestamp, tz).isoformat()
            submissionDate = submissionDate[0:10]
            if submissionDate in subcountmap:
                subcountmap[submissionDate] = subcountmap[submissionDate] + 1
            else:
                subcountmap[submissionDate] = 1

        subcountmaplist = list(subcountmap.items())
        return {
            'platform': 'atcoder',
            'user_name': username,
            'subcountmap': subcountmaplist
        }


if __name__ == '__main__':
    print('START RUNNING ATCODER SCRAPPER SCRIPT\n')
    atcoder_scrapper = AtCoderUnsolvedProblems()
    # resp = spoj_scrapper.get_user_info('tarango_khan')
    #resp = atcoder_scrapper.get_user_submission_count('fsshakkhor')
    # print(resp)
    lol2 = atcoder_scrapper.get_submission_count_per_day('fsshakkhor')
    print(lol2)
