import time
import json
import requests
from bs4 import BeautifulSoup
import re
import pytz
from datetime import datetime

_http_headers = {'Content-Type': 'application/json'}


class UvaUnsolvedProblems:

    def problem_id_name_map(self):
        try:
            rs = requests.session()
            url = f'https://uhunt.onlinejudge.org/api/p'
            data = rs.get(url=url, headers=_http_headers).json()
            map = {}
            for problem in data:
                map[problem[0]] = problem[1]
            return map
        except Exception as e:
            raise e

    def get_unsolved_problems(self, username):
        try:
            rs = requests.session()
            url = f'https://uhunt.onlinejudge.org/api/uname2uid/{username}'
            userid = rs.get(url=url, headers=_http_headers).json()

            profile_url = f'https://uhunt.onlinejudge.org/api/subs-user/{userid}'
            problem_map = self.problem_id_name_map()
            #print(problem_map)

            profile_data = rs.get(url=profile_url, headers=_http_headers).json()

            unsolved_problems = []
            solved_problems = []
            all_submissions = profile_data['subs']
            #print(profile_data)
            for sub in all_submissions:
                problem_id = problem_map[sub[1]]
                verdict = sub[2]
                #print(verdict)
                if verdict == 90:
                    #problem_info = []
                    #problem_link = 'https://onlinejudge.org/external/' + str(int(problem_id/100)) + '/' + str(problem_id) + '.pdf'
                    #problem_url = f'https://uhunt.onlinejudge.org/api/p/id/' + str(problem_id)
                    #problem_data = rs.get(url=problem_url, headers=_http_headers).json()
                    #problem_name = problem_data['title']
                    #print(problem_name)
                    #problem_info.append(problem_id)
                    #problem_info.append(problem_name)
                    #problem_info.append(problem_link)
                    if problem_id not in solved_problems:
                        #print(problem_info)
                        solved_problems.append(problem_id)            
            #print(solved_problems)

            for sub in all_submissions:
                problem_id = problem_map[sub[1]]
                verdict = sub[2]
                #print(verdict)
                if verdict != 90:
                    #problem_info = []
                    #problem_link = 'https://onlinejudge.org/external/' + str(int(problem_id/100)) + '/' + str(problem_id) + '.pdf'
                    #problem_url = f'https://uhunt.onlinejudge.org/api/p/id/' + str(problem_id)
                    #problem_data = rs.get(url=problem_url, headers=_http_headers).json()
                    #problem_name = problem_data['title']
                    #print(problem_name)
                    #problem_info.append(problem_id)
                    #problem_info.append(problem_name)
                    #problem_info.append(problem_link)
                    if problem_id not in solved_problems:
                        unsolved_problems.append(problem_id)
            
            unsolved_problems_res = []
            unsolved_problems_res1 = []
            for item in unsolved_problems:
                if item not in unsolved_problems_res:
                    unsolved_problems_res.append(item)
            #print(unsolved_problems_res)
            for item1 in unsolved_problems_res:
                problem_info = []
                problem_link = 'https://onlinejudge.org/external/' + str(int(item1/100)) + '/' + str(item1) + '.pdf'
                problem_url = f'https://uhunt.onlinejudge.org/api/p/num/' + str(item1)
                problem_data = rs.get(url=problem_url, headers=_http_headers).json()
                problem_name = problem_data['title']
                problem_info.append(item1)
                problem_info.append(problem_name)
                problem_info.append(problem_link)
                #print(problem_info)
                unsolved_problems_res1.append(problem_info)
                #print(unsolved_problems_res1)
                    

            return {
                'platform': 'uva',
                'user_name': username,
                'unsolved_problems': unsolved_problems_res1
            }
        except Exception as e:
            return {
                'platform': 'uva',
                'user_name': username,
                'unsolved_problems': []
            }
    def get_submission_count_per_day(self, username):
        try:
            rs = requests.session()
            url = f'https://uhunt.onlinejudge.org/api/uname2uid/{username}'
            userid = rs.get(url=url, headers=_http_headers).json()

            profile_url = f'https://uhunt.onlinejudge.org/api/subs-user/{userid}'
            problem_map = self.problem_id_name_map()
            #print(problem_map)

            profile_data = rs.get(url=profile_url, headers=_http_headers).json()
            #print(profile_data)
            subinfo = profile_data['subs']
            #print(subinfo)
            subcountmap = {}
            subcountmaplist = []

            tz = pytz.timezone('America/Los_Angeles')
            for item in subinfo:
                #print(item)
                unixTimestamp = item[4]
                #print(unixTimestamp)
                submissionDate = datetime.fromtimestamp(unixTimestamp, tz).isoformat()
                
                submissionDate = submissionDate[0:10]
                #print(submissionDate)
                if submissionDate in subcountmap:
                    subcountmap[submissionDate] = subcountmap[submissionDate] + 1
                else:
                    subcountmap[submissionDate] = 1

            subcountmaplist = list(subcountmap.items())
            return {
                'platform': 'uva',
                'user_name': username,
                'subcountmap': subcountmaplist
            }

        except Exception as e:
            return {
                'platform': 'uva',
                'user_name': username,
                'subcountmap': {}
            }

if __name__ == '__main__':
    print('START RUNNING UVA SCRAPPER SCRIPT\n')
    uva_scrapper = UvaUnsolvedProblems()
    resp = uva_scrapper.get_submission_count_per_day('fsshakkhor')
    print(json.dumps(resp))