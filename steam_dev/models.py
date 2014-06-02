from django.db import models
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from django.utils.translation import ugettext_lazy as _
from time import gmtime, strftime
import binascii
import hashlib
import os
from django.conf import settings

MAX_TOKEN_LENGTH = 100  # Must be Even number if number is 99 will return int(99/2)*2 >> 98


def get_upload_file_name(instance, filename):
    return "uploaded_files/dev/%s/" % hashlib.sha256(binascii.hexlify(
        bytes(instance.steam_dev.id, 'utf-8'))).hexdigest() + "%s_%s" % (strftime("%Y_%m_%d", gmtime()),
            hashlib.md5(binascii.hexlify(os.urandom(len(filename)))).hexdigest()) + ".%s" % filename.split('.')[-1].lower()


class SteamDeveloper(models.Model):
    baseuser = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    steam_user = models.OneToOneField(SteamUser, on_delete=models.CASCADE)
    first_name = models.CharField(_('First Name'), max_length=30, help_text=_('Your First Name'), blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, help_text=_('Your Last Name'), blank=True)
    address = models.CharField(_('Address'), max_length=200, help_text=_('Your Address'), blank=True)
    work_phone = models.CharField(_('Work Phone'), max_length=20, help_text=_('Work Number ex:+886 4-2451-7250'),
                                  blank=True)
    fax = models.CharField(_('Fax'), max_length=20, help_text=_('Fax Number ex:+886 4-2451-7250'), blank=True)
    company_name = models.CharField(_('Company Name'), max_length=50, help_text=_('Your Company Name, Max length 50'),
                                   blank=True)
    api_token = models.CharField(max_length=100, unique=True, blank=True)
    secret_token = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_first_name() + self.get_last_name()
        return "<No Full Name>" + self.baseuser.email

    def generate_key(self):
        # Generate key ex:'fd2eaf5c3677f50820b8c...' length MAX_TOKEN_LENGTH
        return binascii.hexlify(os.urandom(int(MAX_TOKEN_LENGTH / 2))).decode("utf-8")

    def create_new_secret_token(self):
        self.secret_token = self.generate_key()
        self.save()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def save(self, commit=True, *args, **kwargs):
        if not self.api_token:
            self.api_token = self.generate_key()
        if not self.secret_token:
            self.secret_token = self.generate_key()
        if commit:
            return super(SteamDeveloper, self).save(*args, **kwargs)


class SteamDevAPPS(models.Model):
    steam_dev = models.ForeignKey(SteamDeveloper, on_delete=models.CASCADE)
    web_url = models.URLField(_('Web URL'), max_length=225, help_text=_('Your Web URL Address'))
    app_name = models.CharField(_('APP Name'), max_length=30, help_text=_('Your APP Name. Max Length:30'))
    app_introduction = models.CharField(_('APP Introduction'), max_length=300,
                                        help_text=_('Your APP Introduction. Max Length:300'))
    photo_big = models.ImageField(_('Image Big'), help_text=_('Image Big:jpg'),
                                  upload_to=get_upload_file_name, max_length=200,
                                  blank=True, default=settings.NO_IMAGE_AVAILABLE_PHOTO)
    photo_small = models.ImageField(_('Image Small'), help_text=_('Image Small:jpg'),
                                    upload_to=get_upload_file_name,
                                    max_length=200, blank=True, default=settings.NO_IMAGE_AVAILABLE_PHOTO)
    api_token = models.CharField(max_length=100, unique=True, blank=True)
    secret_token = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_app_name()

    def get_app_name(self):
        return self.app_name

    def generate_key(self):
        # Generate key ex:'fd2eaf5c3677f50820b8c...' length is 100
        return binascii.hexlify(os.urandom(int(MAX_TOKEN_LENGTH / 2))).decode("utf-8")

    def create_new_secret_token(self):
        self.secret_token = self.generate_key()
        self.save()

    def save(self, commit=True, *args, **kwargs):
        if not self.api_token:
            self.api_token = self.generate_key()
        if not self.secret_token:
            self.secret_token = self.generate_key()
        if commit:
            return super(SteamDevAPPS, self).save(*args, **kwargs)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()
