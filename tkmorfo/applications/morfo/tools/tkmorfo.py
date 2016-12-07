# -*- coding: utf-8 -*-

from twokenize import emoticon, Hashtag, AtMention, url
from twokenize import tokenize as ark_tokenize
import freeling
import re
#======================== Freling Initialization ===============================
# Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr";

DATA = FREELINGDIR+"/share/freeling/";
LANG="es";

freeling.util_init_locale("default");

# create options set for maco analyzer. Default values are Ok, except for data files.
op= freeling.maco_options("es");
op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
                   DATA + LANG + "/probabilitats.dat");

# create analyzers
#f_tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat"); # tokenizador de freeling
f_mf=freeling.maco(op);

# activate mmorpho odules to be used in next call
f_mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

#======================== ./Freling Initialization =============================


################################################################################
# ALGORITMO
""" 
    Iterar el arreglo que devuelve Twokenizer (lista de strings) y castear
    cada palabra a word usando freeling.word(), al finalizar crear un list<word>
    
    Hacer set_tag() de símbolos, nicknames, hashtags, urls y para
    cada uno setear lock_analysis() para que sean ignorados por el analyze()

    Convertir el list<word> a sentence, aplicar el análisis morfológico, 
    crear estructura de datos para enviar a la aplicación web (interpretar etiquetas)
    y mostrar

 """
################################################################################

#===============================================================================
# Funciones auxiliares 
def taggear(w, lemma, tag):
  """
  Asigna a una palabra "w" el tag y lema especificados y bloquea el
  análisis de la palabra
  """
  analisis = freeling.analysis()
  analisis.set_lemma(lemma)
  analisis.set_tag(tag)
  w.set_analysis(analisis)
  w.lock_analysis()

def parse_sentence(sentencia):
  """
  Recibe una sentencia en formato freeling, retorna una estructura de
  tuplas y listas con las palabras y su información morfológica
  """
  info = []
  for w in sentencia:
    palabra = w.get_form()
    lem_tag = []
    for w_a in w.get_analysis():
      lem_tag.append((w_a.get_lemma(),w_a.get_tag()))
    palabra_analisis =  (palabra,lem_tag)
    info.append(palabra_analisis)
  return info

#===============================================================================
# Funciones análisis
def tokenizar(texto):
  return ark_tokenize(texto)

def morfo_analyze(listatokens,full_analize=True):
  tokens = listatokens[:]
  re_emoticon = re.compile(emoticon)
  re_hashtag = re.compile(Hashtag)
  re_nickname = re.compile(AtMention)
  re_url = re.compile(url)
  for i, tk in enumerate(tokens):
    tokens[i] = freeling.word(tk)
    if re_emoticon.match(tk):
      taggear(tokens[i],"","E")
    elif re_nickname.match(tk):
      taggear(tokens[i],"","@")
    elif re_hashtag.match(tk):
      taggear(tokens[i],"","#")
    elif re_url.match(tk):
      taggear(tokens[i],"","U")
  sentencia = freeling.sentence(tuple(tokens))
  if full_analize:
    sentencia = f_mf.analyze(sentencia)
  return sentencia
#===============================================================================