# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Product.extra'
        db.alter_column(u'cadoshop_product', 'extra', self.gf('cadocms.fields.ExtraFieldsValues')(null=True))

        # Changing field 'ProductOption.extra'
        db.alter_column(u'cadoshop_productoption', 'extra', self.gf('cadocms.fields.ExtraFieldsValues')(null=True))

        # Changing field 'ProductCategory.extra_fields'
        db.alter_column(u'cadoshop_productcategory', 'extra_fields', self.gf('cadocms.fields.ExtraFieldsDefinition')(null=True))

    def backwards(self, orm):

        # Changing field 'Product.extra'
        db.alter_column(u'cadoshop_product', 'extra', self.gf('cadoshop.fields.ExtraFieldsValues')(null=True))

        # Changing field 'ProductOption.extra'
        db.alter_column(u'cadoshop_productoption', 'extra', self.gf('cadoshop.fields.ExtraFieldsValues')(null=True))

        # Changing field 'ProductCategory.extra_fields'
        db.alter_column(u'cadoshop_productcategory', 'extra_fields', self.gf('cadoshop.fields.ExtraFieldsDefinition')(null=True))

    models = {
        u'cadoshop.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'cadoshop.product': {
            'Meta': {'object_name': 'Product'},
            '_unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '10'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['cadoshop.ProductCategory']"}),
            'colors': ('cadoshop.fields.ColorsField', [], {'max_length': '255', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extra': ('cadocms.fields.ExtraFieldsValues', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            'fits_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cadoshop.Product']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image4': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image5': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cadoshop.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tax_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['shop.TaxClass']"}),
            'tax_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'cadoshop.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_fields': ('cadocms.fields.ExtraFieldsDefinition', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['cadoshop.ProductCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'seo_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seo_keywords': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'cadoshop.productoption': {
            'Meta': {'object_name': 'ProductOption'},
            'colors': ('cadoshop.fields.ColorsField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'extra': ('cadocms.fields.ExtraFieldsValues', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price_mod': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cadoshop.Product']"})
        },
        u'shop.taxclass': {
            'Meta': {'ordering': "['-priority']", 'object_name': 'TaxClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['cadoshop']