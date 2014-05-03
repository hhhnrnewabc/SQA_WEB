from django.db import models
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from django.utils.translation import ugettext_lazy as _
from time import gmtime, strftime
import binascii
import hashlib
import os
from django.conf import settings


def get_upload_file_name(instance, filename):
    return "uploaded_files/dev/%s/" % hashlib.sha256(binascii.hexlify(
        bytes(instance.steam_dev.id, 'utf-8'))).hexdigest() + "%s_%s" % (strftime("%Y_%m_%d", gmtime()),
            hashlib.md5(binascii.hexlify(os.urandom(len(filename)))).hexdigest()) + ".%s" % filename.split('.')[-1].lower()


class SteamDeveloper(models.Model):
    baseuser = models.OneToOneField(BaseUser)
    steam_user = models.OneToOneField(SteamUser)


class SteamDevAPPS(models.Model):
    steam_dev = models.ForeignKey(SteamDeveloper)
    web_url = models.URLField(_('Web URL'), max_length=225, help_text=_('Your Web URL Address'))
    app_name = models.CharField(_('APP Name'), max_length=30, help_text=_('Your APP Name. Max Length:30'))
    app_introduction = models.CharField(_('APP Introduction'), max_length=300,
                                        help_text=_('Your APP Introduction. Max Length:300'))
    photo_big = models.ImageField(_('Image'), help_text=_('Image:jpg'), upload_to=get_upload_file_name, max_length=200,
                                  blank=True, default=settings.NO_IMAGE_AVAILABLE_PHOTO)
    photo_smell = models.ImageField(_('Image'), help_text=_('Image:jpg'), upload_to=get_upload_file_name,
                                    max_length=200, blank=True, default=settings.NO_IMAGE_AVAILABLE_PHOTO)
    api_token = models.CharField(max_length=100, unique=True, blank=True)
    secret_token = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.steam_dev.baseuser.email

    def generate_key(self):
        return binascii.hexlify(os.urandom(50))  # Generate key ex:b'fd2eaf5c3677f50820b8c...' lenght is 100

    def create_new_secret_token(self):
        self.secret_token = self.generate_key()
        self.save()

    def save(self, *args, **kwargs):
        if not self.api_token:
            key = self.generate_key()
            # Check api_token is unique
            try:
                count = 0  # generate_key in 10 times
                while count < 10 and SteamUser.objects.get(api_token=key):
                    count += 1
                    key = self.generate_key()

            except SteamUser.DoesNotExist:
                self.api_token = key
        if not self.secret_token:
            self.secret_token = self.generate_key()
        return super(SteamDevAPPS, self).save(*args, **kwargs)

    def update(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self.save()