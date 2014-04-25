from django.db import models
from baseuser.models import BaseUser
from steam_user.models import SteamUser
from django.utils.translation import ugettext_lazy as _
import binascii
import hashlib
import os


class SteamDeveloper(models.Model):
    baseuser = models.OneToOneField(BaseUser)
    steam_user_id = models.OneToOneField(SteamUser)


class SteamDevAPPS(models.Model):
    steam_dev_id = models.ForeignKey(SteamDeveloper)
    web_url = models.URLField(_('Web URL'), max_length=225, help_text=_('Your Web URL Address'))
    app_name = models.CharField(_('APP Name'), max_length=30, help_text=_('Your APP Name. Max Length:30'))
    app_introduction = models.CharField(_('APP Introduction'), max_length=300,
                                        help_text=_('Your APP Introduction. Max Length:300'))
    api_token = models.CharField(max_length=100, unique=True)
    secret_token = models.CharField(max_length=100)
    created_date = models.DateTimeField()

    def generate_key(self):
        return binascii.hexlify(os.urandom(50))  # Generate key ex:b'fd2eaf5c3677f50820b8c...' lenght is 100

    def create_new_secret_token(self):
        self.secret_token = self.generate_key()
        self.save()

    def save(self, *args, **kwargs):
        if not self.api_token:
            self.api_token = self.generate_key()
        if not self.secret_token:
            self.secret_token = self.generate_key()
        return super(SteamDevAPPS, self).save(*args, **kwargs)