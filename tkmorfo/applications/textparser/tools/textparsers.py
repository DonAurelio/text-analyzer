# -*- coding: utf-8 -*-
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import Tree
from helpers.utils import *
#===============================================================================
# functions

def stanford_parser(text):
	"""
	* sent_tokenize is a text segmenter, it takes str and returns list(str), where each str is a sentence.
	* st_parser.raw_parse_sents is a StanforParser, it takes list(list(str)) and returns and returns a parse tree 
	iter(iter(Tree)).
	"""
	return list(list( st_parser.raw_parse_sents(sent_tokenize(text)) ))


def stanford_parser_outfile(inputfile, outputfile):
	with open(inputfile, 'r') as f:
		f.readline() # Skip the first line | .START
		sentences = f.read()
	trees = stanford_parser(sentences)
	with open(outputfile, 'w') as f:
		for t in list(trees):
			f.write(str(list(t)[0]).replace("ROOT", "")+"\n")

def raw_tag(text):
	sentences = sent_tokenize(text) # Segment sentences
	tokenized_sentences = [st_tknzr.tokenize(s) for s in sentences] # Tokenizer
	result = st_tagger.tag_sents(tokenized_sentences) # PosTagger
	return result

def to_bikel_format(tagged_sents):
	result = ""
	for sentence in tagged_sents:
		result += "("
		for item in sentence:
			result = result + "("+item[0]+" "+"("+item[1]+")) "
		result += ") "
	return result

def bikel_parser(sentences):
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

if __name__ == "__main__":
	s = 'Pierre Vinken, 61 years old, will join the board as a nonexecutive director Nov. 29.'

	# demo()
	inputfile = abs_path + '/wsj_0011'
	outputfile_st = abs_path + '/wsj_0011.stf.parsed'
	outputfile_bk = abs_path + '/wsj_0011.bkl.parsed'
	#stanford_parser_outfile(inputfile, outputfile_st)
	#bikel_parser_outfile(inputfile)
	bikel_parser(s)