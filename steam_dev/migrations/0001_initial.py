# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SteamDeveloper'
        db.create_table('steam_dev_steamdeveloper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('baseuser', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['baseuser.BaseUser'])),
            ('steam_user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['steam_user.SteamUser'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20)),
            ('fax', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20)),
            ('company_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('api_token', self.gf('django.db.models.fields.CharField')(unique=True, blank=True, max_length=100)),
            ('secret_token', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('steam_dev', ['SteamDeveloper'])

        # Adding model 'SteamDevAPPS'
        db.create_table('steam_dev_steamdevapps', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('steam_dev', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['steam_dev.SteamDeveloper'])),
            ('web_url', self.gf('django.db.models.fields.URLField')(max_length=225)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('app_introduction', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('photo_big', self.gf('django.db.models.fields.files.ImageField')(default='noImageAvailable300.png', blank=True, max_length=200)),
            ('photo_small', self.gf('django.db.models.fields.files.ImageField')(default='noImageAvailable300.png', blank=True, max_length=200)),
            ('api_token', self.gf('django.db.models.fields.CharField')(unique=True, blank=True, max_length=100)),
            ('secret_token', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('steam_dev', ['SteamDevAPPS'])


    def backwards(self, orm):
        # Deleting model 'SteamDeveloper'
        db.delete_table('steam_dev_steamdeveloper')

        # Deleting model 'SteamDevAPPS'
        db.delete_table('steam_dev_steamdevapps')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'baseuser.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '225'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'steam_dev.steamdevapps': {
            'Meta': {'object_name': 'SteamDevAPPS'},
            'api_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'max_length': '100'}),
            'app_introduction': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo_big': ('django.db.models.fields.files.ImageField', [], {'default': "'noImageAvailable300.png'", 'blank': 'True', 'max_length': '200'}),
            'photo_small': ('django.db.models.fields.files.ImageField', [], {'default': "'noImageAvailable300.png'", 'blank': 'True', 'max_length': '200'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'steam_dev': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['steam_dev.SteamDeveloper']"}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '225'})
        },
        'steam_dev.steamdeveloper': {
            'Meta': {'object_name': 'SteamDeveloper'},
            'address': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'api_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'max_length': '100'}),
            'baseuser': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['baseuser.BaseUser']"}),
            'company_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'steam_user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['steam_user.SteamUser']"}),
            'work_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'})
        },
        'steam_user.steamuser': {
            'Meta': {'object_name': 'SteamUser'},
            'api_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'max_length': '100'}),
            'baseuser': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['baseuser.BaseUser']"}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'noImageAvailable300.png'", 'blank': 'True', 'max_length': '200'}),
            'secret_token': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1'})
        }
    }

    complete_apps = ['steam_dev']