# -*- coding: utf-8 -*-

import freeling
from nltk.tokenize import TweetTokenizer

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

EAGLES_ADJETIVOS = {
  '1A':'Adjetivo',
  '2Q':'Calificativo',
  '3A':'Apreciativo',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '60':'-',
  '7P':'Participio'
}

EAGLES_ADVERBIOS = {
  '1R':'Adverbio',
  '2G':'General',
  '30':'-',
  '40':'-',
  '50':'-'
}

EAGLES_ARTICULOS = {
  '1T':'Artículo',
  '2D':'Definido',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '4S':'Singular',
  '4P':'Plural',
  '50':'-'
}

EAGLES_DETERMINANTES = {
  '1D':'Determinante',
  '2D':'Demostrativo',
  '2P':'Posesivo',
  '2T':'Interrogativo',
  '2E':'Exclamativo',
  '2I':'Indefinido',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '6O':'-',
  '71':'1 Persona-sg',
  '72':'2 Persona-sg',
  '70':'3 Persona',
  '74':'1 Persona-pl',
  '75':'2 Persona-pl'
}

EAGLES_NOMBRES = {
  '1N':'Nombre',
  '2C':'Común',
  '2P':'Propio',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '4S':'Singular',
  '4P':'Plural',
  '4N':'Invariable',
  '50':'-',
  '60':'-',
  '7A':'Apreciativo'
}

EAGLES_VERBOS = {
  '1V':'Verbo',
  '2M':'Principal',
  '2A':'Auxiliar',
  '3I':'Indicativo',
  '3S':'Subjuntivo',
  '3M':'Imperactivo',
  '3C':'Condicional',
  '3N':'Infinitivo',
  '3G':'Gerundio',
  '3P':'Participio',
  '4P':'Presente',
  '4I':'Imperfecto',
  '4F':'Futuro',
  '4S':'Pasado',
  '51':'Primera',
  '52':'Segunda',
  '53':'Tercera',
  '6S':'Singular',
  '6P':'Plural',
  '7M':'Masculino',
  '7F':'Femenino'
}

EAGLES_PRONOMBRES = {
  '1P':'Pronombre',
  '2P':'Personal',
  '2D':'Demostrativo',
  '2X':'Posesivo',
  '2I':'Indefinido',
  '2T':'Interrogativo',
  '2R':'Relativo',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '6N':'Normativo',
  '6A':'Acusativo',
  '6D':'Dativo',
  '6O':'Oblicuo',
  '71':'1 Persona-sg',
  '72':'2 Persona-sg',
  '70':'3 Persona',
  '74':'1 Persona-pl'
  '75':'2 Persona-pl',
  '8P':'Polite'
}


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