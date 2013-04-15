from haystack import indexes
from models import ProductOption
from django.db import models

import re

class ProductOptionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField(faceted=True)
    category = indexes.MultiValueField(faceted=True)
    product = indexes.IntegerField(model_attr='product__id')
    
    price = indexes.FloatField()
    colors = indexes.MultiValueField()
    has_image = indexes.BooleanField()
    
    def get_model(self):
        return ProductOption
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all() #filter(pub_date__lte=datetime.datetime.now())
    
    def prepare_tags(self, obj):
        return re.findall(r'[#]+([-_a-zA-Z0-9]+)', obj.product.description)
    
    def prepare_category(self, obj):
        path = obj.product.category.get_ancestors(include_self=True)
        ret = []
        for category in path:
            ret.append(category.slug)
        return ret
    
    def prepare_price(self, obj):
        return obj.product._unit_price
    
    def prepare_colors(self, obj):
        return []
    
    def prepare_has_image(self, obj):
        return bool(obj.image or obj.product.image1)

    def prepare(self, object):
        self.prepared_data = super(ProductOptionIndex, self).prepare(object)
        #print object.extra
        for key, field in object.product.category.get_extra_model_fields().items():
            h_field = indexes.index_field_from_django_field(field)
            if h_field == indexes.CharField:
                self.prepared_data['%s_s' % key] = object.extra_fields.get(key, None)
            elif h_field == indexes.DateTimeField:
                self.prepared_data['%s_dt' % key] = object.extra_fields.get(key, None)
            elif h_field == indexes.BooleanField:
                self.prepared_data['%s_b' % key] = object.extra_fields.get(key, None)
            elif h_field == indexes.MultiValueField:
                self.prepared_data['%s_s' % key] = object.extra_fields.get(key, None)
            elif h_field == indexes.FloatField:
                self.prepared_data['%s_f' % key] = object.extra_fields.get(key, None)
            elif h_field == indexes.IntegerField:
                self.prepared_data['%s_i' % key] = object.extra_fields.get(key, None)
            else:
                raise Exception('unknown type')
            #<dynamicField name="*_l"  type="long" />
            #<dynamicField name="*_t"  type="text_en" />
            #<dynamicField name="*_f"  type="float" />
            #<dynamicField name="*_d"  type="double" />
            #<dynamicField name="*_p" type="location" />
            
        return self.prepared_data
    
def reindex_product(sender, **kwargs):
    ProductOptionIndex().update_object(kwargs['instance'])
    
models.signals.post_save.connect(reindex_product, sender=ProductOption)
