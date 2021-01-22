import ply.lex as lex

resultado_lexema = []

tokens = ['NUMBER','DECIMAL','OPENTAG','CLOSETAG','ID', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',  'EQUALS', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
'COMMA', 'SEMI','LPAREN', 'RPAREN', 'LBRACE', 'RBRACE']

reservadas = {
# https://dart.dev/guides/language/language-tour#keywords
   'if':'IF',
   'else':'ELSE',
   'null':'NULL',
   'break':'BREAK',
   'true':'TRUE',
   'false':'FALSE',
   'var':'VAR',
   'int':'INT',
   'Void':'VOID',
   'for':'FOR',
   'bool':'BOOL',
   'print':'PRINT',
   'double':'DOUBLE'
}

tokens = tokens + list(reservadas.values())



# RE SYMBOLS
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_LT        = r'<'
t_GT        = r'>'
t_LE        = r'<='
t_GE        = r'>='
t_EQ        = r'=='
t_NE        = r'!='
t_SEMI      = r';'
t_COMMA     = r','
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
#t_PERIOD    = r'\.'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter ilegal '%s'"%t.value[0])
    t.lexer.skip(1)

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_espacio(t):
    r"\s"
    pass

# RE OPEN AND CLOSE TAG
def t_OPENTAG(t):
    #r'(void\smain\s?\(\))'
    r'main\s?\(\)\s?\{'
    return t
def t_CLOSETAG(t):
    #r'(void\smain\s?\(\))'
    r'\}'
    return t
#palabras recervadas

def t_INT(t):
    r'int'
    return t

def t_DOUBLE(t):
    r'double'
    return t

#def t_NUMERO(t):
  #  r'\d+\;?'
   # return t

def t_IF(t):
   r'if'
   return t

def t_ELSE(t):
    r'else'
    return t

def t_NULL(t):
   r'null'
   return t

def t_BREAK(t):
   r'break'
   return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_VAR(t):
    r'var'
    return t

def t_VOID(t):
   r'void'
   return t

def t_FOR(t):
    r'for'
    return t

#def t_ID(t):
 #   r'([int\s]+[A-Za-z]+)'
  #  return t

def t_ID(t):
    r'\w+\=|\w+'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_BOOL(t):
    r'bool'
    return t

#def t_STRING(t):
  #  r'\w+|:'
   # return t

#REYES GUADALUPE KAUIL ESPADAS
#ELIEL DAVID NOVELO CAHUM
#MARCO ANTONIO BAEZA CAHUM
lexer = lex.lex()

# Prueba de ingreso

def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)
    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} Tipo {:4} >>>>> {:4}".format(
            str(tok.lineno), str(tok.type), str(tok.value))
        resultado_lexema.append(estado)

    return resultado_lexema


# abrir archivo
analizador = lex.lex()
path = "prueba.dart"

try:
    archivo = open(path, 'r')
except:
    print("el archivo no se encontro")
    quit()

text = ""
for linea in archivo:
    text += linea
prueba(text)
# AL IMPRIMIR LOS DATOS, ESTO LO ORDENA DE MANERA ESTRUCTURADA
print('\n'.join(list(map(''.join, resultado_lexema))))
