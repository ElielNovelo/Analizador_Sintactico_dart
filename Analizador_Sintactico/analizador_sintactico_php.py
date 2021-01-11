import ply.yacc as yacc
from analizador_lexico_php import tokens
import re

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right', 'SI', 'SINO',),
    ('right', 'ASIGNAR'),
    ('left', 'TAGINICIO'),
    ('right', 'TAG_FINAL'),
    ('right', 'PUNTOYCOMA'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),
)
nombres = {}



def p_declaracion_coditionif(t):
    'declaracion : SI PARIZQ VARIABLE ASIGNAR VARIABLE PARDER LLAIZQ VARIABLE PUNTOYCOMA LLADER'
    t[0] = t[1] 

def p_declaracion_coditionif2(t):
    'declaracion : SI PARIZQ VARIABLE MENORIGUAL VARIABLE PARDER LLAIZQ VARIABLE PUNTOYCOMA LLADER'
    t[0] = t[1]                                              

def p_declaracion_coditionif3(t):
    'declaracion : SI PARIZQ VARIABLE DISTINTO VARIABLE PARDER LLAIZQ VARIABLE PUNTOYCOMA LLADER'
    t[0] = t[1] 

def p_declaracion_coditionelse(t):
    'declaracion : SINO LLAIZQ VARIABLE PUNTOYCOMA LLADER'
    t[0] = t[1]

def p_declaracion_coditionpara(t):
    'declaracion : PARA PARIZQ VARIABLE ASIGNAR ENTERO PUNTOYCOMA VARIABLE MENORQUE VARIABLE PUNTOYCOMA VARIABLE PLUSPLUS PARDER LLAIZQ VARIABLE PUNTOYCOMA LLADER'
    t[0] = t[1] 

def p_declaracion_coditionmientras(t):
    'declaracion : MIENTRAS PARIZQ VARIABLE MENORIGUAL VARIABLE PARDER LLAIZQ VARIABLE PLUSPLUS PUNTOYCOMA LLADER'
    t[0] = t[1]

def p_declaracion_coditiondomientas(t):
    'declaracion : DO LLAIZQ VARIABLE PUNTOYCOMA LLADER MIENTRAS PARIZQ VARIABLE MENORQUE ENTERO PARDER PUNTOYCOMA'
    t[0] = t[1]

# se definde como debe de funcionar
def p_declaracion_asignar(t):
    'declaracion : VARIABLE ASIGNAR expresion PUNTOYCOMA'
    nombres[t[1]] = t[3]


# aqui la idea de como hacer la primera declaracion
def p_declaracion_taginicio(t):
    'declaracion : TAGINICIO'
    t[0] = t[1]


def p_declaracion_tagfinal(t):
    'declaracion :  TAG_FINAL'
    t[0] = t[1]



def p_declaracion_expr(t):
    'declaracion : expresion PUNTOYCOMA'
    # print("Resultado: " + str(t[1]))
    t[0] = t[1]


def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion 
                |   expresion RESTA expresion 
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion

    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1


def p_expresion_uminus(t):
    'expresion : RESTA expresion %prec UMINUS'
    t[0] = -t[2]


def p_expresion_grupo(t):
    '''
    expresion  : PARIZQ expresion PARDER 
                | LLAIZQ expresion LLADER
                | CORIZQ expresion CORDER

    '''
    t[0] = t[2]
# sintactico de expresiones logicas
# sintactico de expresiones logicas
    
def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENORQUE expresion 
                |  expresion MAYORQUE expresion 
                |  expresion MENORIGUAL expresion 
                |   expresion MAYORIGUAL expresion 
                |   expresion IGUAL expresion 
                |   expresion DISTINTO expresion
                |  PARIZQ expresion PARDER MENORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MAYORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MENORIGUAL PARIZQ expresion PARDER 
                |  PARIZQ  expresion PARDER MAYORIGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER IGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER DISTINTO PARIZQ expresion PARDER
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
    'expresion : ENTERO'
    t[0] = t[1]


def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = t[1]



def p_expresion_nombre(t):
    'expresion : VARIABLE'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("")
        print("VERIFICAR: ", t[1])
        print("¿verificar si se definio o asigno un valor(en caso de operacion arimetica)?")
        t[0] = 0



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

    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else:
            print("")
    return resultado_gramatica


path = "PruebaF.php"

try:
    archivo = open(path, 'r')
except:
    print("ARCHIVO NO EN CONTRADO : VERIFIQUE NUEVAMENTE")
    quit()

text = ""
for linea in archivo:
    text += linea


prueba_sintactica(text)
print('-------------------------------------------------')
print('\n'.join(list(map(''.join, resultado_gramatica))))