# coding=utf-8
from django import template

register = template.Library()


@register.filter(name='custom_filter')
def reverse_list(value):
    return reversed(value)


@register.filter(name='activity_filter')
def activity_filter(value):
    # 查看value值
    # print(value, type(value))
    if value == 0 or value is None:
        return "无限制"
    return value
