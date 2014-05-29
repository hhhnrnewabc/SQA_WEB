# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SteamUser'
        db.create_table('steam_user_steamuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('baseuser', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['baseuser.BaseUser'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('nick_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20)),
            ('sex', self.gf('django.db.models.fields.CharField')(blank=True, max_length=1)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(blank=True, default='noImageAvailable300.png', max_length=200)),
            ('api_token', self.gf('django.db.models.fields.CharField')(blank=True, unique=True, max_length=100)),
            ('secret_token', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('steam_user', ['SteamUser'])

        # Adding model 'StreamFriends'
        db.create_table('steam_user_streamfriends', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('steam_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam_user.SteamUser'])),
            ('last_togther_play_game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam.Game'])),
            ('last_togther_play_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('steam_user', ['StreamFriends'])


    def backwards(self, orm):
        # Deleting model 'SteamUser'
        db.delete_table('steam_user_steamuser')

        # Deleting model 'StreamFriends'
        db.delete_table('steam_user_streamfriends')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'baseuser.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '225', 'unique': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'steam_user.steamuser': {
            'Meta': {'object_name': 'SteamUser'},
            'api_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '100'}),
            'baseuser': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['baseuser.BaseUser']", 'unique': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "'noImageAvailable300.png'", 'max_length': '200'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1'})
        },
        'steam_user.streamfriends': {
            'Meta': {'object_name': 'StreamFriends'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_togther_play_game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam.Game']"}),
            'last_togther_play_time': ('django.db.models.fields.DateTimeField', [], {}),
            'steam_user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam_user.SteamUser']"})
        }
    }

    complete_apps = ['steam_user']