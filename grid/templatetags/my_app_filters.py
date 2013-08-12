from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='spacify')
def spacify(value):

	return_string=value.replace(" ", "+")
	return return_string

@register.filter(name='dollarize')
def dollarize(value):
	return '$'*(value+1)


