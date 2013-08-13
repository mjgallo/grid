from notification.models import NotificationKey
from django.dispatch import receiver
from custom_registration.models import UserProfile
from grid.signals import user_invited
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response


is_key_valid = NotificationKey.objects.is_key_valid
# Create your views here.
@receiver(user_invited, dispatch_uid='user_invited')
def invite(sender, to_user, grid, request, **kwargs):
    notification = NotificationKey.objects.create_notification(to_user, grid, request.user)
    notification.send_to(to_user.email)

def confirm(request, notification_key=None):
    if notification_key and is_key_valid(notification_key):
    	notification_object = is_key_valid(notification_key)
    	to_user = notification_object.to_user
    	from_user = notification_object.from_user
    	user_profile = UserProfile.objects.get(user=to_user)
    	grid = notification_object.gridgroup
    	grid.members.add(to_user.pk)
    	user_profile.approval_queue.remove(grid.pk)
        return render_to_response('notification/success.html', {'to_user':to_user, 'from_user': from_user, 'grid':grid})
    else:
        return render_to_response('notification/failure.html', {'to_user':to_user, 'from_user': from_user, 'grid':grid})

