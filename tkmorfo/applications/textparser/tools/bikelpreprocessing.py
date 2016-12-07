# -*- coding: utf-8 -*-
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import StanfordTokenizer
from os.path import dirname

stanford_dir = dirname(__file__) + '/stanford-postagger-2015-12-09/'
modelfile = stanford_dir + 'models/english-bidirectional-distsim.tagger'
posjarfile = stanford_dir + 'stanford-postagger.jar'
st = StanfordPOSTagger(model_filename=modelfile, path_to_jar=posjarfile)
tk = StanfordTokenizer(path_to_jar=posjarfile)

def split_sentence(text):
    splited_text = sent_tokenize(text)
    tokenized_text = tk.tokenize(text)
    print splited_text
