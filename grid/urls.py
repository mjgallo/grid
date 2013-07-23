from django.conf.urls import patterns, url

from grid import views

urlpatterns = patterns('', 
	url(r'^$', views.detail, name='detailnofilter'),
	url(r'^update/$', views.update, name='update'),
	url(r'^remove_user/$', views.remove_user, name='remove_user'),
	url(r'^sort/$', views.sort, name='sort'),
	url(r'^find_users/$', views.find_users, name='find_users'),
	url(r'^add_friend/$', views.add_friend, name='add_friend'),
	url(r'^add_restaurant/$', views.newRestaurant, name='restaurant'),
	url(r'^(?P<filter>\w+)/$', views.detail, name='detail'),
)

