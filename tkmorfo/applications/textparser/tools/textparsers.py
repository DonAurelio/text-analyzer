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
	Takes texts, applies the Stanford Parser and return the 
	corresponding parce trees.

	sentences:: str a text
	Return type:: iter(iter(Tree)) parce trees one for each sentence in a text
	"""
	# sent_tokenize is a text segmenter, it takes str and returns list(str)
	# st_parser.raw_parse_sents is a StanforParser, it takes list(list(str))
	# and returns a parse tree iter(iter(Tree))
	parse_trees = list(list( st_parser.raw_parse_sents(sent_tokenize(sentences)) ))
	raw_parse_trees = [str(list(tree)[0]) for tree in parse_trees]
	return raw_parse_trees

def stanford_parse_from_file(inputfile, outputfile):
	"""
	Reads a file located in 'input' file path, create the parse trees
	corresponding with each sentences in the text from the given input
	file and save the result in an output path 

	inputfile:: str complete path to an input file
	outputfile:: str complete path to an output file
	Return type:: iter(iter(Tree)) parce trees one for each sentence in a text
	"""
	# Reading the input text file
	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line '.START' present in all 00-raw files
		sentences = f.read()

	# Parsing the gievn text
	raw_parse_trees = stanford_parser(sentences)

	# Writting the resulting parse trees in a given outputfile
	with open(outputfile, 'w') as f:
		for t in raw_parse_trees:
			f.write(t.replace("ROOT", "")+"\n")

	return raw_parse_trees

def to_bikel_format(tagged_sents):
	"""
	Converts to bikel format (bracketing). Takes multiple sentences where each
	sentence is a list of (word, tag) tuples.
	
	Parameters:: tagged_sents (list(list(tuple(str, str))))
	Return type:: (str)
	"""
	result = ""
	for sentence in tagged_sents:
		result += "("
		for item in sentence:
			result = result + "("+item[0]+" "+"("+item[1]+")) "
		result += ") "
	return result

def raw_tag(text):
	"""
	Tags multiple sentences. Takes multiple sentences as a String; before
	tagging, it will be automatically segmented and tokenized
	
	Parameters:: text (str) 
	Return type:: (list(list(tuple(str, str))))
	"""
	sentences = sent_tokenize(text) # Segment sentences
	tokenized_sentences = [st_tknzr.tokenize(s) for s in sentences] # Tokenizer
	result = st_tagger.tag_sents(tokenized_sentences) # PosTagger
	return result

def bikel_parser(sentences):
	"""
	Recibe un conjunto de sentencias en un string, aplica el parser de bikel
	y retorna el árbol sintáctico. No deja archivos residuales
	"""

	# Bikel text preprocessing 
	segmented_sents = sent_tokenize(sentences)
	raw_segmented_sents = '\n'.join(segmented_sents)
	raw_tagged_sents = raw_tag(raw_segmented_sents) # tag raw text 
	raw_bracketed_tagged_sents = to_bikel_format(raw_tagged_sents)

	# Save the preprocessing text into a file inside 'helpers' directory
	# to execute the java bikel by os console an process that file
	temp_file = abs_path + '/input' + '.bkl'

	with open(temp_file, 'w') as f:
		f.write(raw_bracketed_tagged_sents)

	cmd = bk_parser_path + " 400 " + bk_settings + " " + bk_parser_model + " " + temp_file
	os.popen(cmd).read() # writes the file '.parsed' given by the bikel parser
	os.remove(temp_file)

	# dbparser implementation creates a file with '.parsed' extension
	# so we read that file to get the parse trees generated
	result_file = abs_path + '/input' + '.bkl' + '.parsed'
	parse_trees = []
	with open(result_file, 'r') as f:
		for line in f:
			parse_trees.append(Tree.fromstring(line))
	os.remove(result_file)

	raw_parse_trees = [str(tree) for tree in parse_trees]

	# return the preprocessing the text (raw_bracketed_tagged_sents)
	# and the generated trees
	return raw_bracketed_tagged_sents , raw_parse_trees
	

def bikel_parse_from_file(inputfile,outputfile):
	# Lee el archivo de entrada, aplica pos_tag, guardar archivo auxiliar,
	# ejecuta comando para parser bikel, guarda salida en archivo final
	# (inputfile.bkl.parse)

	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line | .START
		sentences = f.read()


	raw_bracketed_tagged_sents , raw_parse_trees = bikel_parser(sentences)

	# Tagged_sents: list(list(tuple)), list(tuple) is a sentence and tuple is a (word,postag)
	tagged_sents = raw_tag(sentences)
	temp_file = inputfile+'.bkl'
	bracketed_sentences = None
	with open(outputfile, 'w') as f:
		for raw_tree in raw_parse_trees:
			f.write(raw_tree)

	cmd = bk_parser_path + " 400 " + bk_settings + " " + bk_parser_model + " " + temp_file
	os.popen(cmd).read()

	return raw_bracketed_tagged_sents, raw_parse_trees

def get_raw_files_list():
	files = list(os.walk(abs_path + '/00-raw/'))[0][2]
	files.remove('.gitignore')
	return files

def execute_parseval(raw_file_name):
	raw_file_path = abs_path + '/00-raw/' + raw_file_name
	gold_file_path = abs_path + '/00/' + raw_file_name + '.mrg'
	# To check if the path contains an existing file:
	if not os.path.isfile(gold_file_path):
		gold_file_path = abs_path + '/00/' + raw_file_name.split('_')[0] + '_0' +\
		raw_file_name.split('_')[1] + '.mrg'
	bikel_parsed_file = abs_path + '/parseval/testfiles/' + raw_file_name + '.bkl.parsed'
	stanford_parsed_file = abs_path + '/parseval/testfiles/' + raw_file_name + '.stf.parsed'

	stanford_result = stanford_parse_from_file(raw_file_path, stanford_parsed_file)
	bikel_result = bikel_parse_from_file(raw_file_path, bikel_parsed_file)
	model = Modelo()
	l=[0, '-c']

	# Average precision, recall,  cross brackets and F-score:'
	pre1, re1, crossing1, fscore1 = model.parseval(stanford_parsed_file, gold_file_path, l)
	pre2, re2, crossing2, fscore2 = model.parseval(bikel_parsed_file, gold_file_path, l)
	
	# os.remove(stanford_parsed_file)
	# os.remove(bikel_parsed_file)

	stanford = { 'pre':pre1,'re':re1,'fscore':fscore1,'result':stanford_result }
	bikel = { 'pre':pre2,'re':re2,'fscore':fscore2,'result':bikel_result }

	results = (stanford,bikel)

	return results