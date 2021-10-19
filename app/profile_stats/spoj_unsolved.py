import time
import json
import requests
from bs4 import BeautifulSoup
import re
import pytz
from datetime import datetime
_http_headers = {'Content-Type': 'application/json'}


class SPOJUnsolvedProblems:
    def get_unsolved_problems(self, username):
        rs = requests.session()
        start = 0
        solved_problems = []
        unsolved_problems = []
        temp = []
        temp2 = []
        while start < 10000:
            url = f'https://www.spoj.com/status/{username}/all/start={start}'
            submission_page = rs.get(url=url, headers=_http_headers)
            soup = BeautifulSoup(submission_page.text, 'html.parser')
            table = soup.find("table", {"class": "newstatus"})
            temp2 = temp
            temp = []
            #v = []
            for row in table.find_all("tr")[1:]:  # skipping header row
                cells = row.find_all("td")
                submission_id = re.sub('\s+', '', str(cells[0].text))
                # submission_date = re.sub('\s+', '', str(cells[1].text))
                problem_id = re.sub(
                    '\s+', '', str(cells[2].find('a').get('title')))
                problem_name = re.sub('\s+', ' ', str(cells[2].find('a').text))
                problem_link = 'https://www.spoj.com/problems/' + \
                    str(problem_id) + '/'
                # print(problem_id)
                # print(problem_name)
                verdict = re.sub('\s+', '', str(cells[3].text))
                temp.append(submission_id)
                # v.append(verdict)
                # print(verdict)
                if verdict == 'accepted':
                    problem_info = []
                    problem_info.append(problem_id)
                    problem_info.append(problem_name)
                    problem_info.append(problem_link)
                    if problem_info not in solved_problems:
                        # print(problem_info)
                        solved_problems.append(problem_info)
            for row in table.find_all("tr")[1:]:  # skipping header row
                cells = row.find_all("td")
                submission_id = re.sub('\s+', '', str(cells[0].text))
                # submission_date = re.sub('\s+', '', str(cells[1].text))
                problem_id = re.sub(
                    '\s+', '', str(cells[2].find('a').get('title')))
                problem_name = re.sub('\s+', ' ', str(cells[2].find('a').text))
                problem_link = 'https://www.spoj.com/problems/' + \
                    str(problem_id) + '/'
                # print(problem_id)
                # print(problem_name)
                verdict = re.sub('\s+', '', str(cells[3].text))
                temp.append(submission_id)
                # v.append(verdict)
                # print(verdict)
                if verdict != 'accepted':
                    problem_info = []
                    problem_info.append(problem_id)
                    problem_info.append(problem_name)
                    problem_info.append(problem_link)
                    if problem_info not in solved_problems:
                        unsolved_problems.append(problem_info)
            if temp == temp2:
                break
            start += 20
        unsolved_problems_res = []
        for item in unsolved_problems:
            if item not in unsolved_problems_res:
                unsolved_problems_res.append(item)

        return {
            'platform': 'spoj',
            'user_name': username,
            'unsolved_problems': unsolved_problems_res
        }

    def get_submission_count_per_day(self, username):
        rs = requests.session()
        start = 0
        subcountmap = {}
        subcountmaplist = []
        temp = []
        temp2 = []
        while start < 10000:
            url = f'https://www.spoj.com/status/{username}/all/start={start}'
            submission_page = rs.get(url=url, headers=_http_headers)
            soup = BeautifulSoup(submission_page.text, 'html.parser')
            table = soup.find("table", {"class": "newstatus"})
            temp2 = temp
            temp = []
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                submission_id = re.sub('\s+', '', str(cells[0].text))
                submissionDate = re.sub('\s+', '', str(cells[1].text))
                submissionDate = submissionDate[0:10]
                print(submissionDate)
                if submissionDate in subcountmap:
                    subcountmap[submissionDate] = subcountmap[submissionDate] + 1
                else:
                    subcountmap[submissionDate] = 1
                temp.append(submission_id)

            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                submission_id = re.sub('\s+', '', str(cells[0].text))
                submissionDate = re.sub('\s+', '', str(cells[1].text))
                submissionDate = submissionDate[0:10]
                if submissionDate in subcountmap:
                    subcountmap[submissionDate] = subcountmap[submissionDate] + 1
                else:
                    subcountmap[submissionDate] = 1
                temp.append(submission_id)

            if temp == temp2:
                break
            start += 20
        subcountmaplist = list(subcountmap.items())
        return {
            'platform': 'spoj',
            'user_name': username,
            'subcountmap': subcountmaplist
        }


if __name__ == '__main__':
    print('START RUNNING SPOJ SCRAPPER SCRIPT\n')
    spoj_scrapper = SPOJUnsolvedProblems()
    # resp = spoj_scrapper.get_user_info('tarango_khan')
    #resp = atcoder_scrapper.get_user_submission_count('fsshakkhor')
    # print(resp)
    lol2 = spoj_scrapper.get_submission_count_per_day('fsshakkhor')
    print(lol2)
