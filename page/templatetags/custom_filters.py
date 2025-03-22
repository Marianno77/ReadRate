from django import template
import math

register = template.Library()

@register.filter
def full_stars(rating):
    return range(int(rating))

@register.filter
def half_star(rating):
    return range(rating - int(rating) >= 0.5)

@register.filter
def empty_stars(rating):
    return range(5 - math.floor(rating) - (1 if rating - math.floor(rating) >= 0.5 else 0))

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)