import os

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.shortcuts import redirect
from django.conf import settings

from views import shop

urlpatterns = patterns('',
    url(r'', include(shop.urls)),    
    url(r'^products/(?P<category_slug>[A-Za-z0-9\-]*)$', 'cadoshop.views.product_list', name='product_list'),
    url(r'^product/(?P<product_slug>[A-Za-z0-9\-]*)/$', 'cadoshop.views.product_detail', name='product_detail'),
    
    url(r'^extrafields/(?P<category_id>\d+)$', 'cadoshop.views.extrafields', name='extrafields'),
    
    url(r'^reporting/', include('plata.reporting.urls')),
                    
 )
