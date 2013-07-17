from django.contrib.gis.db import models

# Create your models here.
class Postcode(models.Model):
	name = models.CharField(max_length=8, db_index=True)
	location = models.PointField()

	objects = models.GeoManager()

	def __unicode__(self):
		return self.name