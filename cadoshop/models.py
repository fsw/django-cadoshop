import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _

from plata.product.models import ProductBase
from plata.shop.models import PriceBase


from cadolib.models import Tree, Sluggable
from mptt.fields import TreeForeignKey

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

#class ProductCategory(Tree, Sluggable):
#    name = models.CharField(max_length=256, default='') #Alergolog
#    class Meta:
#        verbose_name = _('category')
#        verbose_name_plural = _('categories')

#    def __unicode__(self):
#        return self.name
        
class Product(ProductBase, PriceBase):
    """(Nearly) the simplest product model ever"""
    
    #category = TreeForeignKey(ProductCategory)
    category = models.ForeignKey('categories.Category')
    is_active = models.BooleanField(_('is active'), default=True)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    ordering = models.PositiveIntegerField(_('ordering'), default=0)
    

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
        return ('plata_product_detail', (), {'object_id': self.pk})
    
    def get_price(self, *args, **kwargs):
        return self

    def handle_order_item(self, orderitem):
        ProductBase.handle_order_item(self, orderitem)
        PriceBase.handle_order_item(self, orderitem)
