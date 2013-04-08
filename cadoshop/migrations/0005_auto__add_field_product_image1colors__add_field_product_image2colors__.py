# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.image1colors'
        db.add_column('cadoshop_product', 'image1colors',
                      self.gf('cadoshop.fields.ColorsField')(default='', max_length=7, blank=True),
                      keep_default=False)

        # Adding field 'Product.image2colors'
        db.add_column('cadoshop_product', 'image2colors',
                      self.gf('cadoshop.fields.ColorsField')(default='', max_length=7, blank=True),
                      keep_default=False)

        # Adding field 'Product.image3colors'
        db.add_column('cadoshop_product', 'image3colors',
                      self.gf('cadoshop.fields.ColorsField')(default='', max_length=7, blank=True),
                      keep_default=False)

        # Adding field 'Product.image4colors'
        db.add_column('cadoshop_product', 'image4colors',
                      self.gf('cadoshop.fields.ColorsField')(default='', max_length=7, blank=True),
                      keep_default=False)

        # Adding field 'Product.image5colors'
        db.add_column('cadoshop_product', 'image5colors',
                      self.gf('cadoshop.fields.ColorsField')(default='', max_length=7, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.image1colors'
        db.delete_column('cadoshop_product', 'image1colors')

        # Deleting field 'Product.image2colors'
        db.delete_column('cadoshop_product', 'image2colors')

        # Deleting field 'Product.image3colors'
        db.delete_column('cadoshop_product', 'image3colors')

        # Deleting field 'Product.image4colors'
        db.delete_column('cadoshop_product', 'image4colors')

        # Deleting field 'Product.image5colors'
        db.delete_column('cadoshop_product', 'image5colors')


    models = {
        'cadoshop.product': {
            'Meta': {'ordering': "['ordering', 'name']", 'object_name': 'Product'},
            '_unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '10'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'to': "orm['cadoshop.ProductCategory']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extra': ('cadoshop.fields.ExtraFieldsValues', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image1colors': ('cadoshop.fields.ColorsField', [], {'max_length': '7', 'blank': 'True'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image2colors': ('cadoshop.fields.ColorsField', [], {'max_length': '7', 'blank': 'True'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image3colors': ('cadoshop.fields.ColorsField', [], {'max_length': '7', 'blank': 'True'}),
            'image4': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image4colors': ('cadoshop.fields.ColorsField', [], {'max_length': '7', 'blank': 'True'}),
            'image5': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image5colors': ('cadoshop.fields.ColorsField', [], {'max_length': '7', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tax_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['shop.TaxClass']"}),
            'tax_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'cadoshop.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_fields': ('cadoshop.fields.ExtraFieldsDefinition', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cadoshop.ProductCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'shop.taxclass': {
            'Meta': {'ordering': "['-priority']", 'object_name': 'TaxClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['cadoshop']
