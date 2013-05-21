'''
This is loosly based on Derek Schaefer's django-json-field:
https://github.com/derek-schaefer/django-json-field
'''

from django.forms import fields
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

### DONT REMOVE BEFORE ALL MIGRATIONS
from cadocms.fields import ExtraFieldsValues, ExtraFieldsDefinition
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^cadoshop\.fields\.ExtraFieldsDefinition"])
add_introspection_rules([], ["^cadoshop\.fields\.ExtraFieldsValues"])
###

from widgets import ColorPickerWidget

class ColorsField(models.CharField):
    """
    A text field made to accept hexadecimal color value (#FFFFFF)
    with a color picker widget.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(ColorsField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorsField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^cadoshop\.fields\.ColorsField"])
except ImportError:
    pass

