# -*- coding: UTF-8 -*
'''
Created on 2013-12-25

@author: Robin
'''
import urllib2
import base64
import re

class Router(object):
    def __init__(self, adminname=None, adminpass=None, routerip='172.16.0.1', routerport=80):
        self.adminname = adminname
        self.adminpass = adminpass
        self.routerip = routerip
        self.routerport = routerport
        
        # 简单验证 (Basic and Digest Authentication)
        self.authstring = 'Basic %s'%base64.b64encode('%s:%s'%(self.adminname, self.adminpass))
    def gethtml(self, path):
        url = 'http://%s:%d%s'%(self.routerip, self.routerport, path)
        print url
        req = urllib2.Request(url)
        req.add_header('Authorization', self.authstring)
        return urllib2.urlopen(req).read()

class Fast(Router):
    def gethtml(self, path):
        return Router.gethtml(self, path).decode('gbk')

class FastFW(Fast):
    wan = None
    def get_val(self, s):
        return eval(s)
    
    def get_wan(self):
        if not self.wan:
            html = self.gethtml('/userRpm/StatusRpm.htm')
            arr = self.get_val(re.findall('wanPara = new Array\(([^\0]*?)\);', html, re.IGNORECASE)[0].replace('\r','').replace('\n',''))
            print arr
            self.wan = {'mac':arr[1],'ip':arr[2], 'mask':arr[4], 'gateway':arr[7], 'dns1':arr[11], 'dns2':arr[12]}
        return self.wan
    def get_ip(self):
        return self.get_wan()['ip']
    
    def wan_cutdown(self):
        html = self.gethtml('/userRpm/StatusRpm.htm?Disconnect=%E6%96%AD%20%E7%BA%BF1')
    
    def wan_connect(self):
        pass
    
    def wan_reconnect(self):
        pass
print FastFW('notcmcc', '1234567809', routerport=8765).get_wan()









