from grid.models import Review, Restaurant
from django.contrib.auth.models import User
from postcodes.models import Postcode
from django.contrib.gis.measure import Distance
from django.core.exceptions import ObjectDoesNotExist

class TableData:
	'Class that takes in queryset and returns altered object list for use in table'

	def __init__(self, filter):
		self.TableSet = self.organizeSet(filter)

	def getTableData(self):
		return self.TableSet

	def getUserSequence(self):
		return self.all_users

	def getRestaurantSequence(self):
		rest_list = []
		for rest in self.all_restaurants:
			rest_list.append(rest.name)
		return rest_list

	# returns two dimensional array of review objects
	def organizeSet(self, filter):
		print ('this is how i organize %s' % filter)
		if filter == None:
			self.all_restaurants = Restaurant.objects.all()
		elif self.isPostcode(filter):
			postcode_obj = None
			try:
				remove_underscore = filter.replace("_", " ")
				postcode_obj = Postcode.objects.get(name=remove_underscore)
			except ObjectDoesNotExist:
				remove_space = filter.replace("_", "")
				postcode_obj = Postcode.objects.get(name=remove_space)
			self.all_restaurants = Restaurant.objects.distance(
									postcode_obj.location, field_name='post_code__location').order_by('distance')
		else:
			print 'could not find filter'
			self.all_restaurants = Restaurant.objects.all()
		self.all_users = User.objects.all()
		table_list = []
		for restaurant in self.all_restaurants:
			restaurant_list = []
			for user in self.all_users:
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