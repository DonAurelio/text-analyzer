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





# INICIO DE PRUEBA
# mensaje = """Mi #Tbt hoy es con @MarcAnthony  y seguro les gustara quiero que continúen ustedes con la letra. Cuando nos volvamos a encontrar :)"""
# mensaje = """Por fin!! de nuevo en Twitter! =D se me daño mi celular pero ya tengo uno nuevo =D @rosariomeneses1 creo que es igual al tuyo #emoticones XD <3 ^_^!"""
mensaje = "El músico bajo toca el bajo"

# tokenizacion
tknzr = TweetTokenizer()
tkn_mensaje = tknzr.tokenize(mensaje)
print (tkn_mensaje)

# análisis morfológico solamente sobre las palabras del Español
print ("Segmentacion y tokenizacion con freeling: ")

# tokenize de freeling retorna un list<word>
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
    
    Hacer a mano tagueo set_tag() de símbolos, nicknames, hashtags, urls y para
    cada uno definir como análisis definitivo con lock_analysis()

    Convertir el list<word> a sentence, aplicar el análisis morfológico, 
    crear estructura de datos para enviar a la aplicación web (interpretar etiquetas)
    y mostrar

 """