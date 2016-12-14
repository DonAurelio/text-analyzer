# -*- coding: utf-8 -*-
# import nltk
# nltk.download('punkt')
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
from nltk import sent_tokenize
from os.path import dirname
from os.path import abspath

#===============================================================================
# STANFORD TOOLS

abs_path = dirname(abspath(__file__))
stanford_pos_dir = abs_path + '/stanford-postagger-2015-12-09/'
postag_modelfile = stanford_pos_dir+'models/english-bidirectional-distsim.tagger'
postag_jar = stanford_pos_dir + 'stanford-postagger.jar'
stanford_parser_dir = abs_path + '/stanford-parser-full-2015-12-09/'
# parser_eng_model = stanford_parser_dir+'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
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
#===============================================================================

#===============================================================================
# functions
def raw_pos_tag(text):
	"""
	Takes multiple sentences as a String
	
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
#===============================================================================


#=============================== MAIN -> TEST ==================================
def main():
	s = 'Pierre Vinken, 61 years old, will join the board as a nonexecutive \
		 director Nov. 29.'
	print "raw_pos_tag:\n", (raw_pos_tag(s))

	#  raw_parse: to parse a sentence. Takes a sentence as a string
	print "raw_parse:\n", list(st_parser.raw_parse(s))

	# raw_parse_sents
	print "raw_parse_sents:\n", list(list(st_parser.raw_parse_sents(sent_tokenize(s)))[0])

	# tagged_parse_sents:  to parse multiple sentences
	print "tagged_parse_sents:\n", list(list(st_parser.tagged_parse_sents(raw_pos_tag(s)))[0])
	
if __name__ == "__main__":
	main()