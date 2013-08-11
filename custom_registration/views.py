# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from grid.models import GridGroup
from custom_registration.models import UserProfile
from custom_registration.forms import CustomRegistrationForm
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from registration.signals import user_activated
from django.dispatch import receiver


# def register(request):
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             new_group = GridGroup(founder=new_user, name='My first grid')
#             new_group.save()
#             new_user_profile = UserProfile(user=new_user, default_grid=new_group)
#             new_user_profile.save()
#             new_user = authenticate(username=request.POST['username'],
#                                     password=request.POST['password1'])
#             login(request, new_user)
#             return HttpResponseRedirect("/grid/")
#         else:
#             template = loader.get_template('registration/login.html')
#             context = {
#                 'registration_error': True,
#                 'form':form,
#                 }
#             context.update(csrf(request))
#             return render_to_response('registration/login.html', context)
#     return HttpResponseRedirect("/login")

def wrongUrl(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/grid/")
    else:
        return HttpResponseRedirect("/login/")

@receiver(user_activated, dispatch_uid='nope')
def create(sender, user, request, **kwargs):
    print('IN CREATION OF NEW GRIDGROUP AND PROFILE')
    new_group, created = GridGroup.objects.get_or_create(founder=user, name='My first grid')
    new_user_profile, created2 = UserProfile.objects.get_or_create(user=user, default_grid=new_group)


#user_activated.connect(create, dispatch_uid="my_unique_string")