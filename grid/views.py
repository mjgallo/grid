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
from django.db.models import Q

def find_users(request):
    if request.user.is_authenticated():
        display_users = None
        group = GridGroup.objects.get(founder=request.user)
        data = None
        for key, value in request.GET.iteritems():
            data = json.loads(key)
        try:
            users = User.objects.filter(Q(username__icontains=data['search-string'])|
                        Q(first_name__icontains=data['search-string'])|
                        Q(last_name__icontains=data['search-string'])).exclude(
                        pk__in=group.members.all().values_list(
                        'pk', flat=True)).exclude(pk=request.user.pk)
        except:
            users = User.objects.exclude(
                        pk__in=group.members.all().values_list(
                        'pk', flat=True)).exclude(pk=request.user.pk)
        display_users = users.all().values('username', 'id', 'first_name', 'last_name')
        return HttpResponse(json.dumps(list(display_users)))

def remove_user(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            gridgroup = GridGroup.objects.get(founder=request.user)
            gridgroup.members.remove(rest_dict['removed_id'])
        else:
            print 'no POST'
        return HttpResponse(json.dumps({'success':True}))
    return HttpResponse(json.dumps({'success':False}))

def add_friend(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            new_friend = User.objects.get(pk=rest_dict['id'])
            gridgroup = GridGroup.objects.get(founder=request.user)
            gridgroup.members.add(new_friend)
            print rest_dict
        return HttpResponse(json.dumps({'success':True}))


def detail(request, filter=None):
    if request.user.is_authenticated():
        group = GridGroup.objects.get(founder=request.user)
        reviewers = group.members.order_by('username')
        table = TableData(request.user, filter)
        table_data = table.getTableData()
        all_users = table.getMyUsers(request.user)
        all_restaurants = table.getRestaurantSequence()
        template = loader.get_template('grid/details.html')
        context = RequestContext(request, {
            'all_users': all_users,
            'table_data':table_data,
            'all_restaurants': all_restaurants,
            'this_user': request.user
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/login/')


def update(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            this_review = None
            new_review = None
            user_rest_string = None
            good=None
            ident_list = string.split(request.POST['name'], '-')
            rest_updated = Restaurant.objects.get(pk=int(ident_list[1])) 
            good = True if request.POST['good']=='good' else False
            try:
                this_review = Review.objects.get(restaurant=rest_updated,
                                                reviewer=request.user)
            except(KeyError, Review.DoesNotExist):
                this_review = Review(restaurant=rest_updated,
                                        review=request.POST['value'],
                                        good=good,
                                        reviewer=request.user,
                                        )
            this_review.good = good
            this_review.review = request.POST['value']
            this_review.save()
            new_review = this_review.review
            return HttpResponse(json.dumps({'new_review':new_review}))
        return HttpResponse('Did not use POST method')
    else:
        return HttpResponseRedirect('/login/')

def sort(request):
    if request.user.is_authenticated():
        postcode=None
        if request.method=='POST':
            postcode = request.POST['filtername']
            postcode = postcode.replace(" ", "_")
        else:
            print 'Didnt say anything'
        return HttpResponseRedirect(reverse('grid:detail', kwargs={'filter':postcode}))
    else:
        return HttpResponseRedirect('/login/')

def newRestaurant(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            website = None
            phone = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            rest_name = rest_dict['name']
            address = rest_dict['address']
            try:
                phone = rest_dict['phone']
            except KeyError:
                print('phone not available')
            try:
                website = rest_dict['website']
            except KeyError:
                print('website not available')
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
                rest_obj = Restaurant(name=rest_name, address=address, post_code=post_obj, telephone=phone, website=website)
                rest_obj.save()
            rest_obj.users_interested.add(request.user.pk)
            return HttpResponse(json.dumps(rest_dict))
        return HttpResponse('Did not use POST method')
    else:
        return HttpResponseRedirect('/login/')
