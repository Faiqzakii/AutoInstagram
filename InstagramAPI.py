import requests, json, re, time, random

class InstagramAPI:
    """
    Created by Faiqzakii
    """

    def __init__(self, username = None, password = None, session = {}):
        self.username = username
        self.password = password
        self.loggedin = False
        self.session  = session
        self.headers  = {}
        self.base_url = "https://www.instagram.com"

    def getHeaders(self):

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36'
        }

        if self.session != {}:
            headers["x-crsftoken"] = self.session["crsftoken"]
            headers["cookie"] = 'crsftoken=' + self.session['crsftoken'] + '; sessionid=' + self.session['sessionid']
        self.headers = headers

    def getTime(self):
        t = str(time.time())
        timenow = t.split('.')[0]
        return timenow

    def getStr(self, string, start, end, index = 1):
        try:
            str = string.split(start)
            str = str[index].split(end)
            return str[0]
        except:
            return False

    def login(self):
        fetch_url = self.base_url + '/accounts/login/'
        login_url = fetch_url + 'ajax/'

        fetch_cookies = requests.get(fetch_url).headers
        csrf = self.getStr(str(fetch_cookies), 'csrftoken=', ';')
        mid = self.getStr(str(fetch_cookies), 'mid=', ';')

        headers = {
            'Host': 'www.instagram.com',
            'x-csrftoken': csrf,
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; LM-G710 Build/PKQ1.181105.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36',
            'cookie': 'rur=FTW; mid='+mid+'; csrftoken='+csrf
        }

        data = {
            'username': self.username,
            'password': self.password
        }

        fetch_login = requests.post(login_url, data = data, headers = headers)
        log = json.loads(fetch_login.text)
        if log['authenticated'] == False:
            login_data = {
                'action': 'login',
                'status': 'error',
                'username': self.username,
                'details': 'wrong username/password'
            }
        elif log['authenticated'] == True:
            self.loggedin = True
            login_data = {
                'action': 'login',
                'status': 'success',
                'username': self.username,
                'csrftoken': self.getStr(str(fetch_login.headers), 'csrftoken=', ';'),
                'sessionid': self.getStr(str(fetch_login.headers), 'sessionid=', ';')
            }

            self.session = login_data
            self.headers['x-csrftoken'] = self.session['csrftoken']
            self.headers['cookie'] = 'csrftoken=' + self.session['csrftoken'] +'; sessionid=' + self.session['sessionid']
        else:
            login_data = fetch_login.text

        return login_data

    def getHome(self):
        timeline_id = []
        resp = requests.get(self.base_url, headers = self.headers)
        data = self.getStr(resp.text, "window.__additionalDataLoaded('feed',", ");</script>")

        if data != False:
            json_timeline = json.loads(data)
            results = json_timeline['user']['edge_web_feed_timeline']

            for i in results['edges']:
                if i['node']['viewer_has_liked'] == False:
                    timeline_id.append(i['node']['id'])
            return timeline_id
        else:
            print("You're not logged in!")
            return False

    def getStory(self):
        story_id = []
        resp = requests.get(self.base_url, headers = self.headers)
        query_hashed = self.getStr(resp.text, '/graphql/query/?query_hash=', '&amp', 1)

        url = 'https://www.instagram.com/graphql/query/?query_hash=%s&variables={"reel_ids":[],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,"story_viewer_fetch_count":50,"story_viewer_cursor":"","stories_video_dash_manifest":false}'%(query_hashed)
        resp = requests.get(url, headers = self.headers)
        jeson = json.loads(resp.text)

        results = jeson['data']['user']['feed_reels_tray']['edge_reels_tray_to_reel']

        for i in results['edges']:
            user_id = i['node']['id']
            username = i['node']['user']['username']

            if i['node']['items'] != None:
                for b in i['node']['items']:
                    reelMediaId = b['id']
                    taken_at = b['taken_at_timestamp']
                    data = {
                        'reelid' : reelMediaId,
                        'user_id': user_id,
                        'taken_at': str(taken_at),
                        'username': username
                    }

                    story_id.append(data)
        return story_id

    def seeStory(self, reelMediaId, user_id, taken_at):
        data = {
            'reelMediaId' : reelMediaId,
            'reelMediaOwnerId': user_id,
            'reelId': user_id,
            'reelMediaTakenAt': taken_at,
            'viewSeenAt': self.getTime()
        }

        url = self.base_url + "/stories/reel/seen"
        resp = requests.post(url, headers = self.headers, data = data)
        status = json.loads(resp.text)

        if status['status'] == 'ok':
            print("Success seen story_id {}".format(reelMediaId))
            status_res = True
        else:
            print("Failed seen story_id {}".format(reelMediaId))
            status_res = False
        return status_res

    def likePost(self, id_post):
        url = self.base_url + '/web/likes/{}/like/'.format(id_post)
        resp = requests.post(url, headers =  self.headers)
        status = json.loads(resp.text)

        if status['status'] == 'ok':
            print("Success like post_id {}".format(id_post))
            status_res = True
        else:
            print("Failed like post_id {}".format(id_post))
            status_res = False
        return status_res

    def unlikePost(self, id_post):
        url = self.base_url + '/web/likes/{}/unlike/'.format(id_post)
        resp = requests.post(url, headers =  self.headers)
        status = json.loads(resp.text)

        if status['status'] == 'ok':
            print("Success unlike post_id {}".format(id_post))
            status_res = True
        else:
            print("Failed unlike post_id {}".format(id_post))
            status_res = False
        return status_res
