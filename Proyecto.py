import re
from typing import Literal
from CNF import CNF
from NormalFormCFG import NormalFormCFG
from CYK import CYK

def leer_gramaticas_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
        bloques_gramatica = contenido.split('#')

        gramaticas = []

        for bloque in bloques_gramatica:
            if bloque.strip():
                gramatica = {}
                lineas = bloque.strip().splitlines()

                for linea in lineas:
                    if '→' in linea:
                        non_terminal, producciones = linea.split('→')
                        non_terminal = non_terminal.strip()
                        producciones = [p.strip().split() for p in producciones.split('|')]

                        
                        if non_terminal in gramatica:
                            gramatica[non_terminal].extend(producciones)
                        else:
                            gramatica[non_terminal] = producciones

                gramaticas.append(gramatica)

        return gramaticas


def contieneXnumero(lista):
    patron = re.compile(r'^X\d+$')
    return any(patron.match(elemento) for elemento in lista)

def customPrint(text, type: Literal["green", "red", "purple"] = "green"):
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    PURPLE = '\033[95m'
    ACTIVECOLOR = GREEN

    if type == "green":
        ACTIVECOLOR = GREEN
    elif type == "red":
        ACTIVECOLOR = RED
    else:
        ACTIVECOLOR = PURPLE
    
    print(f"{ACTIVECOLOR}{text}{RESET}")

nombre_archivo = 'Proyecto.txt'
gramaticas = leer_gramaticas_desde_archivo(nombre_archivo)

for i, gramatica in enumerate(gramaticas):
    grammerLetter = "X"
    customPrint(f"Gramática {i + 1}:", "purple")

    print(gramatica)

    customPrint("Gramatica Transformada: ", "purple")

    startSymbol = list(gramatica.keys())[0]

    NormalizeCFG = NormalFormCFG(gramatica, startSymbol)

    if contieneXnumero(list(NormalizeCFG.grammar.keys())):
        grammerLetter = "G"

    Chumsky = CNF(NormalizeCFG.grammar, grammerLetter)


    for nonTerminal, productions in Chumsky.grammar.items():
        production_strings = [' '.join(production) for production in productions]
        print(f"{nonTerminal} → {' | '.join(production_strings)}")



    cyk = CYK(Chumsky.grammar, startSymbol)

    string = "0 0 1 0"

    belongs, cyk_table = cyk.cykParser(string)

    cyk.printCykTable(cyk_table, string)


    if belongs:
        customPrint(f"La cadena '{string}' pertenece al lenguaje.")
    else:
        customPrint(f"La cadena '{string}' NO pertenece al lenguaje.", "red")
