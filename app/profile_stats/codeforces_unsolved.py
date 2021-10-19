import requests
from bs4 import BeautifulSoup as BS
import json
import re
import pytz
from datetime import datetime

_http_headers = {'Content-Type': 'application/json'}


class CFUnsolvedProblems:
    def get_codeforces_unsolved(self, username):
        try:
            rs = requests.session()
            url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=10000'
            submission_list = rs.get(url=url, headers=_http_headers).json()
            # print(submission_list['result'])
            submission_list = submission_list['result']
            unsolved_problems = []
            solved_problems = []
            for submission in submission_list:
                if submission['verdict'] == 'OK' and submission['testset'] == 'TESTS':
                    problem_info = []
                    problem = str(
                        submission['problem']['contestId']) + '/' + str(submission['problem']['index'])
                    problem_link = ''
                    if submission['problem']['contestId'] >= 100000:
                        problem_link = 'https://codeforces.com/gym/' + \
                            str(submission['problem']['contestId']) + \
                            '/problem/' + str(submission['problem']['index'])
                    else:
                        problem_link = 'https://codeforces.com/contest/' + \
                            str(submission['problem']['contestId']) + \
                            '/problem/' + str(submission['problem']['index'])
                    problem_title = str(submission['problem']['name'])
                    problem_tags = submission['problem']['tags']
                    problem_info.append(problem)
                    problem_info.append(problem_title)
                    problem_info.append(problem_link)
                    problem_info.append(problem_tags)
                    # print(problem_info)
                    if problem_info not in solved_problems:
                        solved_problems.append(problem_info)
            # print(solved_problems)
            for submission in submission_list:
                if submission['verdict'] != 'OK' and submission['testset'] == 'TESTS':
                    problem_info = []
                    problem = str(
                        submission['problem']['contestId']) + '/' + str(submission['problem']['index'])
                    problem_link = ''
                    if submission['problem']['contestId'] >= 100000:
                        problem_link = 'https://codeforces.com/gym/' + \
                            str(submission['problem']['contestId']) + \
                            '/problem/' + str(submission['problem']['index'])
                    else:
                        problem_link = 'https://codeforces.com/contest/' + \
                            str(submission['problem']['contestId']) + \
                            '/problem/' + str(submission['problem']['index'])
                    problem_title = str(submission['problem']['name'])
                    problem_tags = submission['problem']['tags']
                    problem_info.append(problem)
                    problem_info.append(problem_title)
                    problem_info.append(problem_link)
                    problem_info.append(problem_tags)
                    # print(problem_info)
                    # print(solved_problems)
                    if problem_info not in solved_problems:
                        unsolved_problems.append(problem_info)
            # print(unsolved_problems)
            #unsolved_problems_res = list(OrderedDict.fromkeys(unsolved_problems))
            unsolved_problems_res = []
            for item in unsolved_problems:
                if item not in unsolved_problems_res:
                    unsolved_problems_res.append(item)
            return {
                'platform': 'codeforces',
                'user_name': username,
                'unsolved_problems': unsolved_problems_res
            }
        except Exception as e:
            return {
                'platform': 'codeforces',
                'user_name': username,
                'unsolved_problems': []
            }

    def get_submission_count_per_day(self, username):
        try:
            rs = requests.session()
            url = f'http://codeforces.com/api/user.status?handle={username}&from=1&count=10000'
            submission_list = rs.get(url=url, headers=_http_headers).json()
            # print(submission_list)
            submission_list = submission_list['result']
            subcountmap = {}
            subcountmaplist = []
            tz = pytz.timezone('America/Los_Angeles')
            for item in submission_list:
                unixTimestamp = item['creationTimeSeconds']
                submissionDate = datetime.fromtimestamp(
                    unixTimestamp, tz).isoformat()
                submissionDate = submissionDate[0:10]
                if submissionDate in subcountmap:
                    subcountmap[submissionDate] = subcountmap[submissionDate] + 1
                else:
                    subcountmap[submissionDate] = 1

            subcountmaplist = list(subcountmap.items())
            return {
                'platform': 'codeforces',
                'user_name': username,
                'subcountmap': subcountmaplist
            }

        except Exception as e:
            return {
                'platform': 'codeforces',
                'user_name': username,
                'subcountmap': {}
            }


if __name__ == '__main__':
    print('START RUNNING CODEFORCES SCRAPPER SCRIPT\n')
    codeforces_scrapper = CFUnsolvedProblems()
    #resp = codeforces_scrapper.get_user_info_heavy('RiffleShuffle')
    resp = codeforces_scrapper.get_submission_count_per_day('shahed_ahmed')
    # resp = codeforces_scrapper.get_user_rating_history('Starscream-11813')
    # userratings=[]
    # for item in resp:
    #     userratings.append(item['newRating'])
    #     #print(item['newRating'])
    # print(resp)
    unsolved_problems_cf = []
    unsolved_problems_cf = resp

    print(unsolved_problems_cf)

    # unsolved_problems_id = []
    # for item in resp['unsolved_problems']:
    #     unsolved_problems_id.append(item[0])

    # print(unsolved_problems_id)

    # unsolved_problems_name =[]
    # for item in resp['unsolved_problems']:
    #     unsolved_problems_name.append(item[1])

    # print(unsolved_problems_name)

    # unsolved_problems_links = []
    # for item in resp['unsolved_problems']:
    #     unsolved_problems_links.append(item[2])

    # print(unsolved_problems_links)

    # unsolved_problems_tags = []
    # for item in resp['unsolved_problems']:
    #     unsolved_problems_tags.append(item[3])

    # print(unsolved_problems_tags)
    # print(userratings)
    # print(json.dumps(resp))
