import itertools


class NormalFormCFG:
    def __init__(self, grammar, startSymbol):
        self.grammar = grammar 
        self.startSymbol = startSymbol
        self.eliminarProduccionesEpsilon()
        self.eliminarProduccionesUnarias()
        self.eliminarSimbolosInutiles()

    
    def encontrarNullable(self):
        nullable = set()
        changed = True

        while changed:
            changed = False
            for nonTerminal, productions in self.grammar.items():
                for production in productions:            
                    if production == ['ε'] or all(symbol in nullable for symbol in production):
                        if nonTerminal not in nullable:
                            nullable.add(nonTerminal)
                            changed = True
        return nullable

    def eliminarProduccionesEpsilon(self):
        nullable = self.encontrarNullable()

        newGrammar = {}

        for nonTerminal, productions in self.grammar.items():
            newProductions = set()

            for production in productions:
                if production != ['ε']:  
                    nullablePositions = [i for i, symbol in enumerate(production) if symbol in nullable]

                    combinations = []
                    for r in range(len(nullablePositions) + 1):
                        for positionsToRemove in itertools.combinations(nullablePositions, r):
                            newComb = [symbol for i, symbol in enumerate(production) if i not in positionsToRemove]
                            combinations.append(tuple(newComb))
                    
                    newProductions.update(combinations)

            newProductions = {prod for prod in newProductions if prod}
            newGrammar[nonTerminal] = newProductions

        for nonTerminal, productions in newGrammar.items():
            if ('ε',) in productions:
                productions.remove(('ε',))

        self.grammar = newGrammar

    def eliminarProduccionesUnarias(self):
        unarias = []
        newGrammar = {}

        for nonTerminal, productions in self.grammar.items():
            newGrammar[nonTerminal] = set()
            for production in productions:
                if len(production) == 1 and production[0].isupper():
                    unarias.append((nonTerminal, production[0]))
                else:
                    newGrammar[nonTerminal].add(production)
        
        for A, B in unarias:
            visitados = set()
            cola = [B]
            while cola:
                actual = cola.pop()
                if actual not in visitados:
                    visitados.add(actual)
                    if actual in self.grammar:
                        for production in self.grammar[actual]:
                            if len(production) == 1 and production[0].isupper():
                                cola.append(production[0])
                            else:
                                newGrammar[A].add(production)

        self.grammar = newGrammar

    def eliminarSimbolosInutiles(self):
        generadores = set()
        cambiando = True

        while cambiando:
            cambiando = False
            for nonTerminal, productions in self.grammar.items():
                for production in productions:
                    if all(symbol.islower() or symbol.isnumeric() or symbol in generadores for symbol in production):
                        if nonTerminal not in generadores:
                            generadores.add(nonTerminal)
                            cambiando = True

        self.grammar = {
            nt: [p for p in productions if all(s.islower() or s.isnumeric() or s in generadores for s in p)]
            for nt, productions in self.grammar.items() if nt in generadores
        }
        
        alcanzables = {self.startSymbol}
        cambiando = True

        while cambiando:
            cambiando = False
            for nonTerminal in list(alcanzables):
                if nonTerminal in self.grammar:
                    for production in self.grammar[nonTerminal]:
                        for symbol in production:
                            if symbol.isupper() and symbol not in alcanzables:
                                alcanzables.add(symbol)
                                cambiando = True

        self.grammar = {
            nt: [p for p in productions if all(s.islower() or s.isnumeric() or s in alcanzables for s in p)]
            for nt, productions in self.grammar.items() if nt in alcanzables
        }
