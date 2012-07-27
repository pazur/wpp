# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Song'
        db.create_table('songbook_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lyrics', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('songbook', ['Song'])


    def backwards(self, orm):
        # Deleting model 'Song'
        db.delete_table('songbook_song')


    models = {
        'songbook.song': {
            'Meta': {'object_name': 'Song'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lyrics': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['songbook']