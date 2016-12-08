# -*- coding: utf-8 -*-
# import nltk
# nltk.download('punkt')
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import StanfordTokenizer
from os.path import dirname
from os.path import abspath

stanford_dir = dirname(abspath(__file__)) + '/stanford-postagger-2015-12-09/'
modelfile = stanford_dir + 'models/english-bidirectional-distsim.tagger'
posjarfile = stanford_dir + 'stanford-postagger.jar'
st_tagger = StanfordPOSTagger(model_filename=modelfile, path_to_jar=posjarfile)
st_tk = StanfordTokenizer(path_to_jar=posjarfile)


def pos_tag(text):
	sentences = sent_tokenize(text) # Segment sentences
	tokenized_sentences = [st_tk.tokenize(s) for s in sentences] # Tokenizer
	result = st_tagger.tag_sents(tokenized_sentences) # PosTagger
	return result

def to_bikel_format(seq):
    result = ""
    for sentence in seq:
    	result += "("
    	for item in sentence:
    		result = result + "("+item[0]+" "+"("+item[1]+")) "
    	result += ") "
    return result


#=============================== MAIN -> TEST ==================================
def main():
	s = 'Pierre Vinken, 61 years old, will join the board as a nonexecutive \
		 director Nov. 29.'
	print "pos_tag:\n", (pos_tag(s))
	print "to_bikel_format:\n", to_bikel_format(pos_tag(s))
	
if __name__ == "__main__":
    main()