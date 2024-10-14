class CYK:
    def __init__(self, rules, startSymbol="S"):
        self.rules = rules
        self.startSymbol = startSymbol


    def getNonTerminals(self, production):
        result = []
        production_tuple = tuple(production)
        for non_terminal, productions in self.rules.items():
            if production_tuple in productions:
                result.append(non_terminal)
        return result


    def cykParser(self, word):
        word = word.split(" ") 
        n = len(word)
        table = [[set() for _ in range(n)] for _ in range(n)]

        for i in range(n):
            terminals = self.getNonTerminals([word[i]])
            table[i][i].update(terminals)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1 
                for k in range(i, j):
                    for B in table[i][k]:
                        for C in table[k + 1][j]:
                            non_terminals = self.getNonTerminals([B, C])
                            table[i][j].update(non_terminals)

        return self.startSymbol in table[0][n - 1], table
    
    def printCykTable(self, table, word):
        word = word.split(" ") 
        n = len(word)
        print("Tabla CYK:")
        for i in range(n):

            if (i == 0):
                for j in range(n-i):
                    print(f"{word[j]}".center(10), end=' ')
                print()
                for j in range(n-i):
                    print("-----".center(10), end=' ')
                print()
                

            for j in range(n - i):
                cell = table[j][j + i]
                symbols = ','.join(cell)
                print(f"{symbols}".center(10), end=' ')
            print()
