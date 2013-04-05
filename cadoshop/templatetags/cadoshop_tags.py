from django import template
from django.core.urlresolvers import reverse
import urllib
register = template.Library()

@register.simple_tag(name="search_url", takes_context=True)
def get_search_url(context, category=None, tag=None, page=1):
    
    urlparams = {}
    urlparams['category'] = category if category is not None else context['search_params'].get('category', None)
    urlparams['tags'] = tag if tag is not None else context['search_params'].get('tags', None)
    urlparams['page'] = page if page is not None else context['search_params'].get('page', None)
        
    urlparams = dict((k,v) for k,v in urlparams.iteritems() if v is not None)
    if (urlparams['page'] == 1):
        del urlparams['page']
    
    return reverse('product_list') + '?' + urllib.urlencode(urlparams)