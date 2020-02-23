"""
TWITTER API MODULE
"""
import json
import ssl
import urllib.error
import urllib.request


import twurl
from engine import main
from chatbot import to_end
FL_NAME = "file.json"
TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def start():
    """
    Main body
    """
    while True:
        print('')
        acct = input('Enter Twitter Account:')
        if len(acct) < 1:
            break
        url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '100'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        jsn = json.loads(data)
        with open(FL_NAME, encoding="utf-8", mode="w") as f_l:
            json.dump(jsn, f_l, indent=4, ensure_ascii=False)
        main(FL_NAME)
        headers = dict(connection.getheaders())
        print('\nRemaining', headers['x-rate-limit-remaining'], '\n')
        if to_end(bonus=True):
            break


if __name__ == "__main__":
    start()
