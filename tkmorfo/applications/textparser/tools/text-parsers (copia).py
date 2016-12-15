# -*- coding: utf-8 -*-
# import nltk
# nltk.download('punkt')
from nltk import sent_tokenize
from nltk import Tree

from nltk.parse.stanford import StanfordParser
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
from os.path import dirname
from os.path import abspath
import os

#===============================================================================
abs_path = dirname(abspath(__file__))

# STANFORD TOOLS

# paths
stanford_pos_dir = abs_path + '/stanford-postagger-2015-12-09/'
postag_modelfile = stanford_pos_dir+'models/english-bidirectional-distsim.tagger'
postag_jar = stanford_pos_dir + 'stanford-postagger.jar'
stanford_parser_dir = abs_path + '/stanford-parser-full-2015-12-09/'
parser_eng_model = stanford_parser_dir+'edu.stanford.nlp.models.lexparser/englishPCFG.ser.gz'
parser_models_jar = stanford_parser_dir + "stanford-parser-3.6.0-models.jar"
parser_jar = stanford_parser_dir + "stanford-parser.jar"

# Instances:
st_tagger = StanfordPOSTagger(model_filename = postag_modelfile,
							 path_to_jar = postag_jar)

st_tknzr  = StanfordTokenizer(path_to_jar = postag_jar)

st_parser = StanfordParser(model_path = parser_eng_model,
						   path_to_models_jar = parser_models_jar,
						   path_to_jar = parser_jar)

# BIKEL

# paths
bikel_dir = abs_path + '/dbparser/'
bk_parser_path = bikel_dir+'bin/parse'
bk_settings = bikel_dir+'settings/collins.properties'
bk_parser_model = bikel_dir+'bikel/wsj-02-21.obj.gz'
# cmd = bikel_parser+" 400"+bk_settings+" "+bk_parser_model + inputfile
#===============================================================================

#===============================================================================
# functions

def stanford_parser(sentences):
	"""
	Recibe un conjunto de sentencias, aplica el parser de stanford
	y retorna el árbol sintáctico // en bracketing -> list(tree)
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
	

def bikel_parser_outfile(inputfile):
	# Leer archivo, aplicar pos_tag, guardar archivo auxiliar,
	# ejecutar comando, guarda salida en archivo final (inputfile.bkl.parse)

	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line | .START
		sentences = f.read()
	tagged_sents = raw_tag(sentences)
	temp_file = inputfile+'.bkl'
	with open(temp_file, 'w') as f:
		f.write(to_bikel_format(tagged_sents))
	cmd=bk_parser_path+" 400 "+bk_settings+" "+bk_parser_model+" "+temp_file
	os.popen(cmd).read()
	os.remove(temp_file)
	
#===============================================================================


#===================================  DEMO =====================================
def demo():
	s = 'Pierre Vinken, 61 years old, will join the board as a nonexecutive \
		 director Nov. 29.'
	
	print "raw_tag:\n", (raw_tag(s))

	#  raw_parse: to parse a sentence. Takes a sentence as a string
	print "raw_parse:\n", list(st_parser.raw_parse(s))
	print tagged_parse_sents()

	# raw_parse_sents
	# print "raw_parse_sents:\n", list(list(st_parser.raw_parse_sents(sent_tokenize(s)))[0])

	# tagged_parse_sents:  to parse multiple sentences
	# print "tagged_parse_sents:\n", list(list(st_parser.tagged_parse_sents(raw_pos_tag(s)))[0])

	#main()
	inputfile = abs_path + '/wsj_0011'
	outputfile_st = abs_path + '/wsj_0011.stf.parsed'
	outputfile_bk = abs_path + '/wsj_0011.bkl.parsed'
	#stanford_parser_outfile(inputfile, outputfile_st)
	bikel_parser_outfile(inputfile, outputfile_bk)
#===============================================================================
	
if __name__ == "__main__":
	s = 'Pierre Vinken, 61 years old, will join the board as a nonexecutive director Nov. 29.'

	m = "South Korea registered a trade deficit of $101 million in October, reflecting the country's economic sluggishness, according to government figures released Wednesday. \
Preliminary tallies by the Trade and Industry Ministry showed another trade deficit in October, the fifth monthly setback this year, casting a cloud on South Korea's export-oriented economy. \
\
Exports in October stood at $5.29 billion, a mere 0.7% increase from a year earlier, while imports increased sharply to $5.39 billion, up 20% from last October. \
\
South Korea's economic boom, which began in 1986, stopped this year because of prolonged labor disputes, trade conflicts and sluggish exports.\
Government officials said exports at the end of the year would remain under a government target of $68 billion. \
\
Despite the gloomy forecast, South Korea has recorded a trade surplus of $71 million so far this year. \
\
From January to October, the nation's accumulated exports increased 4% from the same period last year to $50.45 billion.\
Imports were at $50.38 billion, up 19%. "

	# demo()
	inputfile = abs_path + '/wsj_0011'
	outputfile_st = abs_path + '/wsj_0011.stf.parsed'
	outputfile_bk = abs_path + '/wsj_0011.bkl.parsed'
	#stanford_parser_outfile(inputfile, outputfile_st)
	#bikel_parser_outfile(inputfile)
	bikel_parser(m)
