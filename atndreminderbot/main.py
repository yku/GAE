# coding: utf-8
# vim: fileencoding=utf-8
import os
import time
import datetime
import urllib2
import xml.dom.minidom
import simplejson
import oauth
import atnd

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, util

ROOT_PATH = os.path.dirname(__file__)

USERNAME='Your Consumer Key'
PASSWORD='Your Consumer Secret'
ACCESS_TOKEN_KEY='Access Token Key'
ACCESS_TOKEN_SECRET='Access Token Secret'

class TweetHandler(webapp.RequestHandler):
    def __init__(self):
        self.client = oauth.TwitterClient(USERNAME,
                                          PASSWORD,
                                          None)
        self.atnd = atnd.Api() 
    def get(self):
        followers = self.get_followers()
        for follower in followers:
            screen_name = follower['screen_name'].encode('utf-8')
            res = self.atnd.event_search({'twitter_id':screen_name})
            for r in res['event']:
                start = datetime.datetime(*time.strptime(r['started_at'], "%Y-%m-%dT%H:%M:%S+09:00")[0:6])
                now = datetime.datetime.now()
                if now < start:
                    limit = start - now
                    if limit.days in (1, 3, 5):
                        tweet = "@%s %sまであと%d日です %s" % (screen_name.encode('utf-8'), r['title'].encode('utf-8'), limit.days, r['event_url'].encode('utf_8'))
                        self.update(tweet) 
        
    def update(self, tweet):
        param = {'status': tweet }
        self.client.make_request('http://twitter.com/statuses/update.json',
                                 token=ACCESS_TOKEN_KEY,
                                 secret=ACCESS_TOKEN_SECRET,
                                 additional_params=param,
                                 protected=True,
                                 method='POST')
        self.response.out.write('')

    def get_followers(self):
        result = self.client.make_request('http://twitter.com/statuses/followers.json',
                                          token=ACCESS_TOKEN_KEY,
                                          secret=ACCESS_TOKEN_SECRET,
                                          protected=True)
        return simplejson.loads(result.content)

        

def main():
    application = webapp.WSGIApplication(
                                        [('/', TweetHandler)],
                                        debug=None)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
