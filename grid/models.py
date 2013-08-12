from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from postcodes.models import Postcode

# Create your models here.

class Restaurant(geomodels.Model):
	PRICES = [(i, i) for i in range(5)]
	name = geomodels.CharField(max_length=150)
	address = geomodels.CharField(max_length=100)
	post_code = geomodels.ForeignKey(Postcode, null=True)
	users_interested = models.ManyToManyField(User)
	telephone = models.CharField(max_length=20, null=True, blank=True)
	website = models.URLField(null=True, blank=True)
	price = models.IntegerField(null=True, blank=True, choices=PRICES)

	objects = geomodels.GeoManager()

	def __unicode__(self):
		return self.name

class Review(geomodels.Model):
	restaurant = geomodels.ForeignKey(Restaurant)
	review = geomodels.CharField(max_length=160)
	good = geomodels.BooleanField()
	reviewer = geomodels.ForeignKey(User, null=True)
	last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
	gridgroup = geomodels.ForeignKey('GridGroup', related_name='grid_group_association')

	def __unicode__(self):
		return self.review + ' by ' + self.reviewer.username

class GridGroup(geomodels.Model):
	name = models.CharField(max_length=50)
	private = models.BooleanField(default=True)
	founder = models.ForeignKey(User, related_name='grid_group_owner')
	members = models.ManyToManyField(User, blank=True, null=True, related_name="current_members")
	restaurantsTracked = models.ManyToManyField(Restaurant, blank=True, null=True)
	request_queue = models.ManyToManyField(User, blank=True, null=True, related_name="pending_requests")

	def __unicode__(self):
		return self.founder.username
