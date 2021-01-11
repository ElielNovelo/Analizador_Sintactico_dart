import ply.lex as lex  
import re

resultado_lexema = []

tokens = [
    # inicio y final
    'TAGINICIO', 'TAG_FINAL',
    'ENTERO', 'ASIGNAR',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'POTENCIA',
    'MODULO',
    'MINUSMINUS',
    'PLUSPLUS',
    'PUNTOYCOMA',
    'PUNTO',
    'COMA', 'DECIMAL', 'VARIABLE', 'COMENTARIO','ENTRE',
    # Condiones
    'SI', 'SINO',
    # Ciclos
    'MIENTRAS', 'PARA', 'DO',
    # logica
    'AND', 'OR', 'NOT', 'MENORQUE', 'MENORIGUAL', 'MAYORQUE', 'MAYORIGUAL', 'IGUAL', 'DISTINTO',
    # Symbolos
    'NUMERAL', 'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER', 'LLAIZQ', 'LLADER'
]

# Reglas de Expresiones Regualres para token de Contexto simple

t_PUNTOYCOMA = r';'
t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'
#t_PUNTO = r'\.'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'
t_ASIGNAR = r'='
# Expresiones
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'

# palabras reservadas de PHP

def t_TAGINICIO(t):
    r'(<+[\?+php]+)'
    return t


def t_TAG_FINAL(t):
    r'([\?>]+)'
    return t


def t_VARIABLE(t):
    r'([\$]+[A-Za-z]+)'
    return t


def t_SINO(t):
    r'else'
    return t

def t_SI(t):
    r'if'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_MIENTRAS(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_PARA(t):
    r'for'
    return t

def t_DECIMAL(t):
    r'([0-9][.]?[0-9]+)'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NUMERAL(t):
    r'\#'
    return t

# operacion logica


def t_PLUSPLUS(t):
    r'\+\+'
    return t


def t_MENORIGUAL(t):
    r'<='
    return t


def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t


def t_MAYORDER(t):
    r'<<'
    return t

def t_MAYORIZQ(t):
    r'>>'
    return t


def t_DISTINTO(t):
    r'!='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMENTARIO(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")


def t_comments_ONELine(t):
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de una linea")


t_ignore = ' \t'


def t_error(t):
    global resultado_lexema
    estado = "** Token no valido en la Linea {:4}".format(str(t.lineno)
                                                          )
    resultado_lexema.append(estado)
    t.lexer.skip(1)


# Prueba de ingreso

def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)
    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} TOKEN {:4} >>>> {:4}".format(
            str(tok.lineno), str(tok.type), str(tok.value))
        resultado_lexema.append(estado)

    return resultado_lexema


# abrir archivo
analizador = lex.lex()
path = "PruebaF.php"

try:
    archivo = open(path, 'r')
except:
    print("ARCHIVO NO EN CONTRADO : VERIFIQUE NUEVAMENTE")
    quit()

text = ""
for linea in archivo:
    text += linea
prueba(text)
print('\n'.join(list(map(''.join, resultado_lexema))))