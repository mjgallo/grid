from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from custom_registration import views as reg_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grid/', include('grid.urls', namespace="grid")),
#    url(r'^register/', include('custom_registration.urls', namespace="custom_registration")),
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page':'/login/'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^invite/', include('invite.urls', namespace='invite')),
    url(r'^.*$', reg_views.wrongUrl, name='wrongUrl'),

)
