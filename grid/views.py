# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from grid.models import Review, Restaurant, GridGroup
from grid.TableData import TableData
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django_tables2 import RequestConfig
from grid.tables import RestaurantTable
from postcodes.models import Postcode
import string
import json

def detail(request, filter=None):
    if request.user.is_authenticated():
        group = GridGroup.objects.get(founder=request.user)
        reviewers = group.members.order_by('username')
        table = TableData(request.user, filter)
        table_data = table.getTableData()
        all_users = table.getMyUsers(request.user)
        all_restaurants = table.getRestaurantSequence()
        template = loader.get_template('grid/details.html')
        print 'length of table  data'
        print(len(table_data))
        print(table_data)
        context = RequestContext(request, {
            'all_users': all_users,
            'table_data':table_data,
            'all_restaurants': all_restaurants,
            'this_user': request.user
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('User is not authenticated to view grid')


def update(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            this_review = None
            new_review = None
            good=None
            try:
                for key, value in request.POST.iteritems():
                    print (key + ' ' + value)
                div_id = int(request.POST['name'])
                try: 
                    this_review = Review.objects.get(pk=div_id)
                except (KeyError, Review.DoesNotExist):
                    print 'Review for some reason does not exist'
                new_review = request.POST['value']
                good = True if request.POST['good']=='good' else False
                this_review.review = new_review
                this_review.good=good
                this_review.save()
            except (ValueError): #no review yet, div_id is 'user_id-restaurant_id'
                ident_list = string.split(request.POST['name'], '-')
                good = True if request.POST['good']=='good' else False                
                rest_updated = Restaurant.objects.get(pk=int(ident_list[1]))
                print ident_list
                new_review_object = Review(restaurant=rest_updated,
                                        review=request.POST['value'],
                                        good=good,
                                        reviewer=User.objects.get(pk=int(ident_list[0])),
                                        )
                rest_updated.users_interested.add(request.user.pk)
                new_review_object.save()
                new_review = new_review_object.review
            return HttpResponse(new_review)
        return HttpResponse('Did not use POST method')
    else:
        return HttpResponse('User is not authenticated to update')

def sort(request):
    print 'here0'
    if request.user.is_authenticated():
        print 'here1'
        postcode=None
        if request.method=='POST':
            print 'here2'
            postcode = request.POST['value']
            postcode = postcode.replace(" ", "_")
        else:
            print 'Didnt say anything'
        return HttpResponseRedirect(reverse('grid:detail', kwargs={'filter':postcode}))
    else:
        return HttpResponse('not logged in')

def newRestaurant(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                print key
                rest_dict = json.loads(key)
                print rest_dict           
            rest_name = rest_dict['name']
            address = rest_dict['address']
            post_code = rest_dict['postcode']
            post_obj = None
            try:
                post_obj = Postcode.objects.get(name=post_code)
            except (KeyError, Postcode.DoesNotExist):
                no_spaces = post_code.replace(" ", "")
                try:
                    post_obj = Postcode.objects.get(name=no_spaces)
                except (KeyError, Postcode.DoesNotExist):
                    HttpResponse('Postcode not in system')
            rest_obj = None
            try: #see if restaurant is already in database for some reason
                rest_obj = Restaurant.objects.get(name=rest_name, address=address, post_code=post_obj)
            except (KeyError, Restaurant.DoesNotExist):
                rest_obj = Restaurant(name=rest_name, address=address, post_code=post_obj)
                rest_obj.save()
            rest_obj.users_interested.add(request.user.pk)
            return HttpResponse(json.dumps(rest_dict))
        return HttpResponse('Did not use POST method')
    else:
        return HttpResponse('User is not authenticated to update')
