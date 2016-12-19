# -*- coding: utf-8 -*-
import nltk
#nltk.download('punkt')
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import Tree
from helpers.utils import *
from helpers.parseval.parseval import Modelo 
#===============================================================================
# functions

def stanford_parser(sentences):
	"""
	Takes multiple sentences as a String (sentences), applies the Stanford Parser
	and return the trees parsed 

	* sent_tokenize is a text segmenter, it takes str and returns list(str),
		where each str is a sentence.
	* st_parser.raw_parse_sents is a StanforParser, it takes list(list(str))
		and returns and returns a parse tree 
		iter(iter(Tree)).
	"""
	return list(list( st_parser.raw_parse_sents(sent_tokenize(sentences)) ))


def stanford_parser_outfile(inputfile, outputfile):
	"""
	Lee el archivo de entrada input, genera el árbol sintáctico utilizando
	el stanford_parser, guarda el resultado en el archivo output
	"""
	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line | .START
		sentences = f.read()
	trees = stanford_parser(sentences)
	with open(outputfile, 'w') as f:
		for t in list(trees):
			f.write(str(list(t)[0]).replace("ROOT", "")+"\n")

def raw_tag(text):
	"""
	Tags multiple sentences. Takes multiple sentences as a String; before
	tagging, it will be automatically segmented and tokenized
	
	Parameters:	text (str) 
	Return type:	(list(list(tuple(str, str))))
	"""
	sentences = sent_tokenize(text) # Segment sentences
	tokenized_sentences = [st_tknzr.tokenize(s) for s in sentences] # Tokenizer
	result = st_tagger.tag_sents(tokenized_sentences) # PosTagger
	return result

def to_bikel_format(tagged_sents):
	"""
	Converts to bikel format (bracketing). Takes multiple sentences where each
	sentence is a list of (word, tag) tuples.
	
	Parameters: tagged_sents (list(list(tuple(str, str))))
	Return type: (str)
	"""
	result = ""
	for sentence in tagged_sents:
		result += "("
		for item in sentence:
			result = result + "("+item[0]+" "+"("+item[1]+")) "
		result += ") "
	return result

def bikel_parser(sentences):
	"""
	Recibe un conjunto de sentencias en un string, aplica el parser de bikel
	y retorna el árbol sintáctico. No deja archivos residuales
	"""
	temp_file = abs_path + '/input'
	segmented_sents = sent_tokenize(sentences)
	with open(temp_file, 'w') as f:
		f.write(".START \n")
		for sent in segmented_sents:
			f.write(sent+"\n")
	bikel_parser_outfile(temp_file)
	os.remove(temp_file)

	output_file = abs_path+'/input'+'.bkl.parsed'
	trees = []
	with open(output_file, 'r') as f:
		for line in f:
			trees.append(Tree.fromstring(line))
	os.remove(output_file)
	return trees
	

def bikel_parser_outfile(inputfile, outputfile):
	# Lee el archivo de entrada, aplica pos_tag, guardar archivo auxiliar,
	# ejecuta comando para parser bikel, guarda salida en archivo final
	# (inputfile.bkl.parse)
	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line | .START
		sentences = f.read()
	tagged_sents = raw_tag(sentences)
	temp_file = inputfile+'.bkl'
	with open(temp_file, 'w') as f:
		f.write(to_bikel_format(tagged_sents))
	cmd=bk_parser_path+" 400 "+bk_settings+" "+bk_parser_model+" "+temp_file
	os.popen(cmd).read()
	print(temp_file+'.parsed')
	os.rename(temp_file+'.parsed',outputfile)
	os.remove(temp_file)

def get_raw_files_list():
	files = list(os.walk(abs_path + '/00-raw/'))[0][2]
	files.remove('.gitignore')
	return files

def execute_parseval(raw_file_name):
	raw_file_path = abs_path + '/00-raw/' + raw_file_name
	gold_file_path = abs_path + '/00/' + raw_file_name + '.mrg'
	# To check if a path is an existing file:
	if not os.path.isfile(gold_file_path):
		gold_file_path = abs_path + '/00/' + raw_file_name.split('_')[0] + '_0' +\
		raw_file_name.split('_')[1] + '.mrg'
	bikel_parsed_file = abs_path + '/parseval/test/' + raw_file_name + '.bkl.parsed'
	stanford_parsed_file = abs_path + '/parseval/test/' + raw_file_name + '.stf.parsed'

	stanford_parser_outfile(raw_file_path, stanford_parsed_file)
	#bikel_parser_outfile(raw_file_path, bikel_parsed_file)

	print gold_file_path
	model = Modelo()
	l=[0, '-c']

	# Average precision, recall,  cross brackets and F-score:'
	pre1, re1, crossing, fscore = model.parseval(stanford_parsed_file, gold_file_path, l)
	# parseval(bikel_parsed_file, gold_file_path)

#===============================================================================