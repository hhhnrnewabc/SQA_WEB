from django.db import models
from baseuser.models import BaseUser
from steam.models import Game
from django.utils.translation import ugettext_lazy as _
from time import gmtime, strftime
import binascii
import hashlib
import os
from django.conf import settings


SEX = {
    ('F','Female'),
    ('M','Male'),
    ('O','Other'),
}


def get_upload_file_name(instance, filename):
    return "uploaded_files/user/%s/" % hashlib.sha256(binascii.hexlify(bytes(instance.baseuser.email, 'utf-8'))).hexdigest() + \
        "%s_%s" % (strftime("%Y_%m_%d", gmtime()), hashlib.md5(binascii.hexlify(os.urandom(len(filename)))).hexdigest()) + \
        ".%s" % filename.split('.')[-1].lower()


class SteamUser(models.Model):
    baseuser = models.OneToOneField(BaseUser)
    first_name = models.CharField(_('First Name'), max_length=30, help_text=_('Your First Name'), blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, help_text=_('Your Last Name'), blank=True)
    nick_name = models.CharField(_('Nick Name'), max_length=30, help_text=_('Your Nick Name'), blank=True)
    cell_phone = models.CharField(_('Cell Phone'),  max_length=20, help_text=_('Cell Phone Number ex:+886 912-345-678'),
                                  blank=True)
    sex = models.CharField(_('Sex'), max_length=1, choices=SEX, help_text=_('Sex :Female, Male, Other '), blank=True)
    photo = models.ImageField(_('Image'), help_text=_('Image:jpg'), upload_to=get_upload_file_name, max_length=200,
                              blank=True, default=settings.NO_IMAGE_AVAILABLE_PHOTO)

    api_token = models.CharField(max_length=100, unique=True, blank=True)
    secret_token = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def generate_key(self):
        return binascii.hexlify(os.urandom(50))  # Generate key ex:b'fd2eaf5c3677f50820b8c...' lenght is 100

    def create_new_secret_token(self):
        self.secret_token = self.generate_key()
        self.save()

    def save(self, commit=True, *args, **kwargs):
        if not self.api_token:
            self.api_token = self.generate_key()
        if not self.secret_token:
            self.secret_token = self.generate_key()
        if commit:
            return super(SteamUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.baseuser.email

    def update(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
        self.save()


class StreamFriends(models.Model):
    steam_user_id = models.ForeignKey(SteamUser)
    last_togther_play_game = models.ForeignKey(Game)
    last_togther_play_time = models.DateTimeField()


