# -*- encoding: utf-8 -*-

import json
from tools import tkmorfo
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView


class MorfoView(TemplateView):
	template_name = 'morfo/index.html'

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		pre = False if request.POST.get('pre',None) else True
		tokens = tkmorfo.tokenizar(text)
		# Anaĺisis morfológico
		morfo_analisis = tkmorfo.parse_sentence(tkmorfo.morfo_analyze(listatokens=tokens,full_analize=pre))
		template = loader.get_template('morfo/includes/result.html')
		context = {'tokens':tokens,'morfo_analisis':morfo_analisis }
		html = template.render(context)

		# Si el campo de texto está vacio entonces se retorna false
		if len(text) == 0:
			respuesta = {'status':False,'html':html}
		else:
			respuesta = {'status':True,'html':html}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')
