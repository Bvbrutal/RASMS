#coding=utf-8
from django import template

register = template.Library()

@register.filter(name='custom_filter')
def reverse_list(value):
    return reversed(value)


@register.filter(name='activity_filter')
def activity_filter(value):
    if value==0:
        return "无限制"
    return value