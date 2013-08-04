from django.db import models
from django.contrib.auth.models import User
from grid.models import Review, Restaurant, GridGroup

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	default_grid = models.ForeignKey(GridGroup)
	approval_queue = models.ManyToManyField(GridGroup, related_name='invited_to')