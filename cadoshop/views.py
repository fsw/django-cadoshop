from django import forms
from django.forms import fields
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import list_detail
from django.core.paginator import Paginator, InvalidPage

from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.views import Shop
from plata.shop.models import Order
from django.forms.forms import Form
from django.http import HttpResponse

from models import Product, ProductCategory

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

def frontend_context(request): 
    context = {}
    order = shop.order_from_request(request)
    context['user_order'] = order
    context['user_contact'] = shop.contact_from_user(request.user)
    context['user_order_total'] = order.items.count() if order else 0
    all_facets = SearchQuerySet().facet('category').facet('tags').facet_counts()['fields']
    
    context['tags'] = {}
    for tag, count in all_facets['tags']:
        context['tags'][tag] = {'total':count, 'count':count}
    categories_map = {}
    for category, count in all_facets['category']:
        categories_map[category] = count
        
    categories = ProductCategory.objects.all()
    context['categories'] = [];
    for category in categories:
        category.total = categories_map.get(category.slug, 0)
        category.count = category.total
        context['categories'].append(category)
    
    context['search_params'] = {};
    
    #print request
    #print context['facet']
    return context

shop = Shop(Contact, Order, Discount)

def extrafields(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    form = Form()
    for key, field in category.get_extra_form_fields().items():
        form.fields['extra[%s]' % key] = field
    return HttpResponse(form.as_p())



def product_list(request):
    context = {}
    if request.method == 'POST':
        order = shop.order_from_request(request, create=True)
        try:
            order.modify_item(Product.objects.get(id=request.POST.get('product')), int(request.POST.get('count')))
            messages.success(request, _('The cart has been updated.'))
        except ValidationError, e:
            if e.code == 'order_sealed':
                [messages.error(request, msg) for msg in e.messages]
            else:
                raise
        return redirect(request.get_full_path())

    results_per_page = 5
    results = SearchQuerySet()
    results = results.facet('category')
    results = results.facet('tags')
    #results.facet('tags')
    
    context['search_params'] = dict((key, request.GET.get(key, None)) for key in ['q', 'page', 'category', 'tag'] )
    
    if 'q' in request.GET and request.GET['q']:
        results = results.filter(text=AutoQuery(request.GET['q']))
    
    if 'category' in request.GET and request.GET['category']:
        results = results.filter(category=request.GET['category'])
        
    if 'tags' in request.GET and request.GET['tags']:
        tags = request.GET['tags'].split(',')
        for tag in tags:
            results = results.filter(tags=tag)
    
    context['facet'] = results.facet_counts()['fields']

    results = results.load_all()
    try:
        page_no = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        raise Http404("Not a valid number for page.")

    if page_no < 1:
        raise Http404("Pages should be 1 or greater.")

    start_offset = (page_no - 1) * results_per_page
    results[start_offset:start_offset + results_per_page]

    paginator = Paginator(results, results_per_page)

    try:
        page = paginator.page(page_no)
    except InvalidPage:
        raise Http404("No such page!")

    for result in results:
        extra = []
        for key,item in result._object.category.extra_fields.items():
            extra.append({'label':key, 'value':result._object.extra.get(key, 'ASD') }) 
        result.extra = extra
    context['results'] = results
    context['page'] = page
    context['search'] = request.GET
    #print page
    #Product.objects.filter(is_active=True)
    return render_to_response('product/list.html', context, context_instance=RequestContext(request))



class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(label=_('quantity'), initial=1,
        min_value=1, max_value=100)
    



def product_detail(request, object_id):
    product = get_object_or_404(Product.objects.filter(is_active=True), pk=object_id)

    if request.method == 'POST':
        form = OrderItemForm(request.POST)

        if form.is_valid():
            order = shop.order_from_request(request, create=True)
            try:
                order.modify_item(product, form.cleaned_data.get('quantity'))
                messages.success(request, _('The cart has been updated.'))
            except ValidationError, e:
                if e.code == 'order_sealed':
                    [messages.error(request, msg) for msg in e.messages]
                else:
                    raise

            return redirect('plata_shop_cart')
    else:
        form = OrderItemForm()
    
    context = {};
    context['object'] = product
    context['form'] = form
    return render_to_response('product/detail.html', context, context_instance=RequestContext(request))