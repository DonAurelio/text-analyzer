# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView
from tools.bikelpreprocessing import split_sentence

class ParserView(TemplateView):
	template_name = 'textparser/index.html'

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		split_sentence(text)
