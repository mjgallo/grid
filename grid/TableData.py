from grid.models import Review, Restaurant, GridGroup
from django.contrib.auth.models import User
from postcodes.models import Postcode
from django.contrib.gis.measure import Distance
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from itertools import chain

class TableData:
    'Class that takes in queryset and returns altered object list for use in table'

    def __init__(self, founder, sort=None, searchstring=None):
        self.postcode_found = False
        self.TableSet = self.organizeSet(founder, sort, searchstring)

    def getTableData(self):
        return self.TableSet

    def getMyUsers(self, group):
        return list(chain(group.members.all(), [group.founder]))

    def setAllRestaurants(self, group):
        """
        Collects list of all restaurants in grid and in any order specified
        """
        rest_dict = group.restaurantsTracked
        self.all_restaurants = rest_dict.all().distinct() #could perhaps do distinct here instead of above


    def sortAllRestaurants(self, sort):
        uppercase = sort.upper()
        postcode_obj = None
        try:
            remove_underscore = uppercase.replace("_", " ")
            postcode_obj = Postcode.objects.get(name=remove_underscore)
            self.all_restaurants = self.all_restaurants.distance(
                                postcode_obj.location, field_name='post_code__location').order_by('distance')
            self.postcode_found = True
        except ObjectDoesNotExist:
            remove_space = uppercase.replace("_", "")
            try:
                postcode_obj = Postcode.objects.get(name=remove_space)
                self.all_restaurants = self.all_restaurants.distance(
                                postcode_obj.location, field_name='post_code__location').order_by('distance')
                self.postcode_found = True
            except ObjectDoesNotExist:
                print 'bad filter'

    def filterSearch(self, group, searchstring):
        # tokenize search string
        searchstrings = searchstring.split()
        relevant_rests = []
        for search in searchstrings:
            relevant_reviews = Review.objects.filter(gridgroup=group, review__icontains=search)
            restaurants = Restaurant.objects.filter(name__icontains=search)
            for review in relevant_reviews:
                if review.restaurant not in relevant_rests:
                    relevant_rests.append(review.restaurant.pk)
            for restaurant in restaurants:
                if restaurant not in relevant_rests:
                    relevant_rests.append(restaurant.pk)
        self.all_restaurants = Restaurant.objects.filter(pk__in=relevant_rests)

    # returns two dimensional array of review objects
    def organizeSet(self, founder, sort, searchstring):
        """
        Main function. Organizes data and returns dictionary, ordered if
        necessary
        """
        print ('this is how i organize %s' % sort)
        group_list = []
        groups = GridGroup.objects.filter(Q(founder=founder)|Q(members=founder)).distinct()
        for group in groups.all():
            # get all restaurants in group
            self.setAllRestaurants(group)
            # pare down results to relevant
            if searchstring:
                self.filterSearch(group, searchstring)
            # sort all restaurants in group
            if sort:
                self.sortAllRestaurants(sort)
            table_list = []
            user_list = self.getMyUsers(group)
            for restaurant in self.all_restaurants:
                restaurant_list = []
                for user in user_list:
                    try:
                        review = Review.objects.get(restaurant=restaurant, reviewer=user, gridgroup=group)
                        restaurant_list.append({'review':review.review, 'id':review.id, 'restaurant':restaurant,'reviewer':user, 'good':review.good})
                    except Review.DoesNotExist:# if no review exists, just add reviewer so that box is editable
                        restaurant_list.append({'reviewer':user, 'restaurant':restaurant})
                table_list.append(restaurant_list)
            element_id = "grid" + str(group.id)
            link_id = "#" + element_id
            group_list.append({'request_queue':group.request_queue.all(), 'founder': group.founder.username, 'name':group.name, 'id':group.id, 'data':table_list, 'users':user_list, 'element_id':element_id, 'link_id':link_id})
        return group_list