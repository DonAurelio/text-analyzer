# -*- encoding: utf-8 -*-

import json
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
	template_name = 'index/index.html'

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		preporcesamiento = 'Preprocesamiento'
		tokenización = 'Tokenización'
		analisis = 'Analisis Morfologico'
		template = loader.get_template('index/includes/result.html')
		context = {}
		html = template.render(context)

		# Si el campo de texto está vacio entonces se retorna false
		if len(text) == 0:
			respuesta = {'status':False,'html':html}
		else:
			respuesta = {'status':True,'html':html}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')