from django import template
from django.core.urlresolvers import reverse
import urllib
register = template.Library()
import re
from django.utils.safestring import mark_safe

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

@register.filter
def urlize_hashtags(value):
    def repl(m):
        hashtag = m.group(1)
        url = reverse('product_list') + '?tags=' + hashtag
        return '<a href="%s">&#35;%s</a>' % (url, hashtag)
    hashtag_pattern = re.compile(r'[#]+([-_a-zA-Z0-9]+)')
    return mark_safe(hashtag_pattern.sub(repl, value))