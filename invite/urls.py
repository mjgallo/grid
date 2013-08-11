from django.conf.urls import patterns, url

from invite.views import register, invite, invited

urlpatterns = patterns('', 
	url(r'^send/$', invite, name='invitation_invite'),
    url(r'^invited/(?P<invitation_key>\w+)/$', 
                invited,
                name='invitation_invited'),
    url(r'^register/$',
                register,
                name='registration_register'),
)
