from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.transport.http import HttpTransport
import urllib2
import time
from random import random

AUTH_URL_ver2 = 'http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'  #version 2.0
AUTH_URL_ver3 = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
outputlist = []


#start block if using IP authentication.
class HTTPAuthSender(urllib2.BaseHandler):
    def __init__(self, username):
        self.username = username
    def http_request(self,req):
        req.add_header('authorization', 'Basic ' + self.username)
        return req
#block quote end


def auth(ver, type, username, password):

    if ver == 2:
        if type == 'up':
            auth_client = Client(AUTH_URL_ver2, username = username, password = password) #version 2.0
            SID = auth_client.service.authenticate()
            return SID
        elif type == 'ip':
            auth_client = Client(AUTH_URL_ver2)
            SID = auth_client.service.authenticate()
            return SID
        else:
            print "Type either 'ip' or 'up'. 'ip' for ip access, 'up' for username/password access"
    elif ver == 3:
        if type == 'up':
            username_password = ['username_password'][username]
                #Your username/password from a purchased subscription should go here!
            auth = HttpTransport()
            auth_sender = urllib2.build_opener(HTTPAuthSender(username_password))
            auth.urlopener = auth_sender
            auth_client = Client(AUTH_URL_ver3, transport = auth)
            SID = auth_client.service.authenticate()
            return SID
        elif type == 'ip':
            auth_client = Client(AUTH_URL_ver3) #comment out if using username, password. #version 3.0
            SID = auth_client.service.authenticate()
            return SID
        else:
            print "Type either 'ip' or 'up'. 'ip' for ip access, 'up' for username/password access. username is an integer, password can be a null value for version 3."
    else:
        print "Authentication failed. Invalid version. Your request was not supported by this authentication module."


def authlist(ver, type, username_start, username_end):
    outputlist = []
    for username_index in range(username_start, (username_end + 1)):
        SID = auth(ver, type, (username_index - 1),'null')
        print SID
        outputlist.append(SID)
        lag_time = random() * 5 + 0.1
        time.sleep(lag_time)
        print('Throttle lag time: ', lag_time)
    return outputlist

