import os
import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket
os.environ["DJANGO_SETTINGS_MODULE"] = "Bl.settings"
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()
