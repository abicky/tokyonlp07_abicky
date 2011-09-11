#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
import sys
import re
import codecs

def format_tweet(tweet):
    # remove CR and LF
    tweet = re.sub(r'[\r\n]', ' ', tweet)
    # remove URL
    tweet = re.sub(r'\s*https?://[-\w.#&%@/?=]*\s*', ' ', tweet)
    # remove hash tags
    tweet = re.sub(r'(^|\s+)#[^\s]+\s*', ' ', tweet)
    # remove user names
    tweet = re.sub(r'\s*(?<!\w)@\w+(?!@)\s*', ' ', tweet)
    return tweet


api = tweepy.API()
f = open('tweets.dat', 'w')
f = codecs.lookup('utf_8')[-1](f)
for c, user in zip((-1, 1), ('a_bicky', 'midoisan')):
    print 'user: ' + str(user)
    for i in range(1, 7):  # get about 500 tweets per user
        while True:
            print ' page: ' + str(i)
            try:
                statuses = api.user_timeline(user, count = 200, page = i)
                break
            except KeyboardInterrupt:
                print
                sys.exit()
            except:
                print "Try again..."
        for tweet in map(lambda s:format_tweet(s.text), statuses):
            f.write('%s #%s\n' % (c, tweet))  # save as SVMlight data format
f.close()
