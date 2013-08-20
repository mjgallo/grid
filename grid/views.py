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
from django.core.mail import send_mail
from custom_registration.models import UserProfile
from grid import signals
import string
import json
from django.db.models import Q


def find_grid(request):
    """
    A user searches for potential grids to join. Handles both search
    terms and non search term requests.
    """
    if request.user.is_authenticated():
        group_list=[]
        group_queryset=None
        data = None
        for key, value in request.GET.iteritems():
            data = json.loads(key)
        try:
            group_queryset = GridGroup.objects.filter(Q(founder__username__icontains=data['search-string'])|
                        Q(name__icontains=data['search-string'])).exclude(
                        members=request.user).exclude(founder=request.user).exclude(
                        request_queue=request.user)
        except:
            group_queryset = GridGroup.objects.all().exclude(members=request.user).exclude(founder=request.user).exclude(request_queue=request.user)
        for group in group_queryset:
            group_list.append({'id':group.id, 'founder': group.founder.username, 'name': group.name, 
                'count': (group.members.count()+1), 'restaurants':group.restaurantsTracked.count(), 'reviews':Review.objects.filter(gridgroup=group).count()})
        return HttpResponse(json.dumps(list(group_list)))

def request_grid(request):
    """
    A user requests that a founder allow him in the founder's grid. If founder
    has already invited user to grid, user is added automatically. Otherwise,
    user is placed into approval_queue and an email is sent to founder.
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            response = None
            for key, value in request.POST.iteritems():
                response = json.loads(key)
            grid = GridGroup.objects.get(pk=response['id'])
            if not UserProfile.objects.get(user=request.user).approval_queue.filter(pk=grid.pk):
                signals.grid_requested.send(sender='request_grid',
                                            to_founder=grid.founder,
                                            grid=grid,
                                            request=request)
                grid.request_queue.add(request.user.pk)
            else: 
                UserProfile.objects.get(user=request.user).approval_queue.remove(grid.pk)
                grid.members.add(request.user.pk)
            return HttpResponse(json.dumps({'success':True, 'username':grid.founder.username, 'gridname':grid.name}))

def remove_grid(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            posted = json.loads(request.body)
            grid = GridGroup.objects.get(pk=int(posted['grid']))
            if grid.founder==request.user:
                if grid==UserProfile.objects.get(user=request.user).default_grid:
                    return HttpResponse(json.dumps({'success':False, 'msg':'cannot delete first grid'}))
                else:
                    grid.delete()
            else:
                grid.members.remove(request.user.pk)
    return HttpResponse(json.dumps({'success':True}))


def approve_request(request):
    """
    A founder approves a user's request to join a grid
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            grid = GridGroup.objects.get(pk=int(rest_dict['grid']))
            grid.members.add(int(rest_dict['approved_id']))
            grid.request_queue.remove(int(rest_dict['approved_id']))
            grid.save()
            return HttpResponse(json.dumps({'success':True}))

def find_users(request):
    """
    The view called when a grid founder searches for more users to add
    to his grid. Called in both cases: when a search string is supplied
    to narrow the table down -- or when no search is provided and all 
    users not currently in the grid or invited to the grid are displayed
    """
    if request.user.is_authenticated():
        display_users = None
        group_dict = []
        for key, value in request.GET.iteritems():
            group_dict = json.loads(key)
        group = GridGroup.objects.get(pk=int(group_dict['group']))
        data = None
        for key, value in request.GET.iteritems():
            data = json.loads(key)
        try: #this is used if a search string is provided
            users = User.objects.filter(Q(username__icontains=data['search-string'])|
                        Q(first_name__icontains=data['search-string'])|
                        Q(last_name__icontains=data['search-string'])).exclude(
                        pk__in=group.members.all().values_list(
                        'pk', flat=True)).exclude(pk=request.user.pk).exclude(is_staff=True)
        except: #DEFAULTS here, no search string provided
            users = User.objects.exclude(
                        pk__in=group.members.all().values_list(
                        'pk', flat=True)).exclude(pk=request.user.pk).exclude(is_staff=True)
        display_users = users.all().values('username', 'id', 'first_name', 'last_name')
        return HttpResponse(json.dumps(list(display_users)))

