from __future__ import annotations
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
import typing
import io
import requests
import random
import pyjson5
import re
import base64
# Native JSON lib won't support non-standard JSON(actually JS objects)

random_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'


class Encryptor:
    @staticmethod
    def _rds(len: int) -> str:
        return ''.join([random.choice(random_chars) for _ in range(len)])

    @staticmethod
    def _gas(data, key0, iv0) -> str:
        key, iv = key0, iv0

        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encoder = PKCS7Encoder()
        padded_text = encoder.encode(data)
        encrypted = encryptor.encrypt(padded_text)
        # Salt is empty, so we don't need to implement
        # `crypto.format.OpenSSL.stringify(a)`.
        return base64.b64encode(encrypted)

    @staticmethod
    def encrypt(data: str, salt: str) -> str:
        if salt == '':
            return data
        return Encryptor._gas(Encryptor._rds(64) + data, salt, Encryptor._rds(16))


class Crawler:
    def __init__(self) -> typing.NoReturn:
        pass

    def login(self, username: str, password: str) -> Crawler:
        url = 'https://ids.shanghaitech.edu.cn/authserver/login'
        self.ids_session = requests.Session()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://ids.shanghaitech.edu.cn',
            'Referer': url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = self.ids_session.get(url, headers=headers)
        # print(self.ids_session.cookies)
        salt = re.search(
            r'var pwdDefaultEncryptSalt = "([^"]+)"',
            response.text
        ).group(1)
        # print(salt)
        lt = re.search(
            r'name="lt" value="([^"]+)"',
            response.text
        ).group(1)
        execution = re.search(
            r'name="execution" value="([^"]+)"',
            response.text
        ).group(1)
        #salt = lt = execution = '123qweasd2der23ew98210392jfi3829'
        data = {
            'username': (None, username),
            'password': (None, Encryptor.encrypt(password, salt)),
            'lt': (None, lt),
            'dllt': (None, 'userNamePasswordLogin'),
            'execution': (None, execution),
            '_eventId': (None, 'submit'),
            'rmShown': (None, '1'),
            'pwdDefaultEncryptSalt': (None, salt)
        }
        self.login_response = self.ids_session.post(
            url, files=data, headers=headers)
        return self

    def set_SESSION(self, SESSION: str) -> Crawler:
        self.SESSION = SESSION
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
            cookies={'JSESSIONID': self.SESSION},
        )
        # sc: Current enrollment; lc: Max enrollment
        return pyjson5.loads(
            response.text[response.text.index('=')+1:].rstrip(';')
        )

    def crawl_courses_meta(self):
        response = requests.get(
            url=('https://eams.shanghaitech.edu.cn/eams'
                 '/stdElectCourse!data.action'),
            params={'profileId': 1744},
            cookies={'JSESSIONID': self.SESSION},
        )
        non_standard_json = response.text[response.text.index(
            '=')+1:].rstrip(';')
        courses = pyjson5.loads(non_standard_json)

        return courses
