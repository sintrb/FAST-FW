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
#         print url
        req = urllib2.Request(url)
        req.add_header('Authorization', self.authstring)
        return urllib2.urlopen(req).read()

class Fast(Router):
    def gethtml(self, path):
        return Router.gethtml(self, path).decode('gbk')

class FastFW(Fast):
    wan = None
    lan = None
    wlan = None
    
    def get_val(self, s):
        return eval(s)
    def get_arrval(self, html, name):
        arr = self.get_val(re.findall('%s = new Array\(([^\0]*?)\);'%name, html, re.IGNORECASE)[0].replace('\r','').replace('\n',''))
        return arr
    def get_wlan(self):
        if not self.wlan:
            self.get_all()
        return self.wlan
    def get_lan(self):
        if not self.lan:
            self.get_all()
        return self.lan
    def get_wan(self):
        if not self.wan:
            self.get_all()
        return self.wan
    def get_all(self, html=None):
        if not html:
            html = self.gethtml('/userRpm/StatusRpm.htm')
        arr = self.get_arrval(html, 'wlanPara')
        self.wlan = {'mac':arr[4], 'ip':arr[5], 'ssid':arr[1]}
        arr = self.get_arrval(html, 'lanPara')
        self.lan = {'mac':arr[0], 'ip':arr[1], 'mask':arr[2]}
        arr = self.get_arrval(html, 'wanPara')
        self.wan = {'mac':arr[1],'ip':arr[2], 'mask':arr[4], 'gateway':arr[7], 'dns':arr[11]}
        
    def get_clients(self):
        html = self.gethtml('/userRpm/AssignedIpAddrListRpm.htm')
        arr = self.get_arrval(html, 'DHCPDynList')
        return [{'name':arr[i*4+0], 'mac':arr[i*4+1], 'ip':arr[i*4+2], 'time':arr[i*4+3]} for i in range((len(arr)-2)/4)]
    
    def wan_cutdown(self):
        html = self.gethtml('/userRpm/StatusRpm.htm?Disconnect=%B6%CF%20%CF%DF&wan=1')
        print html
    
    def wan_connect(self):
        html = self.gethtml('/userRpm/StatusRpm.htm?Connect=%C1%AC%20%BD%D3&wan=1')
        return html
    
    def wan_reconnect(self):
        return self.wan_cutdown() and self.wan_connect()
    
    def reboot(self):
        return self.gethtml('/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7')

    
fw = FastFW('notcmcc', '1234567809', routerport=8765)
# fw = FastFW('trb', '1234567809', routerport=80)

print fw.get_wlan()
print fw.get_lan()
print fw.get_wan()
# print fw.reboot()

print fw.wan_connect()

print 'clients:'
for client in fw.get_clients():
    print client









