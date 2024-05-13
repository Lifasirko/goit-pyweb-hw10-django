from django import template

register = template.Library()

@register.filter(name='split')
def split_string(value, key):
    """
    Повертає значення перетворене в список.
    """
    return value.split(key)
