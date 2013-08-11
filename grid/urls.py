from django.conf.urls import patterns, url

from grid import views
from custom_registration import views as reg_views

urlpatterns = patterns('', 
	url(r'^$', views.detail, name='detailnofilter'),
	url(r'^update/$', views.update, name='update'),
	url(r'^remove_user/$', views.remove_user, name='remove_user'),
	url(r'^sort/$', views.sort, name='sort'),
	url(r'^find_users/$', views.find_users, name='find_users'),
	url(r'^add_friend/$', views.add_friend, name='add_friend'),
	url(r'^add_restaurant/$', views.newRestaurant, name='restaurant'),
	url(r'^create_grid/$', views.creategrid, name='creategrid'),
	url(r'^update_grid/$', views.updategrid, name='updategrid'),
	url(r'^approve_grid/$', views.approvegrid, name='approvegrid'),
	url(r'^find_grid/$', views.find_grid, name='find_grid'),
	url(r'^request_grid/$', views.request_grid, name='request_grid'),
	url(r'^approve_request/$', views.approve_request, name='approve_request'),
	url(r'^invite_user/$', views.invite_user, name='invite_user'),
	url(r'^(?P<filter>\w+)/$', views.detail, name='detail'),
    url(r'^.*/$', reg_views.wrongUrl, name='wrongUrl'),
)

