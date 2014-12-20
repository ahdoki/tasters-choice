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
        req.add_header('cookie', 'SID="' + self.SID + '"') #adds a header to the xml request.
        return req

    https_request = http_request

def retrieve_by_id(input_term, ver, start_record, max_count, SID):
    '''
    This is a method used for subscribed services.
    :param input_term: input search term.
    :param ver: Version 2 or 3. Refer to Thomson Reuters Documentation for details.
    :param start_record: starting record point
    :param max_count: maximum request count
    :param SID: Session ID.
    :return: output xml
    '''
    http = HttpTransport()
    opener = urllib2.build_opener(HTTPSudsPreprocessor(SID))
    http.urlopener = opener
    client_obj = Client(SEARCH_URL[int(ver - 2)], transport = http, retxml = True)
    rparams = {
                'count' : max_count, # 1-100
                'firstRecord' : start_record,
                'sortField' : [{
                            'name' : 'Relevance',
                            'sort' : 'D',
                            }]
                }
    cited_results = client_obj.service.retrieveById('DIIDW', input_term, 'en', rparams)
    return cited_results


def retrieve_by_id_lite(input_term, ver, start_record, max_count, SID):
    '''
    This is a method used for lite services.
    :param input_term: input search term.
    :param ver: Version 2 or 3. Refer to Thomson Reuters Documentation for details.
    :param start_record: starting record point
    :param max_count: maximum request count
    :param SID: Session ID.
    :return: output xml
    '''
    http = HttpTransport()
    opener = urllib2.build_opener(HTTPSudsPreprocessor(SID))
    http.urlopener = opener
    client_obj = Client(SEARCH_LITE_URL[int(ver - 2)], transport = http, retxml = True)
    rparams = {
                'count' : max_count, # 1-100
                'firstRecord' : start_record,
                'sortField' : [{
                            'name' : 'Relevance',
                            'sort' : 'D',
                            }]
                }
    cited_results = client_obj.service.retrieveById('DIIDW', input_term, 'en', rparams)
    return cited_results
