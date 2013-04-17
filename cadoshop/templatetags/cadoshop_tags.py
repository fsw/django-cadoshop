from django import template
from django.core.urlresolvers import reverse
import urllib
register = template.Library()
import re
from django.utils.safestring import mark_safe
from cadoshop.models import ProductCategory
from django.forms.forms import Form
from django.forms import fields
from django.db import models
from haystack import indexes

@register.simple_tag(name="search_url", takes_context=True)
def get_search_url(context, category=None, tag=None, page=1):
    
    urlparams = context['search_params'].copy()
    if 'category' in urlparams:
        del urlparams['category']
    category_slug = category if category is not None else context['search_params'].get('category', '')
    urlparams['tags'] = tag if tag is not None else context['search_params'].get('tags', None)
    urlparams['page'] = page if page is not None else context['search_params'].get('page', None)
    
    urlparams = dict([k, str(v).encode('utf-8')] for k,v in urlparams.iteritems() if v is not None)    
    if (urlparams['page'] == '1'):
        del urlparams['page']
    
    return reverse('product_list', kwargs={'category_slug':category_slug}) + '?' + urllib.urlencode(urlparams)

@register.filter
def urlize_hashtags(value):
    def repl(m):
        hashtag = m.group(1)
        url = reverse('product_list', kwargs={'category_slug':''}) + '?tags=' + hashtag
        return '<a href="%s">&#35;%s</a>' % (url, hashtag)
    hashtag_pattern = re.compile(r'[#]+([-_a-zA-Z0-9]+)')
    return mark_safe(hashtag_pattern.sub(repl, value))


@register.simple_tag(name="search_filter_form", takes_context=True)
def get_search_filter_form(context):
    
    form = Form(initial=context['search_params'])
    form.fields['q'] = fields.CharField(label = 'contains query')
    
    category_id = context['search_params'].get('category', None)
    djangofields = {}
    if category_id:
        category = ProductCategory.objects.get(slug=category_id)
        for key, field in category.get_extra_fields().items():
            djangofields[field['solr_key']] = field['field'] 
    
    djangofields['price'] = models.IntegerField(verbose_name='Price')
    djangofields['has_image'] = models.BooleanField(verbose_name='Has Image')

    for key, field in djangofields.items():
        #print field.__class__.__name__
        if isinstance(field, models.IntegerField):
            form.fields['filter[%s_from]' % key] = fields.IntegerField(label = field.verbose_name + ' from')
            form.fields['filter[%s_to]' % key] = fields.IntegerField(label = field.verbose_name + ' to')
        elif isinstance(field, models.FloatField):
            form.fields['filter[%s_from]' % key] = fields.FloatField(label = field.verbose_name + ' from')
            form.fields['filter[%s_to]' % key] = fields.FloatField(label = field.verbose_name + ' to')
        else:
            form.fields['filter[%s]' % key] = field.formfield()
        
    #form.fields['color'] = fields.IntegerField()
    return form.as_ul()
