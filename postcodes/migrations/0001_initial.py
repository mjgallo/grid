# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Postcode'
        db.create_table(u'postcodes_postcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'postcodes', ['Postcode'])


    def backwards(self, orm):
        # Deleting model 'Postcode'
        db.delete_table(u'postcodes_postcode')


    models = {
        u'postcodes.postcode': {
            'Meta': {'object_name': 'Postcode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'})
        }
    }

    complete_apps = ['postcodes']