import time
import json
import requests
from bs4 import BeautifulSoup
import re

_http_headers = {'Content-Type': 'application/json'}


class CodeforcesScrapper:

    rating_history_url = 'https://codeforces.com/api/user.rating?handle='

    def get_user_info(self, username):
        try:
            rs = requests.session()
            url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=1000000'
            submission_list = rs.get(url=url, headers=_http_headers).json()
            submission_list = submission_list['result']

            solved_problems = []

            for submission in submission_list:
                if submission['verdict'] == 'OK' and submission['testset'] == 'TESTS':
                    problem = str(submission['problem']['contestId']) + '/' + str(submission['problem']['index'])
                    if problem not in solved_problems:
                        solved_problems.append(problem)

            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': len(solved_problems),
                'solved_problems': solved_problems
            }
        except Exception as e:
            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': 0,
                'solved_problems': []
            }

    def get_user_info_heavy(self, username):
        try:
            rs = requests.session()
            url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=1000000'
            submission_list = rs.get(url=url, headers=_http_headers).json()
            submission_list = submission_list['result']
            solved_problems = {}

            for submission in submission_list:
                if 'verdict' not in submission or 'testset' not in submission:
                    continue
                if submission['verdict'] == 'OK' and submission['testset'] == 'TESTS':
                    problem = str(submission['problem']['contestId']) + '/' + str(submission['problem']['index'])
                    if problem not in solved_problems:
                        problem_data = {
                            'problem_id': problem,
                            'submission_list': []
                        }
                        solved_problems[problem] = problem_data

                    sublink = {
                        'submission_time': int(submission['creationTimeSeconds']),
                        'submission_link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}',
                        'submission_id': submission["id"]
                    }
                    solved_problems[problem]['submission_list'].append(sublink)
            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': len(solved_problems),
                'solved_problems': solved_problems
            }
        except Exception as e:
            print('Exception occurred: ', str(e))
            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': 0,
                'solved_problems': {}
            }

    def get_submission_stat(self, username):
        try:
            rs = requests.session()
            url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=1000'
            submission_list = rs.get(url=url, headers=_http_headers).json()
            submission_list = submission_list['result']

            solved_problems = []
            submission_stat = []

            for submission in submission_list:
                print(submission['verdict'])
                # if submission['verdict'] == 'OK' and submission['testset'] == 'TESTS':
                if submission['testset'] == 'TESTS':
                    problem = str(submission['problem']['contestId']) + '/' + str(submission['problem']['index'])
                    # if problem not in solved_problems:
                    solved_problems.append(problem)
                    submission_data = {
                        'problem_id': problem,
                        'submission_link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}',
                        'verdict': submission['verdict'],
                        'submission_date': submission['creationTimeSeconds'],
                    }
                    submission_stat.append(submission_data)
            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': len(solved_problems),
                'solved_problems': solved_problems,
                'submission_stat': submission_stat,
            }
        except Exception as e:
            return {
                'platform': 'codeforces',
                'user_name': username,
                'solved_count': 0,
                'solved_problems': [],
                'submission_stat': [],
            }

    def get_user_rating_history(self, username):
        try:
            rs = requests.session()
            url = self.rating_history_url + username
            rating_history = rs.get(url=url, headers=_http_headers).json()
            return rating_history['result']
        except Exception as e:
            return []

    def get_submission_stat_count(self, username):
            try:
                rs = requests.session()
                url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=1000000'
                submission_list = rs.get(url=url, headers=_http_headers).json()
                submission_list = submission_list['result']
                ac_count = 0
                wa_count = 0
                tle_count = 0
                mle_count = 0
                rte_count = 0
                cpe_count = 0
                others_count = 0
                for submission in submission_list:
                    # print(submission['verdict'])
                    if submission['verdict'] == 'OK' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        ac_count = ac_count + 1
                    elif submission['verdict'] == 'WRONG_ANSWER' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        wa_count = wa_count + 1
                    elif submission['verdict'] == 'TIME_LIMIT_EXCEEDED' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        tle_count = tle_count + 1
                    elif submission['verdict'] == 'MEMORY_LIMIT_EXCEEDED' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        mle_count = mle_count + 1
                    elif submission['verdict'] == 'RUNTIME_ERROR' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        rte_count = rte_count + 1
                    elif submission['verdict'] == 'COMPILATION_ERROR' and (submission['testset'] == 'TESTS' or submission['testset'] == 'PRETESTS'):
                        cpe_count = cpe_count + 1
                    else:
                        others_count = others_count + 1

                    
                return {
                    'platform': 'codeforces',
                    'user_name': username,
                    'solved_count': ac_count,
                    'wrong_answer_count': wa_count,
                    'time_limit_exceeded_count': tle_count,
                    'memory_limit_exceeded_count': mle_count,
                    'runtime_error_count': rte_count,
                    'compilation_error_count': cpe_count,
                    'other_verdict_count': others_count
                }
            except Exception as e:
                return {
                    'platform': 'codeforces',
                    'user_name': username,
                    'solved_count': 0,
                    'wrong_answer_count': 0,
                    'time_limit_exceeded_count': 0,
                    'memory_limit_exceeded_count': 0,
                    'runtime_error_count': 0,
                    'compilation_error_count': 0,
                    'other_verdict_count': 0
                }

if __name__ == '__main__':
    print('START RUNNING CODEFORCES SCRAPPER SCRIPT\n')
    codeforces_scrapper = CodeforcesScrapper()
    #resp = codeforces_scrapper.get_user_info_heavy('RiffleShuffle')
    #resp = codeforces_scrapper.get_submission_stat('RiffleShuffle')
    # resp = codeforces_scrapper.get_user_rating_history('Starscream-11813')
    resp = codeforces_scrapper.get_user_rating_history('shahed_ahmed')
    # resp2 = codeforces_scrapper.get_user_info_heavy('RiffleShuffle')
    userratings=[]
    for item in resp:
        userratings.append(item['newRating'])
        #print(item['newRating'])
    # print(resp)
    print(userratings)

    solved_count = []

    resp2 = codeforces_scrapper.get_submission_stat('RiffleShuffle')

    resp3 = codeforces_scrapper.get_submission_stat_count('RiffleShuffle')
    solved_count=0
    for item in resp2['solved_problems']:
        solved_count = solved_count + 1
    print(solved_count)
    print(resp2)
    print(resp3)

   

    print(resp3['solved_count'])
    




    # solved_count = resp2['solved_count']
    


    # print(solved_count)
    #print(json.dumps(resp))

    #chartist.js
    #chart.js

