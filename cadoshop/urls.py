import os

from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from django.shortcuts import redirect
from django.conf import settings

from views import shop

urls = patterns('',
    url(r'', include(shop.urls)),    
    url(r'^products/$', 'cadoshop.views.product_list', name='product_list'),
    url(r'^product/(?P<object_id>\d+)/$', 'cadoshop.views.product_detail', name='product_detail'),
    
    url(r'^extrafields/(?P<category_id>\d+)$', 'cadoshop.views.extrafields', name='extrafields'),
    
    url(r'^reporting/', include('plata.reporting.urls')),
                    
 )
