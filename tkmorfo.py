# -*- coding: utf-8 -*-

import freeling
from nltk.tokenize import TweetTokenizer


## Modify this line to be your FreeLing installation directory
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
tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
#sp=freeling.splitter(DATA+LANG+"/splitter.dat");
#sid=sp.open_session();
mf=freeling.maco(op);

# activate mmorpho odules to be used in next call
mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

# create tagger, sense anotator, and parsers
#tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
#sen=freeling.senses(DATA+LANG+"/senses.dat");
#parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
#dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());



mensaje = "El músico bajo toca el bajo"
mensaje1 = "Mi #Tbt hoy es con @MarcAnthony  y seguro les gustara quiero que continúen \
ustedes con la letra. Cuando nos volvamos a encontrar :)"
mensaje2 = "Por fin!! de nuevo en Twitter! =D se me daño mi celular pero ya tengo uno \
nuevo =D @rosariomeneses1 creo que es igual al tuyo #emoticones XD <3 ^_^!"

print(mensaje1)
# INICIO DE PRUEBA
def prueba_freeling():
  # análisis morfológico solamente sobre las palabras del Español
  print ("Usando tokenizacion de freeling: ")

  # tokenize() de freeling retorna un list<word>
  tk_msg = tk.tokenize(mensaje)
  # En este caso sentence recibe un list<word> y devuelve un sentence
  s_msg = freeling.sentence(tk_msg)
  # analyze recibe un sentence y me retorna un sentence analizado :P
  s_msg = mf.analyze(s_msg)

  # retorna vector<word>
  ws = s_msg.get_words()
  # iterar sobre las word
  for w in ws:
    print("Análisis de: ", w.get_form())
    #print (w.get_lemma())
    #print (w.get_tag())
    for a in w.get_analysis():
      print (a.get_lemma())
      print (a.get_tag())


# ALGORITMO PROPUESTO:
""" 
    Iterar el arreglo que devuelve TweetTokenizer y "castear" cada palabra
    en word usando freeling.word() al finalizar crear un list<word>
    
    Parte dificil?:
    Hacer a mano tagueo set_tag() de símbolos, nicknames, hashtags, urls y para
    cada uno setear lock_analysis() para que sean ignorados por el analyze()

    Convertir el list<word> a sentence, aplicar el análisis morfológico, 
    crear estructura de datos para enviar a la aplicación web (interpretar etiquetas)
    y mostrar

 """

# Recibe una lista de strings y retorna una tupla de words list<word>
def to_lword(lis):
  lword = ()
  for w in lis:
    lword += (freeling.word(w),)
  return lword

# Recibe un list<word> y taguea símbolos, nicknames, hashtags, urls
def pre_mf_analyze():
  pass

# Recibe una etiqueta EAGLES y retorna un arreglo con la interpretación
""" ejemplo:
  AQ0CP00 ->
  {"Categoría": "Adjetivo", Tipo": "Calificativo", "Grado": 0, "Género": "Común",
   "Número": "Plurar", "Caso":0, "Función":0}
 """
def eagle2info(etiqueta):
  # ADJETIVOS
  if etiqueta[0] == "A":
    if etiqueta[1] == "Q": 
      tipo = "Calificativo"
    if etiqueta[2] == "A":
      grado = "Apreciativo"
    elif etiqueta[2] == "0":
      grado = 0
    if etiqueta[3] == "M":
      genero = "Masculino"
    elif etiqueta[3] == "F":
      genero = "Femenino"
    elif etiqueta[3] == "C":
      genero = "Común"
    elif etiqueta[3] == "0":
      genero = 0
    if etiqueta[4] == "S":
      num = "Singular"
    elif etiqueta[4] == "P":
      num = "Plural"
    elif etiqueta[4] == "N":
      num = "Invariable"
    caso = 0
    if etiqueta[6] == "P":
      funcion = "Participio"
    elif etiqueta[6] == "0":
      funcion = 0
    json_i = {"Categoría": "Adjetivo", "Tipo": tipo, "Grado": grado, \
              "Género": genero, "Número": num, "Caso": caso, "Función": funcion}
    return json_i
  # ADVERBIOS
  if etiqueta[0] == "R"
    json_i = {"Categoría": "Adverbio", "Tipo": "General"}
    return json_i
  # ARTICULOS

print (eagle2info("AQ0CP00"))

# muestra el análisis morfológico por consola
def show_mf(sentence):
  for w in sentence:
    print("Análisis de: ", w.get_form())
    for w_a in w.get_analysis():
      print (w_a.get_lemma())
      print (w_a.get_tag())


# tokenizacion con TweetTokenizer
tknzr = TweetTokenizer()
tkn_mensaje = tknzr.tokenize(mensaje)
print (tkn_mensaje)
# crear list<word> y sentence
msg = to_lword(tkn_mensaje)
msg = freeling.sentence(msg)
# aplicar análisis morfo
msg = mf.analyze(msg)
#show_mf(msg)