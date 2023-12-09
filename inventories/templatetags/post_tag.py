from django import template

register = template.Library()

@register.simple_tag
def sub(a, b, c):
    return a - b - c
