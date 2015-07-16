from instagram import client, subscriptions
import redis
import json
from types import NoneType
import subprocess
import sched
import time

r = redis.Redis(
    host='localhost'
    )

CONFIG = {
    'client_id': '47f3adaae6a245c7bca634f7d85e8fa3',
    'client_secret': 'b4a9405a9e184d3db73a93f42f655e09',
    'redirect_uri': 'http://127.0.0.1:8515/oauth_callback'
}

access_token="45955562.47f3ada.b9472e0e606b4b30ba59cdd97a7309de"
users = [
    {'username': 'dagelan', 'max_id': '', 'recent_media': []}, 
    {'username': 'anzhari_p', 'max_id': '', 'recent_media': []}
]

unauthenticated_api = client.InstagramAPI(**CONFIG)
api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])

def send_updates():
    messages = ''
    for user in users:
        user_id = api.user_search(q=user['username'], count=1)
    #    user['recent_media'], user['max_id'] = api.user_recent_media(user_id, max_id=user['max_id'])
    #    recent_media, max_id = api.user_recent_media(user_id=user_id[0].id, count=20)
        recent_media, max_id = api.user_recent_media(user_id=user_id[0].id, count=20, max_id=r.get(user_id[0].username + ':max_id'))
        r.set(user['username'] + ':max_id', user['max_id'])
        print r.get(user_id[0].username + ':max_id')
        media_info = ''
        for media in recent_media:
            caption_text = ''
            image_url = ''
            username = ''
            if hasattr(media, 'caption'):
                if type(media.caption) is not NoneType:
                    caption_text = unicode(media.caption.text)
            if hasattr(media, 'images'):
                image_url = media.images['standard_resolution'].url
            if hasattr(media, 'user'):
                username = media.user.username    
            media_info = media_info + '<div><img src=' + image_url + '><br>' + username + ': ' + caption_text + '<br></div>\n'
        messages = messages + media_info


    #messages = messages.encode('utf-8')
    #html_mail = 'To: ns.nenden@gmail.com\nSubject: Instagram Distributor Update\nContent-Type: text/html; charset=\'us-ascii\'\n<html>\n' + messages + '\n</html>'

    #mail = subprocess.Popen(['sendmail', 'ns.nenden@gmail.com'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    #send_mail = mail.communicate(input=html_mail)[0]

s = sched.scheduler(time.time, time.sleep)
