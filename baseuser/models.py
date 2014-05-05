from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, is_active=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_staff(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, True, False, True,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    password, is_superuser, groups, user_permissions in PermissionsMixin

    Username, email are required. Other fields are optional.
    """

    email = models.EmailField(_('email address'), unique=True, max_length=225,
                              error_messages={'unique': "This email has already been registered."})
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        return self.email.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        return "sent to " + self.email +" "+ subject +" "+ message

    def __str__(self):
        return self.get_email()

    def get_email(self):
        return self.email