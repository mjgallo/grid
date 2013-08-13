from django.conf.urls import patterns, url

from notification.views import confirm

urlpatterns = patterns('', 
	url(r'^confirm/(?P<notification_key>\w+)/$', confirm, name='notification_confirm'),
)
