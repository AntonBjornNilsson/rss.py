import argparse
import atexit
import feedparser
import json
import os
import pickle
import procname
import requests
from time import sleep


def clean_up():
    print "Exiting program"
    with open('already_posted.txt', 'wb') as f:
            pickle.dump(guid_list,f)

def prepare_post(ep, webhook_url, footer):
    json = make_json(ep, footer)
    send_post(json, webhook_url)

def make_json(ep, footer):
    # May vary depending on rss feed
    title = ep.title[15:-12]
    json_x = {
            'embeds': [{
                'title': title,
                'footer': {'text': footer},
                'description':'\n '+ep.link,
                }]
            }
    return json.dumps(json_x)

def send_post(json_x, webhook_url):
    headers = {"content-type": "application/json"}
    params = (('priority', 'normal'),)
    r = requests.post(webhook_url, headers=headers, params=params, data=str(json_x))
    assert r.status_code == 204

def post_method(list_ep, wanted, webhook_url, footer):
    for ep in list_ep:
        if any(s in ep.title for s in wanted):
            if ep.guid in guid_list:
                print 'not added'
            else:
                guid_list.append(ep.guid)
                print 'added'
                prepare_post(ep, webhook_url, footer)
            print ep.title

def run(config_path):
    json_dict = json.load(config_path)
    print json_dict
    if not 'wanted' in json_dict or not 'webhook_url' in json_dict or not 'RSS_link' in json_dict or not 'footer' in json_dict:
        print 'config incorrect, terminating program'
        quit()
    wanted = json_dict['wanted']
    webhook_url = json_dict['webhook_url']
    RSS_link = json_dict['RSS_link']
    footer = json_dict['footer']
    atexit.register(clean_up)
    feed = feedparser.parse(RSS_link)
    list_ep = feed.entries
    post_method(list_ep, wanted, webhook_url, footer)
    print "Ended successfully"

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Specify a json file to run", required=True,
                    type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()

    procname.setprocname('RSS')
    with open("already_posted.txt", "rb") as fp:
            guid_list = pickle.load(fp)
    print args.config
    run(args.config)



