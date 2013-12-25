# -*- coding: UTF-8 -*
'''
Created on 2013-12-25

@author: Robin
'''
import httplib
import urllib2

class Router(object):
    def __init__(self, adminname=None, adminpass=None, routerip='172.16.0.1', routerport=80):
        self.adminname = adminname
        self.adminpass = adminpass
        self.routerip = routerip
        self.routerport = routerport
    def gethtml(self, path):
        url = 'http://%s:%d%s'%(self.routerip, self.routerport, path)
        print url
        req = urllib2.Request(url)
        urllib2.urlopen(req)

class Fast(Router):
    pass

class FastFW(Fast):
    pass


Router('trb', '1234567809').gethtml('/')