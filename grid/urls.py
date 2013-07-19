from django.conf.urls import patterns, url

from grid import views

urlpatterns = patterns('', 
	url(r'^$', views.detail, name='detailnofilter'),
	url(r'^update/$', views.update, name='update'),
	url(r'^sort/$', views.sort, name='sort'),
	url(r'^add_restaurant/$', views.newRestaurant, name='restaurant'),
	url(r'^(?P<filter>\w+)/$', views.detail, name='detail'),
)

