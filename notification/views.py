from notification.models import NotificationKey
from django.dispatch import receiver
from custom_registration.models import UserProfile
from grid.signals import user_invited, grid_requested
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response


is_key_valid = NotificationKey.objects.is_key_valid
# Create your views here.
@receiver(user_invited, dispatch_uid='user_invited')
def invite(sender, to_user, grid, request, **kwargs):
    """
    Founder invites user to join grid
    """
    user_profile = UserProfile.objects.get(user=to_user)
    if not user_profile.approval_queue.filter(pk=grid.pk):
        print('sending')
        notification = NotificationKey.objects.create_notification(to_user, grid, request.user)
        notification.send_to(to_user.email)

def confirm(request, notification_key=None):
    """
    User clicks on link in email, accepting invitation to grid
    """
    if notification_key and is_key_valid(notification_key):
        notification_object = is_key_valid(notification_key)
        to_user = notification_object.to_user
        from_user = notification_object.from_user
        user_profile = UserProfile.objects.get(user=to_user)
        grid = notification_object.gridgroup
        if user_profile.approval_queue.filter(pk=grid.id):
            grid.members.add(to_user.pk)
            user_profile.approval_queue.remove(grid.pk)
            notification_object.key = NotificationKey.model.ACTIVATED
            return render_to_response('notification/success.html', {'to_user':to_user, 'from_user': from_user, 'grid':grid})
        else:
            return render_to_response('notification/failure.html', {'to_user':to_user, 'from_user': from_user, 'grid':grid})
    else:
        return render_to_response('notification/failure.html', {'to_user':to_user, 'from_user': from_user, 'grid':grid})

@receiver(grid_requested, dispatch_uid='user_invited')
def request(sender, to_founder, grid, request, **kwargs):
    """
    User asks founder for permission to be in the grid
    """
    if not grid.request_queue.filter(pk=request.user.pk):
        print('sending')
        notification = NotificationKey.objects.create_notification(to_founder, grid, request.user)
        notification.send_to(to_founder.email)

def accept(request, notification_key=None):
    """
    Founder clicks link in email, approving request
    """
    if notification_key and is_key_valid(notification_key):
        notification_object = is_key_valid(notification_key)
        grid = notification_object.gridgroup
        if grid.request_queue.filter(username=notification_object.from_user.username):
            grid.members.add(notification_object.from_user.pk)
            grid.request_queue.remove(notification_object.from_user.pk)
            notification_object.key = NotificationKey.model.ACTIVATED
            return render_to_response('notification/success_request.html', {'to_user':notification_object.to_user, 'from_user': notification_object.from_user, 'grid':grid})
        else:
            return render_to_response('notification/failure_request.html', {'to_user':'test'})
    else:
        return render_to_response('notification/failure_request.html', {'to_user':'test'})
