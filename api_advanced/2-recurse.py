#!/usr/bin/python3
'''Defines recursive function to return hot posts in subreddit
'''
import requests


def recurse(subreddit, hot_list=[], fullname=None, count=0):
    '''fetches all hot posts in a subreddit

    Return:
        None - if subreddit is invalid
    '''
    url = 'https://www.reddit.com/r/{}/hot/.json'.format(subreddit)
    params = {'after': fullname, 'limit': 100, 'count': count}
    headers = {'user-agent': 'Mozilla/5.0 \
(Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    info = requests.get(url, headers=headers,
                        params=params, allow_redirects=False)
    if (info.status_code % 400) < 100:
        return None
    info_json = info.json()
    results = info_json.get('data').get('children')
    new_packet = [post.get('data').get('title') for post in results]
    hot_list += new_packet
    after = info_json.get('data').get('after', None)
    dist = info_json.get('data').get('dist')
    count += dist
    if after:
        recurse(subreddit, hot_list, after, count)
    return hot_list
