from django import template

register = template.Library()

@register.filter
def number_items(value, number):
    return value[:number]

@register.filter
def rate_stars(value):
    return     "★" * value


