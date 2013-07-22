# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from grid.models import GridGroup

def register(request):
    if request.method == 'POST':
    	print 'in post'
    	print request.POST
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_group = GridGroup(founder=new_user)
            new_group.save()
            print 'new user is saving'
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)

            return HttpResponseRedirect("/grid/")
    else:
        form = UserCreationForm()
    return HttpResponseRedirect("/login/")