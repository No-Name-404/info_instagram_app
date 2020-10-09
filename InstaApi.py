import threading,requests,json,re
from datetime import datetime

class get_sessionid:
    '''
    How to use this class ?
     ... sessionid = get_sessionid('username','passward')
     ... print (sessionid.text) # type :str
     ... # or
     ... print (str(sessionid)) # type :str
     ... print (sessionid) # type :class

    How to check password and username?
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
    '''
    How to use this class?
     ... insta = get_insta_info()
     ... insta.start_thread(sessionid='sessionid')

    The on_requst function well be called
    to get the data.
     ... def my_callback(info,data):
     ...    print(info)
     ...    print(data)
     ... insta.on_requst = my_callback(info,data)
    '''
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
    urls = {
        'Former usernames':'https://www.instagram.com/accounts/access_tool/former_usernames?__a=1',
        'Former phones':'https://www.instagram.com/accounts/access_tool/former_phones?__a=1',
        'Former emails':'https://www.instagram.com/accounts/access_tool/former_emails?__a=1',
        'Last activity':'https://www.instagram.com/emails/emails_sent/?__a=1',
        'Accounts following you':'https://www.instagram.com/accounts/access_tool/accounts_following_you?__a=1',
        'Accounts you follow':'https://www.instagram.com/accounts/access_tool/accounts_you_follow?__a=1',
        'Current follow requests':'https://www.instagram.com/accounts/access_tool/current_follow_requests?__a=1',
        'Accounts you blocked':'https://www.instagram.com/accounts/access_tool/accounts_you_blocked?__a=1',
        'Former links in bio':'https://www.instagram.com/accounts/access_tool/former_links_in_bio?__a=1',
        'Former bio texts':'https://www.instagram.com/accounts/access_tool/former_bio_texts?__a=1',
        'Search history':'https://www.instagram.com/accounts/access_tool/search_history?__a=1',
        'Currently notarized email':'https://www.instagram.com/download/request/?__a=1',
        'Login activity': 'https://www.instagram.com/session/login_activity/?__a=1',

    }

    def start_thread(self,sessionid=None):
        if sessionid: self.sessionid=sessionid
        if self.sessionid:
            T = threading.Thread(target=self.info_handler)
            T.daemon = True
            T.start()

    def info_handler(self):
        self.on_start_requst()
        for info,url in self.urls.items():
            T = threading.Thread(target=self.get_requst, args=[info,url])
            T.daemon = True
            T.start()
            T.join()
        self.on_end_requst()

    def on_start_requst(self):
        ''' callback: when threading start '''

    def on_end_requst(self):
        ''' callback: when threading stop or end '''

    def get_requst(self,info,url):
        cookies = {
            'sessionid':str(self.sessionid),
        }
        req = requests.request("GET", url, headers=self.headers, cookies=cookies)
        if req.status_code:
            data = req.text
            try:
                if info == 'Login activity':
                    data = json.loads(data)['data']['suspicious_logins']
                else:
                    data = json.loads(data)['data']
            except KeyError:
                data = json.loads(data)['email_hint']
            data = json.dumps(data,indent=2)
            self.on_requst(info,data)

    def on_requst(self,info,data):
        ''' callback: in all requsts '''

if __name__ == '__main__':
    # test class get_sessionid
    sessionid = get_sessionid('username','password')
    print (type(sessionid),sessionid)
    print (type(sessionid.text),sessionid.text)
    print (str(sessionid)) # type is str

    # test class get_insta_info
    class insta_api(get_insta_info):
        def on_requst(self,info,data):
            print(info)
            print(data)

        def on_start_requst(self):
            print('THREADING_START')

        def on_end_requst(self):
            print('THREADING_END')

    INSTA_API = insta_api()
    INSTA_API.start_thread(sessionid=sessionid.text)