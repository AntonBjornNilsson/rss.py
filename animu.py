import feedparser
from time import sleep
import json
import requests
import atexit
import pickle
import procname

webhook_url = "https://discordapp.com/api/webhooks/524396048018440194/Ih8ptB6mIAsGZgo5ZGLCgu6ljemjPhkTiB1T--sr4WqUeJYqSWlXyq4RWvD7IGnJyZAs"
guid_list = []
#guid_list = ['KBHUIUJIFPT7DZFRTAUWZAHHSO5Q2I7U']
wanted = ['Toaru Majutsu no Index III', 'One Piece','Slime']

def clean_up():
    print "Exiting program"
    with open('already_posted.txt', 'wb') as f:
            pickle.dump(guid_list,f)

def prepare_post(ep):
    json = make_json(ep)
    send_post(json)

def make_json(ep):
    title = ep.title[15:-12]
    json_x = { 
            'embeds': [{
                'title': title,
                'footer':{'text':'HorribleSubs - 1080p'},
                'description':'\n '+ep.link,
                }]
            }
    print json.dumps(json_x)
    return json.dumps(json_x)

def send_post(json_x):
    headers = {"content-type": "application/json"}
    params = (('priority', 'normal'),)
    r = requests.post(webhook_url,headers=headers,params=params,data=str(json_x))
    print r.text 

def post_method(list_ep):
    
    for ep in list_ep:
        if any(s in ep.title for s in wanted):
            print ep.guid
            print guid_list
            if ep.guid in guid_list:
                print 'not added'
            else: 
                guid_list.append(ep.guid)
                print 'added'
                prepare_post(ep)
            print ep.title

def run():
    atexit.register(clean_up)
    while(True):
        feed = feedparser.parse('http://www.horriblesubs.info/rss.php?res=1080')
        list_ep = feed.entries
        post_method(list_ep)
        print guid_list 
        sleep(3600)

print "Hello, booting"
procname.setprocname('animu')
with open("already_posted.txt", "rb") as fp:
        guid_list = pickle.load(fp)
        print guid_list
run()



