import ply.yacc as yacc
from lexico_dart import tokens
#import ply.lex as lex
import re 

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','IF', 'ELSE'),
    ('left', 'SEMI'),
    ('left', 'COMMA'),
    ('left', 'EQUALS'),
    ('left', 'SEMI'),
    ('left', 'NE'),
    ('left', 'LT', 'LE','GT', 'GE', 'EQ'),
    ('left', 'PLUS','MINUS'),
    ('left', 'TIMES','DIVIDE'),
    ('left', 'LBRACE', 'RBRACE'),
    ('left', 'LPAREN', 'RPAREN')
)

nombres = {}



def p_declaracion_coditionif(t):
    'declaracion : IF LPAREN expresion GT expresion RPAREN LBRACE expresion SEMI RBRACE'
    t[0] = t[1] 


def p_declaracion_coditionelse(t):
    'declaracion : ELSE LBRACE expresion SEMI RBRACE'
    t[0] = t[1]

# se definde como debe de funcionar
def p_declaracion_asignar(t):
    'declaracion : INT expresion EQUALS expresion SEMI'
    nombres[t[1]] = t[3]

# aqui la idea de como hacer la primera declaracion
def p_declaracion_taginicio(t):
    'declaracion : OPENTAG'
    t[0] = t[1]


def p_declaracion_tagfinal(t):
    'declaracion :  CLOSETAG'
    t[0] = t[1]

def p_declaracion_expr(t):
    'declaracion : expresion SEMI'
    t[0] = t[1]



def p_expresion_operaciones(t):
    '''
    expresion  :   expresion PLUS expresion 
                |   expresion MINUS expresion 
                |   expresion TIMES expresion
                |   expresion DIVIDE expresion 

    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]


def p_expresion_minus(t):
    'expresion : MINUS expresion %prec MINUS'
    t[0] = -t[2]


def p_expresion_grupo(t):
    '''
    expresion  : LPAREN expresion RPAREN 
                | LBRACE expresion RBRACE

    '''
    t[0] = t[2]

# sintactico de expresiones logicas
# sintactico de expresiones logicas


#def p_expresion_ifelse(t):
    #'expresion : SI PARIZQ expresion PARDER LLAIZQ expresion LLADER'
    #t[0] = t[2] = t[4] = t[5] = t[7]
    
def p_expresion_logicas(t):
    '''
    expresion   :  expresion LT expresion 
                |  expresion GT expresion 
                |  expresion LE expresion 
                |   expresion GE expresion 
                |   expresion EQUALS expresion 
                |   expresion EQ expresion
                |  LPAREN expresion LT expresion RPAREN
                |  LPAREN expresion GT expresion RPAREN
                |  LPAREN expresion LE expresion RPAREN
                |  LPAREN expresion GE expresion RPAREN
                |  LPAREN expresion EQUALS expresion RPAREN
                |  LPAREN expresion EQ expresion RPAREN
    '''
    if t[2] == "<":
        t[0] = t[1] < t[3]
    elif t[2] == ">":
        t[0] = t[1] > t[3]
    elif t[2] == "<=":
        t[0] = t[1] <= t[3]
    elif t[2] == ">=":
        t[0] = t[1] >= t[3]
    elif t[2] == "==":
        t[0] = t[1] is t[3]
    elif t[2] == "!=":
        t[0] = t[1] != t[3]
    elif t[3] == "<":
        t[0] = t[2] < t[4]
    elif t[2] == ">":
        t[0] = t[2] > t[4]
    elif t[3] == "<=":
        t[0] = t[2] <= t[4]
    elif t[3] == ">=":
        t[0] = t[2] >= t[4]
    elif t[3] == "==":
        t[0] = t[2] is t[4]
    elif t[3] == "!=":
        t[0] = t[2] != t[4]



def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_id(t):
    'expresion : ID'
    t[0] = t[1]

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {:4} en el valor {:4}".format(
            str(t.type), str(t.value))
    else:
        resultado = "Error sintactico {}".format(t)
    resultado_gramatica.append(resultado)

# instanciamos el analizador sistactico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
   # resultado_gramatica.clear()

    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else:
            print("")
    #print("result: ", resultado_gramatica)
    return resultado_gramatica


path = "prueba.dart"

try:
    archivo = open(path, 'r')
except:
    print("el archivo no se encontro")
    quit()

text = ""
for linea in archivo:
    text += linea


prueba_sintactica(text)
print()
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
print()
print('\n'.join(list(map(''.join, resultado_gramatica))))

