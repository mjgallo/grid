from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from registration import signals
import json
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from custom_registration.models import UserProfile
from grid.models import GridGroup

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm

from invite.models import InvitationKey
from invite.forms import InvitationKeyForm

is_key_valid = InvitationKey.objects.is_key_valid
return_grid = InvitationKey.objects.return_grid
return_email = InvitationKey.objects.return_email
return_user = InvitationKey.objects.return_user
establish_user_profile = InvitationKey.objects.establish_user_profile


# displays registration form
def invited(request, invitation_key=None):
    if invitation_key and is_key_valid(invitation_key):
        template = 'invitation/invited.html'
        return render_to_response(template, {'form': RegistrationForm, 'invitation_key': invitation_key, 'email':return_email(invitation_key)})
    else:
        return HttpResponseRedirect('/accounts/register/')

def register(request, success_url=None,
            form_class=RegistrationForm, profile_callback=None,
            template_name='registration/registration_form.html',
            extra_context=None):
    if 'invitation_key' in request.REQUEST \
        and is_key_valid(request.REQUEST['invitation_key']):
        if extra_context is None:
            extra_context = {'invitation_key': request.REQUEST['invitation_key'], 'grid':return_grid(request.REQUEST['invitation_key'])}
        else:
            extra_context.update({'invitation_key': request.REQUEST['invitation_key'], 'grid':return_grid(request.REQUEST['invitation_key']), 'email':return_email(request.REQUEST['invitation_key'])})
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user, invited_grid = establish_user_profile(request.REQUEST['invitation_key'], cd['username'], cd['password1'])
            new_user = authenticate(username=new_user.username, password=cd['password1'])
            login(request, new_user)
            return render_to_response('invitation/success.html', {'user': return_user(request.REQUEST['invitation_key']), 'grid':invited_grid.name})
        else:
            return render_to_response('invitation/invited.html', {'form': form, 'invitation_key': request.REQUEST['invitation_key'], 'email':return_email(request.REQUEST['invitation_key'])})
    else:
        return HttpResponseRedirect('/accounts/register/')

def invite(request, success_url=None,
            form_class=InvitationKeyForm,
            template_name='invitation/invitation_form.html',):
    if request.method == 'POST':
        response = None
        for key, value in request.POST.iteritems():
            response = json.loads(key)
        form = form_class(data=response)
        if form.is_valid():
            print('in form is valid')
            invitation = InvitationKey.objects.create_invitation(request.user, form.cleaned_data['grid'], form.cleaned_data['email'])
            invitation.send_to(form.cleaned_data["email"])
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponse(json.dumps({'success':True}))
    else:
        form = form_class()
    return HttpResponse('failure')
invite = login_required(invite)
