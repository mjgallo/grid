# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from grid.models import GridGroup
from custom_registration.forms import CustomRegistrationForm
from django.template import RequestContext, loader


def register(request):
    if request.method == 'POST':
    	print 'in post'
    	print request.POST
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            print 'form valid'
            new_user = form.save()
            new_group = GridGroup(founder=new_user)
            new_group.save()
            print 'new user is saving'
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)

            return HttpResponseRedirect("/grid/")
        else:
            template = loader.get_template('registration/login.html')
            context = RequestContext(request, {
                'registration_error': True,
                'form':form,
                })
            return HttpResponse(template.render(context))
    return HttpResponseRedirect("/login")