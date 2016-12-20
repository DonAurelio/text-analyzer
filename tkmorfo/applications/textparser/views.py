# -*- encoding: utf-8 -*-
import json
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from tools.textparsers import stanford_parser
from tools.textparsers import raw_tag, to_bikel_format, bikel_parser
from tools.textparsers import get_raw_files_list
from tools.parsetreeimage import save_image_from_tree

class ParserView(TemplateView):
	template_name = 'textparser/index.html'

	def get_context_data(self,**kwargs):
		context = super(ParserView,self).get_context_data(**kwargs)
		context['raw_files'] = sorted(get_raw_files_list())
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
		preprocessing = None
		raw_parse_trees = None
		paths_to_tree_images = None
		has_preprocessing = None
		has_precision_and_recall = None

		if model == "Standfor" and mode == "Analisis" and len(text) != 0:
			parse_trees = stanford_parser(text)
			raw_parse_trees = [str(list(tree)[0]) for tree in parse_trees]
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

		if model == "Bikel" and mode == "Analisis" and len(text) != 0:
			preprocessing ,parse_trees = bikel_parser(text)
			raw_parse_trees = [str(tree) for tree in parse_trees]
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

		if mode == "Test" and len(text) != 0:
			pass
			
		# Template Rendetization
		template = loader.get_template('textparser/includes/result_analisys.html')
		context = {
			'preprocessing':preprocessing,
			'has_precision_and_recall':has_precision_and_recall,
			'raw_parse_trees':raw_parse_trees,
			'paths_to_tree_images':paths_to_tree_images
		}
		html = template.render(context)

		# Text validations, if the text field is empty, we return and error or
		# False status
		respuesta = {
		'status':False if len(text) == 0 else True,
		'html':html }

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')
		
