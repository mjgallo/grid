import os
import random
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from custom_registration.models import UserProfile

# Create your models here.
from grid.models import Restaurant, GridGroup

from registration.models import SHA1_RE


class NotificationKeyManager(models.Manager):
    def is_key_valid(self, notification_key):
        """
        Check if an ``InvitationKey`` is valid or not, returning a boolean,
        ``True`` if the key is valid.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(notification_key):
            try:
                notification_key = self.get(key=notification_key)
            except self.model.DoesNotExist:
                return False
            return notification_key
        return False

    def create_notification(self, to_user, grid, from_user):
        """
        Create an ``NotificationKey`` and returns it.
        
        The key for the ``InvitationKey`` will be a SHA1 hash, generated 
        from a combination of the ``User``'s username and a random salt.
        """
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        key = sha_constructor(salt+to_user.username).hexdigest()
        return self.create(from_user=from_user, key=key, gridgroup=grid, to_user=to_user)

class NotificationKey(models.Model):
    key = models.CharField(_('notification key'), max_length=40)
    date_invited = models.DateTimeField(_('date invited'), 
                                        auto_now_add=True)
    from_user = models.ForeignKey(User, blank=True, null=True, related_name='notification_initiator')
    gridgroup = models.ForeignKey(GridGroup, blank=True, null=True)
    to_user = models.ForeignKey(User, blank=True, null=True, related_name='notification_destination')
    
    objects = NotificationKeyManager()
    
    def __unicode__(self):
        return u"Notification from %s on %s" % (self.from_user.username, self.date_invited)
    
    def key_expired(self):
        """
        Determine whether this ``InvitationKey`` has expired, returning 
        a boolean -- ``True`` if the key has expired.
        
        The date the key has been created is incremented by the number of days 
        specified in the setting ``ACCOUNT_INVITATION_DAYS`` (which should be 
        the number of days after invite during which a user is allowed to
        create their account); if the result is less than or equal to the 
        current date, the key has expired and this method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_INVITATION_DAYS)
        return self.date_invited + expiration_date <= timezone.now()
    key_expired.boolean = True
    
    def send_to(self, email):
        """
        Send an invitation email to ``email``.
        """
        print self.key

        current_site = Site.objects.get_current()
        template_subject, template_email = (None, None)
        # Logic to determine whether this is an invitation or a request
        # evaluates true if invitation, i.e. grid is in to_user's approval queue
        if UserProfile.objects.get(user=self.to_user).approval_queue.filter(pk=self.gridgroup.pk):
            template_subject, template_email = ('notification/invitation_email_subject.txt',
                                                'notification/invitation_email.txt')
        else:
            template_subject, template_email = ('notification/request_email_subject.txt',
                                                'notification/request_email.txt')

        subject = render_to_string(template_subject,
                                   { 'site': current_site,
                                   'from_email':self.from_user.email })
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string(template_email,
                                   { 'from_email': self.from_user.email,
                                   'grid': self.gridgroup.name,
                                   'notification_key': self.key,
                                     'site': current_site })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])