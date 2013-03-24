import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
import simplejson

from plata.product.models import ProductBase
from plata.shop.models import PriceBase
from fields import JSONField

from cadolib.models import Tree, Sluggable
from mptt.fields import TreeForeignKey

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Adjust
from south.modelsinspector import add_introspection_rules
from django.forms import fields

add_introspection_rules([], ["^cadoshop\.models\.ExtraFieldsDefinition"])
add_introspection_rules([], ["^cadoshop\.models\.ExtraFieldsValues"])


        
class ExtraFieldsDefinition(JSONField):
    pass 
    
class ExtraFieldsValues(JSONField): 
    pass
'''
    __metaclass__ = models.SubfieldBase
    def db_type(self):
        return 'text'
    
    def get_prep_value(self, value): 
        if value: 
            value = simplejson.dumps(value)
            return value 
        return None 
    
    def to_python(self, value): 
        if isinstance(value, (str, unicode)): 
            value = simplejson.loads(value)
        return value 
    
    def formfield(self, **kwargs):
        print 'FORM FIELD'
        kwargs.update({'widget': ExtraFieldsDefinitionField})
        print kwargs
        return super(ExtraFieldsDefinition, self).formfield(**kwargs)
    
    def value_to_string(self, obj):
        print "VTS"
        return "asdf"

    
    __metaclass__ = models.SubfieldBase
    def db_type(self):
        return 'text'
    
    def get_prep_value(self, value): 
        if value: 
            value = simplejson.dumps(value)
            return value 
        return None 
    
    def to_python(self, value):
        if isinstance(value, (str, unicode)): 
            try:
                value = simplejson.loads(value)
            except Exception:
                value = {} 
        return value 
'''

class ProductCategory(Tree, Sluggable):

    name = models.CharField(max_length=100, verbose_name=_('name'))
    active = models.BooleanField(default=True, verbose_name=_('active'))
    
    thumbnail = ProcessedImageField([ResizeToFill(50, 50)], upload_to='categories', format='JPEG', options={'quality': 90})
    description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(
        blank=True,
        default="",
        max_length=255,
        help_text="Comma-separated keywords for search engines.")

    extra_fields = ExtraFieldsDefinition(null=True, blank=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name
        
class Product(ProductBase, PriceBase):
    """(Nearly) the simplest product model ever"""
    
    category = TreeForeignKey(ProductCategory)
    is_active = models.BooleanField(_('is active'), default=True)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    ordering = models.PositiveIntegerField(_('ordering'), default=0)
    extra = ExtraFieldsValues(null=True, blank=True)
    

    image1 = models.ImageField(verbose_name = _('Image 1'), upload_to='products', blank=True)
    image2 = models.ImageField(verbose_name = _('Image 2'), upload_to='products', blank=True)
    image3 = models.ImageField(verbose_name = _('Image 3'), upload_to='products', blank=True)
    image4 = models.ImageField(verbose_name = _('Image 4'), upload_to='products', blank=True)
    image5 = models.ImageField(verbose_name = _('Image 5'), upload_to='products', blank=True)
    thumbnail = ImageSpecField([ResizeToFill(170, 170)],
                               image_field='image1',
                               format='JPEG', options={'quality': 90})
    tiny_thumbnail = ImageSpecField([ResizeToFill(50, 50)],
                               image_field='image1',
                               format='JPEG', options={'quality': 90})
    
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = _('product')
        verbose_name_plural = _('products')
  
    #def __init__(self, *args, **kwargs):
    #    self._meta.get_field('_unit_price').decimal_places = 2
    #    super(Product, self).__init__(*args, **kwargs)
              
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', (), {'object_id': self.pk})
    
    def get_price(self, *args, **kwargs):
        return self

    def handle_order_item(self, orderitem):
        ProductBase.handle_order_item(self, orderitem)
        PriceBase.handle_order_item(self, orderitem)


