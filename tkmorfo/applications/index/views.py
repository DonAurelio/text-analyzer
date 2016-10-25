# -*- encoding: utf-8 -*-

import json
from tools import tkmorfo 
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
	template_name = 'index/index.html'

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		tokens = tkmorfo.tokenizar(text)
		#pre_analisis = tkmorfo.parse_sentence(tkmorfo.pre_mf_analyze(tokens))

		# Anaĺisis morfológico
		morfo_analisis = tkmorfo.parse_sentence(tkmorfo.morfo_analyze(tokens))
		group_len = 6
		morfo_analisis_groups = [ morfo_analisis[i:i+group_len] for i in range(0, len(morfo_analisis), group_len) ]
		print "TOKENS",tokens
		print "MORFO ANALISIS",morfo_analisis
		print "MORFO ANALISIS GROUPS", morfo_analisis_groups
		
		template = loader.get_template('index/includes/result.html')
		context = {'tokens':tokens,'morfo_analisis_groups':morfo_analisis_groups }
		html = template.render(context)

		# Si el campo de texto está vacio entonces se retorna false
		if len(text) == 0:
			respuesta = {'status':False,'html':html}
		else:
			respuesta = {'status':True,'html':html}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')