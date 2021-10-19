import time
import json
import requests
from bs4 import BeautifulSoup
import re

_http_headers = {'Content-Type': 'application/json'}

class SpojScrapper():
    def get_submission_stat_count(self, username):
            rs = requests.session()
            start = 0
            ac_count = 0
            wa_count = 0
            tle_count = 0
            mle_count = 0
            rte1_count = 0
            rte2_count = 0
            cpe_count = 0 
            others_count = 0
            solved_problems = []
            temp = []
            temp2 = []
            while start < 10000:
                url = f'https://www.spoj.com/status/{username}/all/start={start}'
                submission_page = rs.get(url=url, headers=_http_headers)
                soup = BeautifulSoup(submission_page.text, 'html.parser')
                table = soup.find("table",{"class":"newstatus"})
                temp2 = temp
                temp = []
                v = []
                for row in table.find_all("tr")[1:]:  # skipping header row
                    cells = row.find_all("td")
                    submission_id = re.sub('\s+', '', str(cells[0].text))
                    # submission_date = re.sub('\s+', '', str(cells[1].text))
                    problem_id = re.sub('\s+', '', str(cells[2].find('a').get('title')))
                    verdict = re.sub('\s+', '', str(cells[3].text))
                    temp.append(submission_id)
                    v.append(verdict)
                    #print(verdict)
                    if verdict == 'accepted':
                        ac_count = ac_count + 1
                    elif verdict == 'wronganswer':
                        wa_count = wa_count + 1
                    elif verdict == 'compilationerror':
                        cpe_count = cpe_count + 1
                    elif verdict == 'runtimeerror(SIGSEGV)':
                        rte1_count = rte1_count + 1
                    elif verdict == 'runtimeerror(SIGABRT)':
                        rte2_count = rte2_count + 1
                    elif verdict == 'timelimitexceeded':
                        tle_count = tle_count + 1
                    elif verdict == 'memorylimitexceeded':
                        mle_count = mle_count + 1
                    else:
                        others_count = others_count + 1
                    solved_problems.append(problem_id)
                if temp == temp2:
                    # print(temp)
                    # print(temp2)
                    for i in v:
                        if i == 'accepted':
                            ac_count = ac_count - 1
                        elif i == 'wronganswer':
                            wa_count = wa_count - 1
                        elif i == 'compilationerror':
                            cpe_count = cpe_count - 1
                        elif i == 'runtimeerror(SIGSEGV)':
                            rte1_count = rte1_count - 1
                        elif i == 'runtimeerror(SIGABRT)':
                            rte2_count = rte2_count - 1
                        elif i == 'timelimitexceeded':
                            tle_count = tle_count - 1
                        elif i == 'memorylimitexceeded':
                            mle_count = mle_count - 1
                        else:
                            others_count = others_count - 1
                    #print(start)
                    break
                start += 20

            return {
                'platform': 'spoj',
                'user_name': username,
                'solved_count': ac_count,
                'wrong_answer_count': wa_count,
                'time_limit_exceeded_count': tle_count,
                'memory_limit_exceeded_count': mle_count,
                'runtime_error1_count': rte1_count,
                'runtime_error2_count': rte2_count,
                'compilation_error_count': cpe_count,
                'other_verdict_count': others_count
            }

if __name__ == '__main__':
    print('START RUNNING SPOJ SCRAPPER SCRIPT\n')
    spoj_scrapper = SpojScrapper()
    # resp = spoj_scrapper.get_user_info('tarango_khan')
    submission_list = spoj_scrapper.get_submission_stat_count('starscream_73')
    print(submission_list)