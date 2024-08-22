from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='add_id')
def add_id(field, id_value):
    return field.as_widget(attrs={"id": id_value})
