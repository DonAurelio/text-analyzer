# -*- encoding: utf-8 -*-

# ETIQUETAS EAGLE Y ADICIONALES PARA RECONOCER EMOTICIONES
EAGLES_ADJETIVOS = {
  '1A':'Adjetivo',
  '2Q':'Calificativo',
  '2O':'Ordinal',
  '20':'',
  '3A':'Aumentativo',
  '3D':'Disminutivo',
  '3C':'Comparativo',
  '3S':'Superlativo',
  '30':'',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '40':'',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '50':'',
  '60':'-',
  '6P':'Participio',
}

EAGLES_ADVERBIOS = {
  '1R':'Adverbio',
  '2G':'General',
  '2N':'Negativo',
  '20':'',
}

EAGLES_DETERMINANTES = {
  '1D':'Determinante',
  '2D':'Demostrativo',
  '2P':'Posesivo',
  '2T':'Interrogativo',
  '2E':'Exclamativo',
  '2I':'Indefinido',
  '2A':'Artículo',
  '20':'',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '30':'',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '4N':'Neutro',
  '40':'',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '50':'',
  '6S':'Singular',
  '6P':'Plural',
  '60':'',
}

EAGLES_NOMBRES = {
  '1N':'Nombre',
  '2C':'Común',
  '2P':'Propio',
  '20':'',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '30':'',
  '4S':'Singular',
  '4P':'Plural',
  '4N':'Invariable',
  '40':'',
  #-->
  '50':'',
  '60':'',
  #<--
  '7A':'Apreciativo',
  '7D':'Disminutivo'
  '70':'',
}

EAGLES_VERBOS = {
  '1V':'Verbo',
  '2M':'Principal',
  '2A':'Auxiliar',
  '2S':'Semiauxiliar',
  '20':'',
  '3I':'Indicativo',
  '3S':'Subjuntivo',
  '3M':'Imperactivo',
  '3N':'Infinitivo',
  '3G':'Gerundio',
  '3P':'Participio',
  '30':'',
  '4P':'Presente',
  '4I':'Imperfecto',
  '4F':'Futuro',
  '4S':'Pasado',
  '4C':'Condicional',
  '40':'-',
  '51':'Primera',
  '52':'Segunda',
  '53':'Tercera',
  '50':'',
  '6S':'Singular',
  '6P':'Plural',
  '60':'',
  '7M':'Masculino',
  '7F':'Femenino',
  '70':''
}

EAGLES_PRONOMBRES = {
  '1P':'Pronombre',
  '2P':'Personal',
  '2D':'Demostrativo',
  '2X':'Posesivo',
  '2I':'Indefinido',
  '2T':'Interrogativo',
  '2R':'Relativo',
  '2E':'Exclamativo',
  '20':'',
  '31':'Primera',
  '32':'Segunda',
  '33':'Tercera',
  '30':'',
  '4M':'Masculino',
  '4F':'Femenino',
  '4C':'Común',
  '4N':'Neutro',
  '40':'',
  '5S':'Singular',
  '5P':'Plural',
  '5N':'Invariable',
  '5M':'Impersonal',
  '50':'',
  '6N':'Normativo',
  '6A':'Acusativo',
  '6D':'Dativo',
  '6O':'Oblicuo',
  '60':'',
  '7S':'Singular',
  '7P':'Plural',
  '70':'',
  '8P':'Polite',
  '80':''
}

EAGLES_CONJUNCIONES = {
  '1C':'Conjunción',
  '2C':'Coordinada',
  '2S':'Subordinada',
  '20':'',
}

EAGLES_INTERJECCIONES = {
  '1I':'Interjección'
}

EAGLES_PREPOSICIONES = {
  '1S':'Adposición',
  '2P':'Preposición',
  '20':'',
  '3S':'Simple',
  '3C':'Contraída',
  '3M':'Masculino',
  '30':'',
  '4S':'Singular',
  '40':''
}

EAGLES_SIGNOS_DE_PUNTUACION = {
  '1F':'Puntuación'
}

EAGLES_NUMERALES = {
  '1Z':'Cifra',
  '2d':'Partivivo',
  '2m':'Moneda',
  '2p':'Porcentaje',
  '2u':'Unidad',
  '20':'',
}

EAGLES_NUMERALES = {
  '1W':'Fecha/Hora',
}

# borrar? ->
EAGLES_ABREVIATURAS = {
  '1Y':'Abreviatura'
}

EAGLES_ARTICULOS = {
  '1T':'Artículo',
  '2D':'Definido',
  '20':'',
  '3M':'Masculino',
  '3F':'Femenino',
  '3C':'Común',
  '30':'',
  '4S':'Singular',
  '4P':'Plural',
  '40':'',
  '50':''
}
# <- borrar?

ETIQUETA_EMOTICONES = {
  '1E':'Emoticón'
}

ETIQUETA_URL = {
  '1U':'Url'
}

ETIQUETA_HASHTAG = {
  '1#':'Hashtag'
}

ETIQUETA_NICKNAME = {
  '1@':'Nickname'
}

EAGLES_CATEGORIAS = {
  'A':EAGLES_ADJETIVOS,
  'R':EAGLES_ADVERBIOS,
  'T':EAGLES_ARTICULOS,
  'D':EAGLES_DETERMINANTES,
  'N':EAGLES_NOMBRES,
  'V':EAGLES_VERBOS,
  'P':EAGLES_PRONOMBRES,
  'C':EAGLES_CONJUNCIONES,
  'M':EAGLES_NUMERALES,
  'I':EAGLES_INTERJECCIONES,
  'Y':EAGLES_ABREVIATURAS,
  'S':EAGLES_PREPOSICIONES,
  'F':EAGLES_SIGNOS_DE_PUNTUACION,
  '@':ETIQUETA_NICKNAME,
  '#':ETIQUETA_HASHTAG,
  'U':ETIQUETA_URL,
  'E':ETIQUETA_EMOTICONES
}

def interpretar(texto):
  categoria = texto[0]
  diccionario = EAGLES_CATEGORIAS[categoria]
  traduccion = ""
  try:
    for i,letra in zip(range(1,len(texto)+1),texto):
      traduccion += diccionario[str(i)+str(letra)] + " "
  except KeyError:
    traduccion = "¿"+ texto +"?"
  finally:
    return traduccion