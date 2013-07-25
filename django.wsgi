import os, sys, site
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(project)
sys.path.append(workspace)
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

