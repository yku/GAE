#!/usr/bin/python 
# coding: utf-8
# vim: fileencoding=utf-8

'''A library that provides a Python interface to the ATND API '''

__author__ = 'kz2yz4@gmail.com'
__version__ = '0.1'

import time
import datetime
import urllib
import urllib2
import xml.dom.minidom

class Api:
    '''
    A python interface to the ATND API
    
    Example usage:
    
      >>> import atnd
      >>> api = atnd.Api()

    To fetch event by twitter_id
      
      >>> param = {'twitter_id':'hoge'}
      >>> result = api.event_search(param)
      >>> for v in result['event']:
      >>>     print v['title']
    
    Use list if you search by keywords

      >>> param = {'twitter_id':'hoge', 'keyword':['foo', 'bar']}
      >>> result = api.event_search(param)
      >>> for v in result['event']:
      >>>     print v['title']
    '''
    def __init__(self):
        None

    def event_search(self, param={}):
        url = 'http://api.atnd.org/events/?%s' % (self.prepare_query(param))
        doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
        root = doc.documentElement 
        events_dom = root.getElementsByTagName('event')
    
        ret = {}
        ret['results_returned'] = root.getElementsByTagName('results_returned')[0].firstChild.data
        ret['results_start'] = root.getElementsByTagName('results_start')[0].firstChild.data
    
        event_structure = ('event_id',
                           'title',
                           'catch',
                           'description',
                           'event_url',
                           'started_at',
                           'ended_at',
                           'url',
                           'limit',
                           'address',
                           'place',
                           'lat',
                           'lon',
                           'owner_id',
                           'owner_nickname',
                           'owner_twitter_id',
                           'accepted',
                           'waiting',
                           'updated_at')
        event = []
        for e in events_dom:
            data = {}
            for tag in event_structure:
                elem = e.getElementsByTagName(tag)[0]
                if elem.hasChildNodes():
                    data[tag] = elem.firstChild.data
            event.append(data)

        ret['event'] = event
        
        return ret 
 
    def event_user_search(self, param={}):
        url = 'http://api.atnd.org/events/users/?%s' % (self.prepare_query(param))
        doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
        root = doc.documentElement 
    
        ret = {}
        ret['results_returned'] = root.getElementsByTagName('results_returned')[0].firstChild.data
        ret['results_start'] = root.getElementsByTagName('results_start')[0].firstChild.data
    
        events_dom = root.getElementsByTagName('event')
        event_structure = ('event_id',
                           'title',
                           'event_url',
                           'limit',
                           'accepted',
                           'waiting',
                           'updated_at')
        event = []
        for e in events_dom:
            data = {}
            for tag in event_structure:
                elem = e.getElementsByTagName(tag)[0]
                if elem.hasChildNodes():
                    data[tag] = elem.firstChild.data
            
            users_dom = e.getElementsByTagName('user')
            user_structure = ('user_id',
                              'nickname',
                              'twitter_id',
                              'status')
            data['user'] = []
            for u in users_dom:
                user_data = {}
                for tag in user_structure:
                    elem = u.getElementsByTagName(tag)[0]
                    if elem.hasChildNodes():
                        user_data[tag] = elem.firstChild.data
                data['user'].append(user_data)
            event.append(data)

        ret['event'] = event
        return ret 
    
    def prepare_query(self, param={}):
        query = ''
        for k, v in param.items():
            '''
            Target format is XML. 
            ATND default format is XML. 
            '''
            if k == 'format': continue
            if isinstance(v, list):
                for e in v:
                    query += '%s=%s&' % (k, e)
            elif isinstance(v, str):
                query += '%s=%s&' % (k, v)
            else:
                # TODO: raise exception
                None
        return query[:-1]
