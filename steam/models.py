from django.db import models
from django.utils.translation import ugettext_lazy as _

REQUIRED_LEVEL = (
    ('M', _('Minimum')),
    ('R', _('Recommended')),
    ('O', _('Other')),
)


class Game(models.Model):
    name = models.CharField(max_length=200)
    game_type = models.CharField(max_length=20)
    release_date = models.DateTimeField(_('Release Date'))
    web_url = models.URLField(max_length=225)
    developer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)


class GameLanguages(models.Model):
    game = models.ForeignKey(Game)
    language = models.CharField(max_length=200)
    has_interface = models.BooleanField()
    has_full_audio = models.BooleanField()
    has_subtitles = models.BooleanField()


class GameVersions(models.Model):
    game = models.ForeignKey(Game)
    version = models.CharField(max_length=10)
    updated_date = models.DateTimeField(_('Updated Date'))


class GameUpdatedDate(models.Model):
    game = models.ForeignKey(Game)
    version = models.ForeignKey(GameVersions)
    reason = models.CharField(max_length=1000)


class GameReviews(models.Model):
    game = models.ForeignKey(Game)
    pub_date = models.DateTimeField(_('Published Date'))
    version = models.ForeignKey(GameVersions)
    comment = models.CharField(max_length=200)


class GameSystemRequirements(models.Model):
    game = models.ForeignKey(Game)
    required_level = models.CharField(max_length=1, choices=REQUIRED_LEVEL)
    os = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    graphics = models.CharField(max_length=50)
    hard_drive = models.CharField(max_length=50)
    additional_notes = models.CharField(max_length=200)
