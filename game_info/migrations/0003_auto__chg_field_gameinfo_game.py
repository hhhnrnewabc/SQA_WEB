# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'GameInfo.game'
        db.alter_column('game_info_gameinfo', 'game_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['steam_dev.SteamDevAPPS']))

    def backwards(self, orm):

        # Changing field 'GameInfo.game'
        db.alter_column('game_info_gameinfo', 'game_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['game_info.GameRelation']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'baseuser.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '225', 'unique': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'game_info.gameinfo': {
            'Meta': {'object_name': 'GameInfo'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'chess': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eaten': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'fromx': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'fromy': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['steam_dev.SteamDevAPPS']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nema': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tox': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'toy': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'game_info.gamerelation': {
            'Meta': {'object_name': 'GameRelation'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'primary_key': 'True', 'to': "orm['steam_dev.SteamDevAPPS']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'steam_dev.steamdevapps': {
            'Meta': {'object_name': 'SteamDevAPPS'},
            'api_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '100'}),
            'app_introduction': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'blank': 'True', 'default': "'noImageAvailable300.png'"}),
            'photo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'blank': 'True', 'default': "'noImageAvailable300.png'"}),
            'secret_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'steam_dev': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam_dev.SteamDeveloper']"}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '225'})
        },
        'steam_dev.steamdeveloper': {
            'Meta': {'object_name': 'SteamDeveloper'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'api_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '100'}),
            'baseuser': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['baseuser.BaseUser']", 'unique': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'steam_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['steam_user.SteamUser']", 'unique': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'steam_user.steamuser': {
            'Meta': {'object_name': 'SteamUser'},
            'api_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '100'}),
            'baseuser': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['baseuser.BaseUser']", 'unique': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'blank': 'True', 'default': "'userDefaultAvatar.png'"}),
            'secret_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['game_info']