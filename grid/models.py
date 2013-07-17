from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from postcodes.models import Postcode

# Create your models here.

class Restaurant(geomodels.Model):
	name = geomodels.CharField(max_length=150)
	address = geomodels.CharField(max_length=100)
	post_code = geomodels.ForeignKey(Postcode)

	objects = geomodels.GeoManager()



	def __unicode__(self):
		return self.name

class Review(geomodels.Model):
	restaurant = geomodels.ForeignKey(Restaurant)
	review = geomodels.CharField(max_length=160)
	good = geomodels.BooleanField()
	reviewer = geomodels.ForeignKey(User, null=True)

	def __unicode__(self):
		return self.review + ' by ' + self.reviewer.username

