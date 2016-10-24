# -*- coding: utf-8 -*-
######################################################################
from twokenize import emoticon, Hashtag, AtMention, url
from twokenize import tokenize as ark_tokenize
#from nltk.tokenize import TweetTokenizer
import freeling
import re
######################################################################

#============================ Freling Initialization ================================
# Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr";

DATA = FREELINGDIR+"/share/freeling/";
LANG="es";

freeling.util_init_locale("default");

# create language analyzer
#la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

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
f_tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
#sp=freeling.splitter(DATA+LANG+"/splitter.dat");
#sid=sp.open_session();
f_mf=freeling.maco(op);

# activate mmorpho odules to be used in next call
f_mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

# create tagger, sense anotator, and parsers
#tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
#sen=freeling.senses(DATA+LANG+"/senses.dat");
#parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
#dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());

#============================ Freling Initialization ================================


#============================ Descripción del proyecto ==============================
# El procesamiento de lenguaje natural de textos comprende 3 etapas 
# 1) Preprocesamiento: Consiste en normalizar el texto de entrada, en algunos casos 
# se corrigen errores ortográficos, se eliminan espacios innecesarios y dependiendo 
# del tipo de analisis que se desee hacer se le dá un significado alternativo a los 
# emoticones, se elimian hash "#" haciendo que el resto del hash haga parte de la oración
# tambien se modifican urls y nicknames. 
# NOTA: Para este caso no se hace la etapa de preprocesado

# 2) Segmentación de frases y palabras
# Tras el preprocesado del texto ya se han normalizado algunos de los elementos que podián
# complicar la identificación y división de frases y palabras, como la incorrecta colocación de 
# signos de puntuación o la aparición de nombres de usuarios de twitter o hashtags, para la 
# segmenación de oraciones, se usa la biblioteca nltk.
# NOTA: Las estructuras de un parrafo son: 
#   Sentencias o Oraciones (componentes del parrafo).
#   Palabras hace parte de una sentencia u oración 
# NLTK primero lleva a cabo la segmentación de oraciones y luego la segmentación de palabras 

# 3) Análisis morfológico
# Dada una oracion S compuesta por un conjunto de palabras Wi, y un conjunto de etiquetas 
# T con etiquetas Ti, el proceso de análisis morfológico tambien conocido como etiquetación,
# consiste en asignar a cada palabra de la oración su etiqueta correspondiente, creando una 
# lista de tuplas (s,t) donde s partenece a S y t pertenece a T

#============================ Descripción del proyecto ==============================


######################################################################
# ALGORITMO PROPUESTO
######################################################################
""" 
    Iterar el arreglo que devuelve TweetTokenizer (lista de strings) y cada palabra
    a word usando freeling.word() al finalizar crear un list<word>
    
    Hacer tag set_tag() de símbolos, nicknames, hashtags, urls y para
    cada uno setear lock_analysis() para que sean ignorados por el analyze()

    Convertir el list<word> a sentence, aplicar el análisis morfológico, 
    crear estructura de datos para enviar a la aplicación web (interpretar etiquetas)
    y mostrar

 """

def procesar_texto_nltk_freeling(texto):
  pass

def procesar_texto_nltk(texto):
  pass

def procesar_texto_freeling(texto):
  pass

######################################################################
# Funciones internas
def taggear(w,tag):
  """
  A una palabra freeling "w" le asigna el "tag", lema="" y bloquea el
  análisis respectivo
  """
  analisis = freeling.analysis()
  analisis.set_tag(tag)
  analisis.set_lemma("")
  w.set_analysis(analisis)
  w.lock_analysis()

######################################################################
# Funciones análisis

def pre_mf_analyze(listatokens):
  """
  :param lis: lista de strings
  
  Hace el casting de los elementos a <word> y si es una expresión
  especial (emoticon, nickname, hashtag o url) le asigna una anotación
  morfológica.
  
  :retorna: tupla de words list<word>
  """
  tokens = listatokens[:]
  re_emoticon = re.compile(emoticon)
  re_hashtag = re.compile(Hashtag)
  re_nickname = re.compile(AtMention)
  re_url = re.compile(url)
  for i, tk in enumerate(tokens):
    tokens[i] = freeling.word(tk)
    if re_emoticon.match(tk):
      taggear(tokens[i], "E")
    elif re_nickname.match(tk):
      taggear(tokens[i], "@")
    elif re_hashtag.match(tk):
      taggear(tokens[i], "#")
    elif re_url.match(tk):
      taggear(tokens[i], "U")
  return tuple(tokens)

def analisis_morfologico(lword):
  """
  Recibe una tupla list<word>, aplica análisis morfológico, por cada
  elemento retorna el elemento y una lista con sublistas de parejas
  lema, tag
  Ejemplo para toca:
  [ "toca", [["tocar", "VMIP3S0"],["toca","NCFS000"],["tocar","VMM02S0"]] ]
  """
  sentencia = freeling.sentence(lword)
  sentencia = f_mf.analyze(sentencia)
  info = []
  for w in sentencia:
    info.append(w.get_form())
    for w_a in w.get_analysis():
      lem_tag = []
      lem_tag.append[w_a.get_lemma()]
      lem_tag.append[w_a.get_tag()]
      info.append[lem_tag]
  return info

######################################################################
# Función para interacción externa
def obtener_mf(texto):
  """
  Ejemplo para toca:
  {"n_tokens": 1,
  "tokens":["toca"]
  "toca": [["tocar", "VMIP3S0"],["toca","NCFS000"],["tocar","VMM02S0"]] }
  """
  tokens = ark_tokenize(texto)
  n_tokens = len(tokens)
  result = analisis_morfologico(pre_mf_analyze(tokens))
  print (result)

######################################################################

######################################################################
if __name__ == '__main__':
  mensaje = "El musico bajo toca el bajo"
  mensaje1 = "Mi #Tbt hoy es con @MarcAnthony  y seguro les gustara quiero que continúen \
  ustedes con la letra. Cuando nos volvamos a encontrar :)"
  mensaje2 = "Por fin!! de nuevo en Twitter! =D se me daño mi celular pero ya tengo uno \
  nuevo =D @rosariomeneses1 creo que es igual al tuyo #emoticones XD <3 ^_^!"
  m_emojis = "Hola si =D entonces o.O 12:30 O.o (: jeje :v 1, 2, 3.5 1,2"

  print("HOLA MUNDO")
  # Tokenizar con Twokenize
  tokens = ark_tokenize(mensaje)
  print(tokens)
  pre = pre_mf_analyze(tokens)
  print(pre)

  #morfo = analisis_morfologico(pre)
  #print(morfo)
  
######################################################################