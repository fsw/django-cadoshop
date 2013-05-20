from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin

from . import models
from imagekit.admin import AdminThumbnail
from plata.shop.models import TaxClass
from django.conf import settings
from django import forms
from models import Product, ProductOption

from django.forms.models import inlineformset_factory
from django.contrib.admin.util import flatten_fieldsets
from django.utils.functional import curry
from cadolib.admin import StaticPage, StaticPageAdmin, Setting, SettingAdmin

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 0
    fieldsets = (
        (
         None, 
         {
            'fields': ('name', 'price_mod', 'extra', 'colors', 'image')
            }
        ),
    )
    def get_formset(self, request, obj=None, **kwargs):
        return super(ProductOptionInline, self).get_formset(request, obj=obj, **kwargs)
        
    
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    class Media:
        js = (
                #"/static/admin/js/inlines.js",  #this needs to be loaded before productadmin
                "/static/cadoshop/productadmin.js",
            )
    list_display = ('category', 'admin_thumbnail', 'name', '_unit_price', 'is_active')
    list_display_links = ('name', 'admin_thumbnail',)
    list_filter = ('is_active', '_unit_price')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    admin_thumbnail = AdminThumbnail(image_field='tiny_thumbnail')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'manufacturer', '_unit_price', 'description', 'is_active', 'colors')
        }),
        ('Fits to Products', {
            'classes': ('collapse', 'grp-collapse', 'grp-closed'),
            'fields': ('fits_to',)
        }),
        ('Extra Fields', {
            'classes': ('collapse', 'grp-collapse', 'grp-closed'),
            'fields': ('extra',)
        }),
        ('Images', {
            'classes': ('collapse', 'grp-collapse', 'grp-closed'),
            'fields': ('image1','image2','image3','image4','image5')
        }),
        ('Advanced options', {
            'classes': ('collapse', 'grp-collapse', 'grp-closed'),
            'fields': ('currency', 'tax_included', 'tax_class')
        }),
    )
    radio_fields = {'tax_class': admin.HORIZONTAL, 'currency': admin.HORIZONTAL}
    
    inlines = (ProductOptionInline, )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tax_class":
            kwargs["initial"] = TaxClass.objects.all()[0].id
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "currency":
            kwargs["initial"] = settings.CURRENCIES[0]
        return super(ProductAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    
    def save_form(self, request, form, change):
        #print form
        #print 'ASDASD'
        return form.save(commit=False)
    
    def save_model(self, request, obj, form, change):
        #print obj.values()
        obj.save()
        
    def save_formset(self, request, form, formset, change):
        #print 'FS'
        formset.save()

class ProductCategoryAdmin(MPTTModelAdmin):
    
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    
    list_display = ('name', 'admin_thumbnail', 'get_excerpt', 'active')
    list_display_links = ('name',)
    list_filter = ('active', )
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'order', 'active', 'description', 'thumbnail', 'extra_search_terms')
        }),
        ('SEO', {
            'fields': ('seo_keywords', 'seo_description', 'seo_title',)
        }),
        ('Extra Fields', {
            'fields': ('extra_fields',)
        }),
    )
        
class ManufacturerAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='tiny_thumbnail')
    list_display = ('name', 'admin_thumbnail', 'url')
    list_display_links = ('name',)
    
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'logo', 'url' )
        }),
    )


admin.site.register(models.Manufacturer, ManufacturerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)

admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Setting, SettingAdmin)