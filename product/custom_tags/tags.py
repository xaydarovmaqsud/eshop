from django import template

from product.models import Category

register=template.Library()

@register.simple_tag('add')
def add(value,v1):
    return value + v1


@register.simple_tag
def Cat(category):
    choise=Category.objects.all()
    return choise