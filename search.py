from suds.client import Client
from suds.transport.http import HttpTransport
import urllib2

SEARCH_LITE_URL = ['http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl',  #version 2.0
                   'http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl'] #version 3.0

SEARCH_URL = ['http://search.isiknowledge.com/esti/wokmws/ws/WokSearch?wsdl',   #version 2.0
            'http://search.webofknowledge.com/esti/wokmws/ws/WokSearch?wsdl'] #version 3.0

class HTTPSudsPreprocessor(urllib2.BaseHandler):
    def __init__(self, SID):
        self.SID = SID

    def http_request(self, req):
        req.add_header('cookie', 'SID = "' + self.SID + '"')
        return req

    https_request = http_request

def search(fieldtag, searchterm, ver, count, SID):
    '''
    Makes a search query to the database.
    :param fieldtag: fieldtag must be 'PN = ' or 'CD ='
    :param searchterm: search term. in this case, the patent number.
    :param ver: version 2 or 3. refer to the thomson reuters documentation.
    :param count: requested retrieval count.
    :param SID: Session ID.
    :return: output xml.
    '''

    http = HttpTransport()
    opener = urllib2.build_opener(HTTPSudsPreprocessor(SID))
    http.urlopener = opener
    client_obj = Client(SEARCH_URL[int(ver - 2)], transport = http, retxml = True)

    query = fieldtag + '=' + searchterm
    #construct query and retrieve field parameters
    qparams = {
                'databaseId' : 'DIIDW',
                'userQuery' : query,
                'queryLanguage' : 'en',
                'editions' : [{
                            'collection' : 'DIIDW',
                            'edition' : 'CDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'MDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'EDerwent',
                            }]
                }
    rparams = {
                'count' : count, # 1-500
                'firstRecord' : 1,
                'sortField' : [{
                            'name' : 'Relevance',
                            'sort' : 'D',
                            }]
                }
    result = client_obj.service.search(qparams, rparams)
    return result

def search_by_cd(search_term, ver, count, SID):
    #fieldtag must be 'PN = ' or 'CD ='
    http = HttpTransport()
    opener = urllib2.build_opener(HTTPSudsPreprocessor(SID))
    http.urlopener = opener
    client_obj = Client(SEARCH_URL[int(ver - 2)], transport = http, retxml = True)

    query = 'CD =' + search_term
    #construct query and retrieve field parameters
    qparams = {
                'databaseId' : 'DIIDW',
                'userQuery' : query,
                'queryLanguage' : 'en',
                'editions' : [{
                            'collection' : 'DIIDW',
                            'edition' : 'CDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'MDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'EDerwent',
                            }]
                }
    rparams = {
                'count' : count, # 1-500
                'firstRecord' : 1,
                'sortField' : [{
                            'name' : 'Relevance',
                            'sort' : 'D',
                            }],
                'viewField':[{
                            'collectionName': 'DIIDW',
                            'fieldName' : 'DCE',
                            }]
                }
    result = client_obj.service.search(qparams, rparams)
    return result

def search_lite(fieldtag, searchterm, ver, count, SID):
    #fieldtag must be 'PN = ' or 'CD ='
    http = HttpTransport()
    opener = urllib2.build_opener(HTTPSudsPreprocessor(SID))
    http.urlopener = opener
    client_obj = Client(SEARCH_LITE_URL[int(ver - 2)], transport = http, retxml = True)

    query = fieldtag + '=' + searchterm
    #construct query and retrieve field parameters
    qparams = {
                'databaseId' : 'DIIDW',
                'userQuery' : query,
                'queryLanguage' : 'en',
                'editions' : [{
                            'collection' : 'DIIDW',
                            'edition' : 'CDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'MDerwent',
                            },{
                            'collection' : 'DIIDW',
                            'edition' : 'EDerwent',
                            }]
                }
    rparams = {
                'count' : count, # 1-500
                'firstRecord' : 1,
                'sortField' : [{
                            'name' : 'TC',
                            'sort' : 'D',
                            }]
                }
    result = client_obj.service.search(qparams, rparams)
    return result
