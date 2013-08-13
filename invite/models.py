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
from grid.models import Restaurant, GridGroup
from custom_registration.models import UserProfile

from registration.models import SHA1_RE
# Create your models here.

class InvitationKeyManager(models.Manager):

    def establish_user_profile(self, invitation_key, username, password):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, return the ``User``
        after activating.
        
        If the key is not valid or has expired, return ``False``.
        
        If the key is valid but the ``User`` is already active,
        return ``False``.
        
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(invitation_key):
            try:
                profile = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return False
            new_user = User.objects.create_user(username=username, email=profile.to_email, password=password)
            new_group, user_created = GridGroup.objects.get_or_create(founder=new_user, name='My first grid')
            new_user_profile, profile_created = UserProfile.objects.get_or_create(user=new_user, default_grid=new_group)
            profile.gridgroup.members.add(new_user.pk)
            profile.key = self.model.ACTIVATED
            profile.save()
            return (new_user, profile.gridgroup)
        return False

    def is_key_valid(self, invitation_key):
        """
        Check if an ``InvitationKey`` is valid or not, returning a boolean,
        ``True`` if the key is valid.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(invitation_key):
            try:
                invitation_key = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return False
            return not invitation_key.key_expired()
        return False

    def create_invitation(self, user, grid, to_email):
        """
        Create an ``InvitationKey`` and returns it.
        
        The key for the ``InvitationKey`` will be a SHA1 hash, generated 
        from a combination of the ``User``'s username and a random salt.
        """
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        key = sha_constructor(salt+user.username).hexdigest()
        return self.create(from_user=user, key=key, gridgroup=GridGroup.objects.get(pk=grid), to_email=to_email)

    def return_grid(self, invitation_key):
        """
        Get the grid from which the invitation was extended
        """
        if SHA1_RE.search(invitation_key):
            try:
                invitation_key = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return None
            return invitation_key.gridgroup.pk

    def return_email(self, invitation_key):
        """
        Get the grid from which the invitation was extended
        """
        if SHA1_RE.search(invitation_key):
            try:
                invitation_key = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return None
            return invitation_key.to_email
    
    def return_user(self, invitation_key):
        """
        Get the grid from which the invitation was extended
        """
        if SHA1_RE.search(invitation_key):
            try:
                invitation_key = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return None
            return invitation_key.from_user

class InvitationKey(models.Model):
    ACTIVATED = u"ALREADY_ACTIVATED"
    key = models.CharField(_('invitation key'), max_length=40)
    date_invited = models.DateTimeField(_('date invited'), 
                                        auto_now_add=True)
    from_user = models.ForeignKey(User)
    gridgroup = models.ForeignKey(GridGroup)
    to_email = models.EmailField(max_length=254, null=True)
    
    objects = InvitationKeyManager()
    
    def __unicode__(self):
        return u"Invitation from %s on %s" % (self.from_user.username, self.date_invited)
    
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
        
        subject = render_to_string('invitation/invitation_email_subject.txt',
                                   { 'site': current_site,
                                   'from_email':self.from_user.email })
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('invitation/invitation_email.txt',
                                   { 'from_email': self.from_user.email,
                                   'grid': self.gridgroup.name,
                                   'invitation_key': self.key,
                                     'expiration_days': settings.ACCOUNT_INVITATION_DAYS,
                                     'site': current_site })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])