# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.lang import Builder
from datetime import datetime
import re, requests, json

Kv = '''
MDScreen:
    MDFloatingActionButton:
        pos:root.width-self.width-dp(10),dp(10)
        icon: "account-search"
        md_bg_color: app.theme_cls.primary_color
        
    MDLabel:
        id:NO_INFO_LABEL
        pos_hint:{'center_x':.5,'center_y':.5}
        size_hint:None,None
        size:dp(150),dp(30)
        text:'No information !?'
        halign:'center'
        theme_text_color:'Hint'
'''

class get_sessionid:
    '''

    How to use this class ?
     ... sessionid = get_sessionid('username','passward')
     ... print (sessionid.text) # type :str
     ... # or
     ... print (str(sessionid)) # type :str
     ... print (sessionid) # type :class

    How to check password and user?
     ... sessionid = get_sessionid('username','passward')
     ... if sessionid.text:
     ...    print (True)
     ... else:
     ...    print(False)

    '''
    LINK = 'https://www.instagram.com/accounts/login/'
    LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'
    text = False

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.__str__()

    def __str__(self):
        time = int(datetime.now().timestamp())
        payload = {
            'username': ''+self.username+'',
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        with requests.Session() as s:
            r = s.get(self.LINK)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
            r = s.post(self.LOGIN_URL, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken":csrf
            })
        temp = str(s.cookies).split(' ')
        sessionid= ''
        for i in temp:
            if 'sessionid=' in i:
                sessionid = i.replace('sessionid=','')
                self.text = sessionid
                return sessionid
                break
        self.text = ''
        return ''

class get_insta_info:
    sessionid = None
    headers = {
        'Host': 'www.instagram.com',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
        'Connection': 'close',
        'X-IG-App-ID': '936619743392459',
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-WWW-Claim': 'hmac.AR0uQ3YRnOII5ROjBT7pKkMy1bjATWrSkfZCgwbaUBjNv-rw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Referer': 'https://www.instagram.com/accounts/access_tool/former_phones',
        'Cookie': 'ig_cb=1; ig_did=69205DC3-D787-47E5-B250-1C4A7ADC3A05; csrftoken=HKmRQ2ZwuqCZjpMycM3xOVIjDUBo5HWd; mid=XoSg-AAEAAHRshuq4BlxladvlcbE; datr=HmBKXyPTk86RJpmkaUQ7eM5w; urlgen="{\"51.36.8.205\": 43766}:1kLnkz:ZHs58RZnu4USDtTqolZcEXDJp7s"; rur=ATN; ds_user_id=37466401585',
        'DNT': '1'
    }

    def __init__(self):
        pass

    def get_requst(self,url):
        cookies = {
            'sessionid':str(self.sessionid),
        }
        url = 'https://www.instagram.com/accounts/access_tool/former_phones?__a=1'
        req = requests.request("GET", url, headers=self.headers, cookies=cookies)
        if req.status_code:
            data = req.text
            data = json.loads(data)['data']
            data = json.dumps(data,indent=2)
            self.on_requst(data)

    def on_requst(self,data):
        print(data)

class Insta_App(MDApp):
    def build(self):
        self.root = Builder.load_string(Kv)

if __name__=='__main__':
    # test
    insta = get_insta_info()
    insta.sessionid = get_sessionid('username','password').text
    insta.get_requst('')

    # user enterface...
    Insta_App().run()
