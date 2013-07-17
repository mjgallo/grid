# load some initial data
from postcodes.models import Postcode
from grid.models import Restaurant, Review
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
# First create a couple restaurants

class Command(BaseCommand):
	def handle(self, *args, **options):
		name1 = 'GBK'
		postcode1 = 'E1 1HD'
		address1 = '10 Something Way'
		post1=None
		try:
			post1 = Postcode.objects.get(name=postcode1)
		except(DoesNotExist):
			remove_space = postcode1.replace(" ", "")
			post1 = Postcode.objects.get(name=remove_space)

		rest1 = Restaurant(name=name1, address=address1, post_code=post1)
		rest1.save()

		name2 = 'Hawksmoor - Spitalfields'
		postcode2 = 'E1 6BJ'
		address2 = '157a Commercial Street'
		post2=None
		try:
			post2 = Postcode.objects.get(name=postcode2)
		except(ObjectDoesNotExist):
			remove_space = postcode2.replace(" ", "")
			post2 = Postcode.objects.get(name=remove_space)

		rest2 = Restaurant(name=name2, address=address2, post_code=post2)
		rest2.save()

		name3 = 'Davys Wine Bar'
		postcode3 = 'SW1Y 6QY'
		address3 = 'Crown Passage'
		post3=None
		try:
			post3 = Postcode.objects.get(name=postcode3)
		except(ObjectDoesNotExist):
			remove_space = postcode3.replace(" ", "")
			post3 = Postcode.objects.get(name=remove_space)

		rest3 = Restaurant(name=name3, address=address3, post_code=post3)
		rest3.save()

		# Then a couple more users
		user1 = User.objects.create_user(username="john2", email="", password="marines")
		user1.save()

		user2 = User.objects.create_user(username="bill2", email="", password="marines")
		user2.save()

		# and finally review
		review1 = "Hawksmoore is pretty good"

		review_obj1 = Review(restaurant=rest2, review=review1, good=True, reviewer=user1)
		review_obj1.save()

		review2 = "Cool understated place in posh area"
		review_obj2 = Review(restaurant=rest3, review=review2, good=True, reviewer=user2)
		review_obj2.save()


