#!/usr/bin/python3
"""Query for the reddit api and parse the title of all hot articles
"""

import json
import requests

def count_words(subreddit, word_list, after="", count=None):
    """Function to count words
    """

    if count is None:
        count = {word.lower(): 0 for word in word_list}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'user-agent': 'bhalut'}
    params = {'after': after}

    request = requests.get(url, params=params, headers=headers, allow_redirects=False)

    if request.status_code == 200:
        data = request.json()

        for topic in data['data']['children']:
            title_words = topic['data']['title'].split()
            for word in word_list:
                count[word.lower()] += title_words.count(word.lower())

        after = data['data']['after']
        if after is None:
            sorted_counts = sorted(count.items(), key=lambda x: (-x[1], x[0]))
            for word, word_count in sorted_counts:
                if word_count > 0:
                    print(f"{word}: {word_count}")
        else:
            count_words(subreddit, word_list, after, count)

# Example usage:
subreddit = "unpopular"
word_list = ['you', 'unpopular', 'vote', 'down', 'downvote', 'her', 'politics']
count_words(subreddit, word_list)

