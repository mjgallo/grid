# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Restaurant'
        db.create_table(u'grid_restaurant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('post_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postcodes.Postcode'])),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'grid', ['Restaurant'])

        # Adding M2M table for field users_interested on 'Restaurant'
        m2m_table_name = db.shorten_name(u'grid_restaurant_users_interested')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm[u'grid.restaurant'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['restaurant_id', 'user_id'])

        # Adding model 'Review'
        db.create_table(u'grid_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restaurant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grid.Restaurant'])),
            ('review', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'grid', ['Review'])

        # Adding model 'GridGroup'
        db.create_table(u'grid_gridgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('founder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='grid_group_owner', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'grid', ['GridGroup'])

        # Adding M2M table for field members on 'GridGroup'
        m2m_table_name = db.shorten_name(u'grid_gridgroup_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gridgroup', models.ForeignKey(orm[u'grid.gridgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gridgroup_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Restaurant'
        db.delete_table(u'grid_restaurant')

        # Removing M2M table for field users_interested on 'Restaurant'
        db.delete_table(db.shorten_name(u'grid_restaurant_users_interested'))

        # Deleting model 'Review'
        db.delete_table(u'grid_review')

        # Deleting model 'GridGroup'
        db.delete_table(u'grid_gridgroup')

        # Removing M2M table for field members on 'GridGroup'
        db.delete_table(db.shorten_name(u'grid_gridgroup_members'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'grid.gridgroup': {
            'Meta': {'object_name': 'GridGroup'},
            'founder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grid_group_owner'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'grid.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'post_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postcodes.Postcode']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'users_interested': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'grid.review': {
            'Meta': {'object_name': 'Review'},
            'good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'restaurant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grid.Restaurant']"}),
            'review': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'postcodes.postcode': {
            'Meta': {'object_name': 'Postcode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'})
        }
    }

    complete_apps = ['grid']