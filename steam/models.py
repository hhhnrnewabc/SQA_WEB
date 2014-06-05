from django.db import models
from django.utils.translation import ugettext_lazy as _


REQUIRED_LEVEL = (
    ('M', _('Minimum')),
    ('R', _('Recommended')),
    ('O', _('Other')),
)

GAME_TYPE = (
    ('Action', _('Action')),
    ('Adventure', _('Adventure')),
    ('Strategy', _('Strategy')),
    ('RPG', _('RPG')),
    ('Indie', _('Indie')),
    ('MM', _('Massively Multiplayer')),
    ('Casual', _('Casual')),
    ('Simulation', _('Simulation')),
    ('Racing', _('Racing')),
    ('Sports', _('Sports')),
    ('Other', _('Other'))
)


class Game(models.Model):
    name = models.CharField(_('Gmae Name'), max_length=200,
                            help_text=_('Your gmae name for publish. Max lenght:200'))
    game_type = models.CharField(_('Game Type.'), max_length=20,
                                 choices=GAME_TYPE,
                                 help_text=_('Gmae type. If not find, choice "Other".'))
    release_date = models.DateTimeField(_('Release Date'), help_text=_('The date game will release.'))
    web_url = models.URLField(_('Game Web Url'), max_length=225, help_text=_('Game more info WEB URL.'))
    developer = models.CharField(_('Developer'), max_length=200, help_text=_('Game Developer full name.'))
    publisher = models.CharField(_('Publisher'), max_length=200, help_text=_('Game Publisher Company'))

    def __str__(self):
        return "%s" % self.name


class GameLanguages(models.Model):
    game = models.ForeignKey(Game)
    language = models.CharField(_('Gmae Language'), max_length=200,
                                help_text=_('Language full name. Ex:English, Traditional Chinese'))
    has_interface = models.BooleanField(_('Has Interface'), help_text=_('In this language has full inuerface?'))
    has_full_audio = models.BooleanField(_('Has Full Audio'), help_text=_('In this language has full audio?'))
    has_subtitles = models.BooleanField(_('Has Subtitles'), help_text=_('In this language has full subtitles?'))

    def __str__(self):
        return "%s" % self.language


class GameVersions(models.Model):
    game = models.ForeignKey(Game)
    version = models.CharField(_('Game Version'), max_length=10, help_text=_('Version Ex: 1.0.0  Max lenght:20'))
    updated_date = models.DateTimeField(_('Updated Date'))

    def __str__(self):
        return "%s" % self.version


class GameUpdatedDate(models.Model):
    game = models.ForeignKey(Game)
    version = models.ForeignKey(GameVersions)
    reason = models.CharField(_('Game Update Reason'), max_length=1000,
                              help_text=_('Update reason. Max Lenght:1000. Type:MarkDown, text'))

    def __str__(self):
        return "%s-%s" % (self.version, self.reason)


class GameReviews(models.Model):
    game = models.ForeignKey(Game)
    pub_date = models.DateTimeField(_('Game Reviews Published Date'))
    version = models.ForeignKey(GameVersions)
    comment = models.CharField(_('Game Reviews Comment'), max_length=200)

    def __str__(self):
        return "%s-%s" % (self.game, self.version)


class GameSystemRequirements(models.Model):
    game = models.ForeignKey(Game)
    required_level = models.CharField(_('Game System Required Level'),
                                      max_length=1, choices=REQUIRED_LEVEL)
    os = models.CharField(_('Game System OS'), max_length=50)
    processor = models.CharField(_('Game System Processor'), max_length=50)
    memory = models.CharField(_('Game System Memory'), max_length=50)
    graphics = models.CharField(_('Game System Graphics'), max_length=50)
    hard_drive = models.CharField(_('Game System Hard Drive'), max_length=50)
    additional_notes = models.CharField(_('Game Additional Notes'),
                                        max_length=200)

    def __str__(self):
        return "%s-%s" % (self.game, self.required_level)
