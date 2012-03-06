# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Site.folder_name'
        db.add_column('django_site', 'folder_name', self.gf('dynamicsites.fields.FolderNameField')(default=None, max_length=64, blank=True), keep_default=False)

        # Adding field 'Site.subdomains'
        db.add_column('django_site', 'subdomains', self.gf('dynamicsites.fields.SubdomainListField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Site.folder_name'
        db.delete_column('django_site', 'folder_name')

        # Deleting field 'Site.subdomains'
        db.delete_column('django_site', 'subdomains')


    models = {
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'folder_name': ('dynamicsites.fields.FolderNameField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subdomains': ('dynamicsites.fields.SubdomainListField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['sites']