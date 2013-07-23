from grid.models import Review, Restaurant, GridGroup
from django.contrib.auth.models import User
from postcodes.models import Postcode
from django.contrib.gis.measure import Distance
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from itertools import chain

class TableData:
	'Class that takes in queryset and returns altered object list for use in table'

	def __init__(self, founder, filter):
		self.TableSet = self.organizeSet(founder, filter)
		self.all_users = self.getMyUsers(founder)

	def getTableData(self):
		return self.TableSet

	def getMyUsers(self, founder):
		gridgroup = GridGroup.objects.get(founder=founder)
		return list(chain(gridgroup.members.all(), [founder]))

	def setAllRestaurants(self, founder, filter):
		rest_dict = Restaurant.objects.filter(Q(users_interested__in=self.getMyUsers(founder))|Q(users_interested=founder)).distinct()
		self.all_restaurants = rest_dict.all() #could perhaps do distinct here instead of above
		if filter != None:
			uppercase = filter.upper()
			postcode_obj = None
			try:
				remove_underscore = uppercase.replace("_", " ")
				postcode_obj = Postcode.objects.get(name=remove_underscore)
				self.all_restaurants = self.all_restaurants.distance(
									postcode_obj.location, field_name='post_code__location').order_by('distance')
			except ObjectDoesNotExist:
				remove_space = uppercase.replace("_", "")
				try:
					postcode_obj = Postcode.objects.get(name=remove_space)
					self.all_restaurants = self.all_restaurants.distance(
									postcode_obj.location, field_name='post_code__location').order_by('distance')
				except ObjectDoesNotExist:
					print 'bad filter'

	def getRestaurantSequence(self):
		self.rest_list = []
		for rest in self.all_restaurants:
			self.rest_list.append(rest.name)
		return self.rest_list

	# returns two dimensional array of review objects
	def organizeSet(self, founder, filter):
		print ('this is how i organize %s' % filter)
		self.setAllRestaurants(founder, filter)
		table_list = []
		for restaurant in self.all_restaurants:
			restaurant_list = []
			for user in self.getMyUsers(founder):
				try:
				    review = Review.objects.get(restaurant=restaurant, reviewer=user)
				    restaurant_list.append({'review':review.review, 'id':review.id, 'restaurant':restaurant,'reviewer':user, 'good':review.good})
				except Review.DoesNotExist:# if no review exists, just add reviewer so that box is editable
					restaurant_list.append({'reviewer':user, 'restaurant':restaurant})
			table_list.append(restaurant_list)
		return table_list

	def isPostcode(self, filter):
		if len(filter)==8 or len(filter)==7 or len(filter)==6:
			return True