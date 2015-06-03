import urllib2
import json
from datetime import datetime

SERVER_URL = 'http://localhost:1234/'
USERNAME = 'shassaro'
PASSWORD = '1'

def main():
    try:
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, SERVER_URL, USERNAME, PASSWORD)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)

        urllib2.install_opener(opener)
        try:
            request = urllib2.Request('http://localhost:1234/scavage/', '')
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            print 'Server could not complete request. Err: ' + str(e.code)
        except urllib2.URLError as e:
            print 'Failed to reach the server. Err: ' + str(e.reason)
        else:
            result = response.read()

            str_to_write = str(datetime.now())
            json_result = json.loads(result)
            str_to_write += ' - response = ' + str(json_result)

            print str_to_write
    except Exception as e:
        print str(datetime.now()) + ' - Exception occurred: ' + str(e)

if __name__ == '__main__':
    main()
