import os
import sys
import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0,root)

os.environ["DJANGO_SETTINGS_MODULE"] = "Bl.settings"
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()
