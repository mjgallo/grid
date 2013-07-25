activate_this = '/home/django/.virtualenvs/grid/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import os, sys, site
apache_configuration = os.path.dirname(__file__)
print('APACHE CONFIG DIRNAME: %s' % apache_configuration)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(apache_configuration)
sys.path.append(project)
sys.path.append(workspace)
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

