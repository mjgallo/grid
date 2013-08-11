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


# displays registration form
def invited(request, invitation_key=None):
    if invitation_key and is_key_valid(invitation_key):
        template = 'invitation/invited.html'
    else:
        template = 'invitation/wrong_invitation_key.html'
    return render_to_response(template, {'form': RegistrationForm, 'invitation_key': invitation_key, 'email':return_email(invitation_key)})

def register(request, success_url=None,
            form_class=RegistrationForm, profile_callback=None,
            template_name='registration/registration_form.html',
            extra_context=None):
    if 'invitation_key' in request.REQUEST \
        and is_key_valid(request.REQUEST['invitation_key']):
        if extra_context is None:
            extra_context = {'invitation_key': request.REQUEST['invitation_key'], 'grid':return_grid(request.REQUEST['invitation_key'])}
        else:
            extra_context.update({'invitation_key': invitation_key, 'grid':return_grid(request.REQUEST['invitation_key']), 'email':return_email(request.REQUEST['invitation_key'])})
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            new_group, created = GridGroup.objects.get_or_create(founder=new_user, name='My first grid')
            new_user_profile, created2 = UserProfile.objects.get_or_create(user=new_user, default_grid=new_group)
            new_user_profile.approval_queue.add(return_grid(request.REQUEST['invitation_key']))
            new_user = authenticate(username=new_user.username)
            login(request, new_user)
            return HttpResponseRedirect('/grid/')
        else:
            return render_to_response('invitation/invited.html', {'form': form, 'invitation_key': invitation_key, 'email':return_email(request.REQUEST['invitation_key'])})
    else:
        return HttpResponse('not valid key')

def invite(request, success_url=None,
            form_class=InvitationKeyForm,
            template_name='invitation/invitation_form.html',):
    if request.method == 'POST':
        response = None
        for key, value in request.POST.iteritems():
            response = json.loads(key)
        form = form_class(data=response)
        if form.is_valid():
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
