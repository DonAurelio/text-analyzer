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
		raw_parse_trees = None
		preprocessing = None
		raw_parse_trees = None
		paths_to_tree_images = None
		has_preprocessing = None
		has_precision_and_recall = None
		context = {}
		template = None
		html = None
		status = None

		if model == "Standfor" and mode == "Analisis" and len(text) != 0:
			status = False if len(text) == 0 else True
			raw_parse_trees = stanford_parser(text)
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))
		
			context['preprocessing'] = preprocessing
			context['raw_parse_trees'] = raw_parse_trees
			context['paths_to_tree_images'] = paths_to_tree_images

		if model == "Bikel" and mode == "Analisis" and len(text) != 0:
			status = False if len(text) == 0 else True
			preprocessing ,raw_parse_trees = bikel_parser(text)
			paths_to_tree_images = []
			has_preprocessing = None
			has_precision_and_recall = None
			for i,raw_tree in enumerate(raw_parse_trees):
				paths_to_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

			context['preprocessing'] = preprocessing
			context['raw_parse_trees'] = raw_parse_trees
			context['paths_to_tree_images'] = paths_to_tree_images

		if mode == "Test":
			status = True
			stanford, bikel = execute_parseval(rawfile)

			context['stanford'] = stanford
			s_raw_parse_trees = stanford['result']
			stanford_tree_images = []
			for i,raw_tree in enumerate(s_raw_parse_trees):
				stanford_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='standfor'))

			context['stanford_tree_images'] = stanford_tree_images

			context['bikel'] = bikel
			bikel_tree_images = []
			b_raw_parse_trees = bikel['result'][1]
			for i,raw_tree in enumerate(b_raw_parse_trees):
				bikel_tree_images.append(save_image_from_tree(
					raw_tree=raw_tree,name='s%d'% i,type='bikel'))

			context['bikel_tree_images'] = bikel_tree_images


		# Template Rendetization
		if mode == "Analisis":
			template = loader.get_template('textparser/includes/result_analisys.html')
			print "A1"
		else:
			template = loader.get_template('textparser/includes/result_test.html')
			print "A2"
		html = template.render(context)

		# Text validations, if the text field is empty, we return and error or
		# False status
		respuesta = {
		'status':status,
		'html':html 
		}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')
		
