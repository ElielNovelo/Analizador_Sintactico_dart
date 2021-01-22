import ply.yacc as yacc
from lexico_dart import tokens #erencia de los tokens del analizador lexico
import re 

# resultado del analisis
resultado_gramatica = []

#aqui  los tokens eredados con su nivel de precedencia, hacia donde va su lectura con 
#referencia a su validacion.
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

#almacenar los tipos de asignacion
nombres = {}


#en estas funciones se definen las condicionales
def p_declaracion_coditionif(t):
    'declaracion : IF LPAREN expresion GT expresion RPAREN LBRACE expresion SEMI RBRACE'
    t[0] = t[1] # en dado caso que se quiera reutilizar solo se cambian los tokens con referencia la leguaje

#declaracion de funcion else
def p_declaracion_coditionelse(t):
    'declaracion : ELSE LBRACE expresion SEMI RBRACE'
    t[0] = t[1]

# se definde como se debe llevar el proceso de asignacion con refencia al tipo de dato
def p_declaracion_asignar(t):
    'declaracion : INT expresion EQUALS expresion SEMI'
    nombres[t[1]] = t[3]

def p_declaracion_asignar2(t):
    'declaracion : DOUBLE expresion EQUALS expresion SEMI'
    nombres[t[1]] = t[3]
    
# se define como inicia el programa
def p_declaracion_taginicio(t):
    'declaracion : OPENTAG'
    t[0] = t[1]

# se define como concluye el programa
def p_declaracion_tagfinal(t):
    'declaracion :  CLOSETAG'
    t[0] = t[1]

#como se define una expresion.
def p_declaracion_expr(t):
    'declaracion : expresion SEMI'
    t[0] = t[1]


#definimos como se validara los operandos
def p_expresion_operaciones(t):
    '''
    expresion  :   expresion PLUS expresion 
                |   expresion MINUS expresion 
                |   expresion TIMES expresion
                |   expresion DIVIDE expresion 

    '''
    #como debe de expresarse las operaciones cuando se este compilando 
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

#variante de el menos
def p_expresion_minus(t):
    'expresion : MINUS expresion %prec MINUS'
    t[0] = -t[2]

#como se definen las expresiones entre parentesis y corchetes con expreciones
def p_expresion_grupo(t):
    '''
    expresion  : LPAREN expresion RPAREN 
                | LBRACE expresion RBRACE

    '''
    t[0] = t[2]

# sintactico de expresiones logicas
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
    ''' #cada una de las variantes en las expresiones logicas
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

#definicion de las funiones de tipos de variable, muy importante tomar en cuenta el oreden 
def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = t[1]

def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_id(t):
    'expresion : ID'
    t[0] = t[1]

#funcion que nos ayuda a recibir el error en caso de existir
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

#funcion que caputa de manera presisa los erroes
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

#importamos el archivo a analizar
path = "prueba.dart"

#verificacion y capura de error al buscar el archivo
try:
    archivo = open(path, 'r')
except:
    print("el archivo no se encontro")
    quit()

text = ""
for linea in archivo:
    text += linea

#impresion de los resultados de manera ordena.
prueba_sintactica(text)
print()
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
print()
print('\n'.join(list(map(''.join, resultado_gramatica))))

