"""
WSGI config for Bl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0,root)
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bl.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "Bl.settings"


from django.contrib.auth.handlers.modwsgi import check_password

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
