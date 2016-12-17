from nltk.parse.stanford import StanfordParser
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
from os.path import dirname
from os.path import abspath
import os

abs_path = dirname(abspath(__file__))
print "absulute path", abs_path

# STANFORD TOOLS
#-------------------------------------------------------------------------------
# paths
stanford_pos_dir = abs_path + '/stanford-postagger-2015-12-09/'
postag_modelfile = stanford_pos_dir+'models/english-bidirectional-distsim.tagger'
postag_jar = stanford_pos_dir + 'stanford-postagger.jar'
stanford_parser_dir = abs_path + '/stanford-parser-full-2015-12-09/'
parser_eng_model = stanford_parser_dir+'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
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
#-------------------------------------------------------------------------------
# paths
bikel_dir = abs_path + '/dbparser/'
bk_parser_path = bikel_dir+'bin/parse'
bk_settings = bikel_dir+'settings/collins.properties'
bk_parser_model = bikel_dir+'bikel/wsj-02-21.obj.gz'
# cmd = bikel_parser+" 400"+bk_settings+" "+bk_parser_model + inputfile