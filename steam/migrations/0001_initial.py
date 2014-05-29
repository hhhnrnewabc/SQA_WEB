# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table('steam_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('game_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('web_url', self.gf('django.db.models.fields.URLField')(max_length=225)),
            ('developer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('steam', ['Game'])

        # Adding model 'GameLanguages'
        db.create_table('steam_gamelanguages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('has_interface', self.gf('django.db.models.fields.BooleanField')()),
            ('has_full_audio', self.gf('django.db.models.fields.BooleanField')()),
            ('has_subtitles', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('steam', ['GameLanguages'])

        # Adding model 'GameVersions'
        db.create_table('steam_gameversions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('steam', ['GameVersions'])

        # Adding model 'GameUpdatedDate'
        db.create_table('steam_gameupdateddate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.GameVersions'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('steam', ['GameUpdatedDate'])

        # Adding model 'GameReviews'
        db.create_table('steam_gamereviews', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.GameVersions'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('steam', ['GameReviews'])

        # Adding model 'GameSystemRequirements'
        db.create_table('steam_gamesystemrequirements', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('required_level', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('processor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('memory', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('graphics', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hard_drive', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('additional_notes', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('steam', ['GameSystemRequirements'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table('steam_game')

        # Deleting model 'GameLanguages'
        db.delete_table('steam_gamelanguages')

        # Deleting model 'GameVersions'
        db.delete_table('steam_gameversions')

        # Deleting model 'GameUpdatedDate'
        db.delete_table('steam_gameupdateddate')

        # Deleting model 'GameReviews'
        db.delete_table('steam_gamereviews')

        # Deleting model 'GameSystemRequirements'
        db.delete_table('steam_gamesystemrequirements')


    models = {
        'steam.game': {
            'Meta': {'object_name': 'Game'},
            'developer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '225'})
        },
        'steam.gamelanguages': {
            'Meta': {'object_name': 'GameLanguages'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'has_full_audio': ('django.db.models.fields.BooleanField', [], {}),
            'has_interface': ('django.db.models.fields.BooleanField', [], {}),
            'has_subtitles': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'steam.gamereviews': {
            'Meta': {'object_name': 'GameReviews'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.GameVersions']"})
        },
        'steam.gamesystemrequirements': {
            'Meta': {'object_name': 'GameSystemRequirements'},
            'additional_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'graphics': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hard_drive': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'processor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required_level': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'steam.gameupdateddate': {
            'Meta': {'object_name': 'GameUpdatedDate'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.GameVersions']"})
        },
        'steam.gameversions': {
            'Meta': {'object_name': 'GameVersions'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['steam']