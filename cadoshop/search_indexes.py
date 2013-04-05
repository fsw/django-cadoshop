from haystack import indexes
from models import Product
import re

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='category__slug', faceted=True)
    tags = indexes.MultiValueField(faceted=True)
    
    def get_model(self):
        return Product
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all() #filter(pub_date__lte=datetime.datetime.now())
    
    def prepare_tags(self, obj):
        return re.findall(r'[#]+([-_a-zA-Z0-9]+)', obj.description)

    def prepare(self, object):
        self.prepared_data = super(ProductIndex, self).prepare(object)
        #print object.extra
        for key, field in object.category.extra_fields.items():
            h_field = indexes.index_field_from_django_field(field['modelField'])
            if h_field == indexes.CharField:
                self.prepared_data['%s_s' % key] = object.extra[key]
            elif h_field == indexes.DateTimeField:
                self.prepared_data['%s_dt' % key] = object.extra[key]
            elif h_field == indexes.BooleanField:
                self.prepared_data['%s_b' % key] = object.extra[key]
            elif h_field == indexes.MultiValueField:
                self.prepared_data['%s_s' % key] = object.extra[key]
            elif h_field == indexes.FloatField:
                self.prepared_data['%s_f' % key] = object.extra[key]
            elif h_field == indexes.IntegerField:
                self.prepared_data['%s_i' % key] = object.extra[key]
            else:
                raise Exception('unknown type')
            #<dynamicField name="*_l"  type="long" />
            #<dynamicField name="*_t"  type="text_en" />
            #<dynamicField name="*_f"  type="float" />
            #<dynamicField name="*_d"  type="double" />
            #<dynamicField name="*_p" type="location" />
            
        return self.prepared_data