from __future__ import annotations
import typing

import requests
#import random
import pyjson5 
# Native JSON lib won't support non-standard JSON(actually JS objects)

#possible_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'.upper()


class Crawler:
    def __init__(self) -> typing.NoReturn:
        pass

    def login(self, username: str, password: str) -> Crawler:
        self.login_response = requests.post(
            url=('https://controller.shanghaitech.edu.cn:8445'
                 '/PortalServer/Webauth/webAuthAction!login.action'),
            data={'userName': username,
                  'password': password,
                  #'hasValidateCode': 'false',
                  #'validCode': '',
                  #'hasValidateNextUpdatePassword': 'true'
                  },
            #headers={'Accept': '*/*',
                     #'Content-Type': 'application/x-www-form-urlencoded',
                     #'JSESSIONID': ''.join(random.sample(possible_chars, 32)),
                     # This is distributed by the server,
                     # rather than randomly generated.
                     #'User-Agent':  # Hide yourself
                     #('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     # 'AppleWebKit/537.36 (KHTML, like Gecko) '
                     # 'Chrome/70.0.3538.77 '
                     # 'Safari/537.36')
                     #}
        )
        return self

    def set_JSESSION(self, JSESSION: str) -> Crawler:
        self.JSESSION = JSESSION
        return self

    def set_goal(self, SEMESTER: int) -> Crawler:
        self.SEMESTER = SEMESTER
        return self

    def crawl_courses_status(self) -> dict[int, dict[str, int]]:
        response = requests.get(
            url=('https://eams.shanghaitech.edu.cn'
                 '/eams/stdElectCourse!queryStdCount.action'),
            params={'projectId': 1,
                    'semesterId': self.SEMESTER},
            cookies={'JSESSIONID': self.JSESSION},
        )
        # sc: Current enrollment; lc: Max enrollment
        return pyjson5.loads(response.text[response.text.index('=')+1:].rstrip(';'))
        
    def crawl_courses_meta(self):
        response = requests.get(
            url=('https://eams.shanghaitech.edu.cn/eams'
                 '/stdElectCourse!data.action'),
            params={'profileId': 1744},
            cookies={'JSESSIONID': self.JSESSION},
        )
        non_standard_json = response.text[response.text.index(
            '=')+1:].rstrip(';')
        courses = pyjson5.loads(non_standard_json)
        
        return courses
