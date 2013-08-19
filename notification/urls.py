from django.conf.urls import patterns, url

from notification.views import confirm, accept

urlpatterns = patterns('', 
	url(r'^confirm/(?P<notification_key>\w+)/$', confirm, name='notification_confirm'),
	url(r'^accept/(?P<notification_key>\w+)/$', accept, name='request_accept'),
)
