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
mf=freeling.maco(op);

# activate mmorpho odules to be used in next call
mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

# create tagger, sense anotator, and parsers
tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
sen=freeling.senses(DATA+LANG+"/senses.dat");
parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());

# INICIO DE PRUEBA
tknzr = TweetTokenizer()
mensaje = """Mi #Tbt hoy es con @MarcAnthony  y seguro les gustara quiero que continúen
            ustedes con la letra. Cuando nos volvamos a encontrar :)"""
tknzr.tokenize(mensaje)