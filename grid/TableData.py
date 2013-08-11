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

    def getTableData(self):
        return self.TableSet

    def getMyUsers(self, group):
        return list(chain(group.members.all(), [group.founder]))

    def setAllRestaurants(self, group, filter):
        rest_dict = group.restaurantsTracked
        self.all_restaurants = rest_dict.all().distinct() #could perhaps do distinct here instead of above
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
        group_list = []
        groups = GridGroup.objects.filter(Q(founder=founder)|Q(members=founder)).distinct()
        for group in groups.all():
            self.setAllRestaurants(group, filter)
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

    def isPostcode(self, filter):
        if len(filter)==8 or len(filter)==7 or len(filter)==6:
            return True