def invite_user(request):
    """
    Out of service
    """

    if request.user.is_authenticated():
        group_dict = []
        for key, value in request.POST.iteritems():
            group_dict = json.loads(key)
        return HttpResponse(json.dumps({'success':True}))    

def remove_user(request):
    """
    Out of service
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            gridgroup = GridGroup.objects.get(pk=int(rest_dict['group']))
            gridgroup.members.remove(rest_dict['removed_id'])
        else:
            print 'no POST'
        return HttpResponse(json.dumps({'success':True}))
    return HttpResponse(json.dumps({'success':False}))

def remove_restaurant(request):
    """
    Founder of grid clicks on x in grid and the restaurant is removed from
    the restuarantsTracked field. The associated reviews are NOT deleted. If
    the restaurant is re-added all associated reviews are 
    automatically reinstituted
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            gridgroup = GridGroup.objects.get(pk=int(rest_dict['group']))
            gridgroup.restaurantsTracked.remove(rest_dict['removed_id'])
            gridgroup.save()
        else:
            print 'no POST'
        return HttpResponse(json.dumps({'success':True}))
    return HttpResponse(json.dumps({'success':False}))


def add_friend(request):
    """
    A founder of a grid requests that another user join the grid. If 
    the requested user has himself already requested access to the grid,
    then the user is added automatically.
    Otherwise, the grid is placed in the invited user's approval_queue
    and an email notification is sent.
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            new_friend = User.objects.get(pk=rest_dict['id'])
            new_friend_profile = UserProfile.objects.get(user=new_friend)
            gridgroup = GridGroup.objects.get(pk=int(rest_dict['group']))
            if not gridgroup.request_queue.filter(pk=new_friend.pk):
                signals.user_invited.send(sender='add_friend',
                                            to_user=new_friend,
                                            grid=gridgroup,
                                            request=request)
                new_friend_profile.approval_queue.add(gridgroup)
            else:
                gridgroup.members.add(new_friend.pk)
                gridgroup.request_queue.remove(new_friend.pk)
            return HttpResponse(json.dumps({'success':True, 'name':new_friend.username}))
        else:
            return HttpResponse(json.dumps({'success':False}))

def detail(request):
    """
    The main view that handles the organizing and loading of the 
    user's grid data into the details template. 
    """
    if request.user.is_authenticated():
        postcode = searches = sort = None
        request_dict = {'filtername':'', 'searchgridparams':''}
        if request.GET:
            request_dict = request.GET.dict()
        user_profile = UserProfile.objects.get(user=request.user)
        group = user_profile.default_grid
        groups = GridGroup.objects.filter(Q(founder=request.user)|Q(members=request.user))
        table = TableData(request.user, sort=request_dict['filtername'], searchstring=request_dict['searchgridparams'])
        table_data = table.getTableData()
        if len(request_dict['filtername']) > 0: # test to see if page submitted a value here
            if not table.postcode_found:
                message = "Could not find postal code " + request_dict['filtername'].upper()
                postcode = None
                sort = {'message':message, 'postcode':postcode}
            else:
                message = "Sorting on " + request_dict['filtername'].upper()
                postcode = request_dict['filtername'].upper().replace(' ', '_')
                sort = {'message':message, 'postcode':postcode}
        if len(request_dict['searchgridparams']) > 0: # test to see if page submitted a value here
            message = "Filtering on '" + request_dict['searchgridparams']+"'"
            terms = request_dict['searchgridparams']
            searches = {'message':message, 'terms':terms}
        template = loader.get_template('grid/details.html')
        context = RequestContext(request, {
            'default_group': group,
            'sort': sort,
            'searches': searches,
            'groups': groups,
            'approval_queue': user_profile.approval_queue.all(),
            'table_data':table_data,
            'this_user': request.user
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/login/')


def update(request):
    """
    User creates or edits a review
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            this_review = None
            new_review = None
            user_rest_string = None
            good=None
            ident_list = string.split(request.POST['name'], '-')
            rest_updated = Restaurant.objects.get(pk=int(ident_list[1]))
            grid_updated = GridGroup.objects.get(pk=int(ident_list[0])) 
            good = True if request.POST['good']=='good' else False
            try:
                this_review = Review.objects.get(restaurant=rest_updated,
                                                reviewer=request.user,
                                                gridgroup=grid_updated,)
            except(KeyError, Review.DoesNotExist):
                this_review = Review(restaurant=rest_updated,
                                        review=request.POST['value'],
                                        good=good,
                                        reviewer=request.user,
                                        gridgroup=grid_updated,
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

def rest_manual_add(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rest_dict = None
            for key, value in request.POST.iteritems():
                rest_dict = json.loads(key)
            grid = GridGroup.objects.get(pk=int(rest_dict['grid']))
            new_rest = Restaurant(name=rest_dict['name'])
            new_rest.save()
            grid.restaurantsTracked.add(new_rest.pk)
            new_rest.users_interested.add(request.user.pk)
            return HttpResponse(json.dumps({'success':True}))

def newRestaurant(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            # Organize POST JSON dictionary coming from website
            rest_dict = None
            website = None
            phone = None
            price = None
            for key, value in request.POST.iteritems():
                print('the key is %s' % key)
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
            try:
                price = int(rest_dict['price'])
            except KeyError:
                print('price not available')
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
            # Now handle server-side manipulation of info from website
            try: #see if restaurant is already in database for some reason
                rest_obj = Restaurant.objects.get(name=rest_name, address=address, post_code=post_obj)
            except (KeyError, Restaurant.DoesNotExist):
                rest_obj = Restaurant(name=rest_name, address=address, post_code=post_obj, telephone=phone, website=website, price=price)
                rest_obj.save()
            rest_obj.users_interested.add(request.user.pk)
            grid = GridGroup.objects.get(pk=int(rest_dict['group']))
            grid.restaurantsTracked.add(rest_obj.pk)
            return HttpResponse(json.dumps(rest_dict))
        return HttpResponse('Did not use POST method')
    else:
        return HttpResponseRedirect('/login/')

def creategrid(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            new_grid = GridGroup(founder=request.user, private=request.POST['private'], name=request.POST['name'])
            new_grid.save()
            return HttpResponseRedirect('/grid/')
    else:
        return HttpResponseRedirect('/login/')

def updategrid(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            request_dict = []
            for key, value in request.POST.iteritems():
                request_dict = json.loads(key)
            print request_dict
            grid = GridGroup.objects.get(pk=int(request_dict['id']))
            print request_dict['name']
            grid.name = request_dict['name']
            grid.save()
            return HttpResponse(json.dumps({'success':True}))

def approvegrid(request):
    """
    A user consents to a founder's invitation to be included in the founder's
    grid
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            request_dict = []
            for key, value in request.POST.iteritems():
                request_dict = json.loads(key)
            grid = GridGroup.objects.get(pk=int(request_dict['approved_id']))
            grid.members.add(request.user.pk)
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.approval_queue.remove(grid.pk)
            return HttpResponse(json.dumps({'success':True}))
    else:
        return HttpResponseRedirect('/login/')            

def update_account(request):
    if request.user.is_authenticated():
        print 'user authenticated'
        if request.method == 'POST':
            try:
                request.user.first_name = request.POST['firstname']
            except KeyError:
                print 'no first name'
            try:
                request.user.last_name = request.POST['lastname']
            except KeyError:
                print 'no last name'
            request.user.save()
            return HttpResponse(json.dumps({'success':True, 'firstname':request.user.first_name, 'lastname':request.user.last_name}))
    return HttpResponse(json.dumps({'success':False}))


