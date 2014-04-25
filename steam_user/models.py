from django.db import models
from baseuser.models import BaseUser
from steam.models import Game
from django.utils.translation import ugettext_lazy as _

SEX = {
    ('F','Female'),
    ('M','Male'),
    ('O','Other'),
}

class SteamUser(models.Model):
    baseuser = models.OneToOneField(BaseUser)
    first_name = models.CharField(_('First Name'), max_length=30, help_text=_('Your First Name'))
    last_name = models.CharField(_('Last Name'), max_length=30, help_text=_('Your Last Name'))
    nick_name = models.CharField(_('Nick Name'), max_length=30, help_text=_('Your Nick Name'))
    cell_phone = models.CharField(_('Cell Phone'),  max_length=20, help_text=_('Cell Phone Number ex:+886 912-345-678'))
    sex = models.CharField(_('Sex'), max_length=1, choices=SEX, help_text=_('Sex :Female, Male, Other '))


class StreamFriends(models.Model):
    steam_user_id = models.ForeignKey(SteamUser)
    last_togther_play_game = models.ForeignKey(Game)
    last_togther_play_time = models.DateTimeField()


