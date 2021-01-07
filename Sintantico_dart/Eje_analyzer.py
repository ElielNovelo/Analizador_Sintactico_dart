import sys
from sintantico_dart import parser
n=0
if __name__ == "__main__":
    file_name = 'prueba.dart'
    file = open(file_name, "r")
    data = file.read()

    while True:
        n=n+1
        tok = parser.token()
        if not tok:
            break
        print ("Token ",n," >>>> ", tok)