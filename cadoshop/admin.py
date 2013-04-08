from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin

from . import models
from imagekit.admin import AdminThumbnail
from plata.shop.models import TaxClass
from django.conf import settings
from django import forms
from models import Product

class ProductForm(forms.ModelForm):
    options = forms.CharField(label=_("Options"), max_length=512,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
        help_text = _("Optional comma separated list"),)

    class Meta:
        model = Product

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    class Media:
        js = (
                "/static/cadoshop/productadmin.js",
            )
    list_display = ('category', 'admin_thumbnail', 'name', '_unit_price', 'is_active', 'ordering')
    list_display_links = ('name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    admin_thumbnail = AdminThumbnail(image_field='tiny_thumbnail')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', '_unit_price', 'description', 'is_active', 'options')
        }),
        ('Extra Fields', {
            'fields': ('extra',)
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image5')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('currency', 'tax_included', 'tax_class', 'ordering')
        }),
    )
    radio_fields = {'tax_class': admin.HORIZONTAL, 'currency': admin.HORIZONTAL}
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tax_class":
            kwargs["initial"] = TaxClass.objects.all()[0].id
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "currency":
            kwargs["initial"] = settings.CURRENCIES[0]
        return super(ProductAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    
    
class ProductCategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'order', 'active', 'description', 'thumbnail')
        }),
        ('SEO', {
            'fields': ('meta_keywords',)
        }),
        ('Extra Fields', {
            'fields': ('extra_fields',)
        }),
    )


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)