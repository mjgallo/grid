from django.conf.urls import patterns, url

from custom_registration import views

urlpatterns = patterns('', 
	url(r'^$', views.register, name='register'),
)
