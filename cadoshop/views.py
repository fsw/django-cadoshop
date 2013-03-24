from django import forms
from django.forms import fields
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import list_detail

from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.views import Shop
from plata.shop.models import Order
from django.forms.forms import Form
from django.http import HttpResponse

from models import Product, ProductCategory

shop = Shop(Contact, Order, Discount)

def extrafields(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    form = Form()
    for key, field in category.extra_fields.items():
        methodToCall = getattr(fields, field.get('class', 'CharField'), fields.CharField)
        field = fields.CharField(**field.get('args', {}))
        #'CharField','IntegerField','DateField','TimeField','DateTimeField','RegexField',
        #'EmailField','FileField','ImageField','URLField','BooleanField','ChoiceField',
        #'MultipleChoiceField','FloatField','DecimalField','SplitDateTimeField','IPAddressField',
        #'GenericIPAddressField','FilePathField','SlugField','TypedChoiceField','TypedMultipleChoiceField'
        form.fields['extra[%s]' % key] = field
    return HttpResponse(form.as_p())

def frontend_context(): 
    return {
        'categories' : ProductCategory.objects.all(),
    }

def product_list(request):
    print 'asf'
    return list_detail.object_list(request,
        queryset = Product.objects.filter(is_active=True),
        template_name = 'product/list.html',
        extra_context = frontend_context()
    )

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
    
    context = frontend_context();
    context['object'] = product
    context['form'] = form
    return render_to_response('product/detail.html', context, context_instance=RequestContext(request))