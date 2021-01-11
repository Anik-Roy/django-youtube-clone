from django import template

register = template.Library()


def range_filter(value):
    return value[:200]+'...'


def first_character(value):
    return value[:1]


register.filter('range_filter', range_filter)
register.filter('first_character', first_character)