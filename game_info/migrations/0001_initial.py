# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameRelation'
        db.create_table('game_info_gamerelation', (
            ('game', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('game_info', ['GameRelation'])

        # Adding model 'GameInfo'
        db.create_table('game_info_gameinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['game_info.GameRelation'])),
            ('nema', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('chess', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('eaten', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fromx', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('fromy', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('tox', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('toy', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('game_info', ['GameInfo'])


    def backwards(self, orm):
        # Deleting model 'GameRelation'
        db.delete_table('game_info_gamerelation')

        # Deleting model 'GameInfo'
        db.delete_table('game_info_gameinfo')


    models = {
        'game_info.gameinfo': {
            'Meta': {'object_name': 'GameInfo'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'chess': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'eaten': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'fromx': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'fromy': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['game_info.GameRelation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nema': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tox': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'toy': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'game_info.gamerelation': {
            'Meta': {'object_name': 'GameRelation'},
            'game': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['game_info']