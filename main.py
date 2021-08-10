import requests
import operator
import json
from urllib import request
from datetime import datetime
from random import randrange
from time import sleep

##print("hello word")


def loadTagFromFile(fname):
    tags = {}
    with open(fname) as f:
        for line in f:
            tags[line.replace('\n', '')] = -1
    return tags


def saveTagToFile(fname, d):
    f = open(fname, 'w')
    for k, v in d.items():
        f.write(str(k) + ':' + str(v) + '\n')
    f.close()
    print("done")


def parseStatsFromInstagram(tagDict, login, psw):
    # authorize on instagram
    d = tagDict
    time = int(datetime.now().timestamp())
    url = 'https://www.instagram.com/accounts/login/'
    url_main = url + 'ajax/'
    auth = {
        'username': login,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:' + psw,
        'queryParams': {},
        'optIntoOneTap': 'false'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'referer': 'https://www.instagram.com/accounts/login/'
    }
    with requests.Session() as s:
        s.headers.update(headers)
        req = s.get(url)
        headers['x-csrftoken'] = req.cookies['csrftoken']
        s.post(url_main, data=auth, headers=headers)
        for tag in d.keys():  # get stats for every tag in dict
            r = s.get('https://www.instagram.com/explore/tags/' +
                      request.quote(str(tag).encode('cp1251')) + '/?__a=1')
            j = json.loads(r.text)

            if type(j['data']['media_count']) == int:
                d[tag] = j['data']['media_count']
            else:
                d[tag] = -1  # if stats are not available for any reason set -1
            #print(str(tag) + ': ' + str(d[tag]))
            sleep(randrange(0, 1))  # adding a random delay between requests
    return d


def main():
    # load file
    tags = loadTagFromFile('tags.txt')

    # login data
    login = 'login_here'
    psw = 'passowd_here'

    # parse statistics
    tags = parseStatsFromInstagram(tags, login, psw)

    # sort dictronary
    tags = dict(sorted(tags.items(), key=operator.itemgetter(1), reverse=True))

    # save to file
    saveTagToFile('out.txt', tags)


main()