# -*- encoding: utf-8 -*-
import json
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from tools.textparsers import stanford_parser
from tools.textparsers import raw_tag, to_bikel_format, bikel_parser
from tools.textparsers import get_raw_files_list
from tools.textparsers import execute_parseval
from tools.parsetreeimage import save_image_from_tree

class ParserView(TemplateView):
	template_name = 'textparser/index.html'

	def get_context_data(self,**kwargs):
		context = super(ParserView,self).get_context_data(**kwargs)
		context['raw_files'] = get_raw_files_list()
		print "RAW FILES", context['raw_files']
		return context

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		mode = request.POST.get('radio-modo',None)
		model = request.POST.get('radio-modelo',None)
		rawfile = request.POST.get('rawfile',None)
		
		# Options given by the user throut the template
		print "Form Data:", text, mode, model, rawfile

		# Text Processing
		parse_trees = None
		raw_parse_trees = None
		paths_to_tree_images = None
		has_preprocessing = None
		has_precision_and_recall = None

		if model == "Standfor" and mode == "Analisis":
			parse_trees = stanford_parser(text)
			raw_parse_trees = [str(list(tree)[0]) for tree in parse_trees]
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

		if model == "Bikel" and mode == "Analisis":
			parse_trees = bikel_parser(text)
			print "BIKEL:", parse_trees
			raw_parse_trees = [str(tree) for tree in parse_trees]
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

		if model == "Standfor" and mode == "Test":
			execute_parseval(rawfile)





		# Template Rendetization
		template = loader.get_template('textparser/includes/result_analisys.html')
		context = {
			'has_preprocessing':has_preprocessing,
			'has_precision_and_recall':has_precision_and_recall,
			'raw_parse_trees':raw_parse_trees,
			'paths_to_tree_images':paths_to_tree_images
		}
		html = template.render(context)

		# Text validations, if the text field is empty, we return and error or
		# False status
		if len(text) == 0:
			respuesta = {'status':False,'html':html}
		else:
			respuesta = {'status':True,'html':html}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')
		
