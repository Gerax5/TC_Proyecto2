class CNF:
    def __init__(self, grammar, newNonTerminalLetter = "X"):
        self.characters = "*/-+()$%&#"
        self.grammar = grammar
        self.newNonTerminalLetter = newNonTerminalLetter
        self.counter = 0
        self.terminalMap = {}
        self.transformarACNF()
        # print(self.grammar)
    
    def transformarACNF(self):
        newGrammar = {}

        def getNewNonTerminal():
            newNT = f"{self.newNonTerminalLetter}{self.counter}"
            self.counter += 1
            return newNT

        def getFilterGramar():
            filterGrama = []

            # print(newGrammar)
            
            for rule in list(newGrammar.values()):
                if len(rule) == 1:
                    filterGrama.append(rule)
                else:
                    should_exclude = False
                    for item in rule:
                        if len(item) > 1: 
                            should_exclude = True
                            break

                    if not should_exclude:
                        filterGrama.append(rule)
            
            return filterGrama

        def getKeyforValue(value):
            keyFound = None
            for key, valueSet in newGrammar.items():
                if value in valueSet:
                    keyFound = key
                    break 
            return keyFound

        for nonTerminal, productions in self.grammar.items():
            newProductions = set()
            # print(self.terminalMap)
            for production in productions:
                if len(production) > 2:
                    first, *rest = production
                    if first.islower() or first.isnumeric() or first in self.characters:
                        if first in self.terminalMap:
                            first = self.terminalMap[first]
                        else:
                            self.terminalMap[first] = getNewNonTerminal()
                            newGrammar[self.terminalMap[first]] = {(first,)}
                            first = self.terminalMap[first]

                    newNonTerminal = getNewNonTerminal()
                    newProductions.add((first, newNonTerminal))
                    for index, symbol in enumerate(rest[:-1]):
                        if symbol.islower() or symbol.isnumeric() or symbol in self.characters:
                            if symbol in self.terminalMap:
                                symbol = self.terminalMap[symbol]
                            else:
                                symbolNT = getNewNonTerminal()
                                self.terminalMap[symbol] = symbolNT
                                newGrammar[symbolNT] = {(symbol,)}
                                symbol = symbolNT

                        if index + 1 == len(rest[:-1]):
                            if rest[-1].islower() or rest[-1].isnumeric() or rest[-1] in self.characters:
                                if rest[-1] in self.terminalMap:
                                    nextNonTerminal = self.terminalMap[rest[-1]]
                                else:
                                    nextNonTerminal = getNewNonTerminal()
                                    self.terminalMap[rest[-1]] = nextNonTerminal
                                    newGrammar[nextNonTerminal] = {(rest[-1],)}
                            else:
                                nextNonTerminal = rest[-1]
                        else:
                            nextNonTerminal = getNewNonTerminal()

                        if {(symbol, nextNonTerminal)} in getFilterGramar():
                            matches = [item for item in newProductions if newNonTerminal in item]
                            if matches:
                                newProductions.remove(matches[0])
                                newValue = tuple(s for s in matches[0] if s != newNonTerminal)
                                keyForValue = getKeyforValue((symbol, nextNonTerminal))
                                newValue += (keyForValue,)
                                newProductions.add(newValue)
                        else:
                            newGrammar[newNonTerminal] = {(symbol, nextNonTerminal)}
                            newNonTerminal = nextNonTerminal
                elif len(production) == 2:
                    left, right = production
                    if left.islower() or left.isnumeric() or left in self.characters:
                        if left not in self.terminalMap:
                            self.terminalMap[left] = getNewNonTerminal()
                            newGrammar[self.terminalMap[left]] = {(left,)}
                        left = self.terminalMap[left]
                    if right.islower() or right.isnumeric() or right in self.characters:
                        if right not in self.terminalMap:
                            self.terminalMap[right] = getNewNonTerminal()
                            newGrammar[self.terminalMap[right]] = {(right,)}
                        right = self.terminalMap[right]
                    newProductions.add((left, right))
                else:
                    symbol = production[0]
                    # if symbol.islower() or symbol.isnumeric():
                    #     # if symbol not in self.terminalMap:
                    #     #     self.terminalMap[symbol] = getNewNonTerminal()
                    #     #     newGrammar[self.terminalMap[symbol]] = {(symbol,)}
                    #     symbol = self.terminalMap[symbol]
                    newProductions.add((symbol,))
            newGrammar[nonTerminal] = newProductions

        self.grammar = newGrammar
