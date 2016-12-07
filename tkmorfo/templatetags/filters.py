# -*- encoding: utf-8 -*-

from django import template
from applications.morfo.tools import eagle
register = template.Library()

@register.filter(name='interpretag')
def zip_lists(etiqueta_eagle):
	return eagle.interpretar(etiqueta_eagle)
