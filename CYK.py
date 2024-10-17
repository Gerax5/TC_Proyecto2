from collections import defaultdict
from graphviz import Digraph
import time


class CYK:
    def __init__(self, rules, startSymbol="S"):
        self.rules = rules
        self.startSymbol = startSymbol
        self.nodeID = 0
        self.d = Digraph(f'Diagrama{0}', format='png')
        self.stack = []


    def getNonTerminals(self, production):
        result = []
        production_tuple = tuple(production)
        for non_terminal, productions in self.rules.items():
            if production_tuple in productions:
                result.append(non_terminal)
        return result

    def cykParser(self, word):
        startTime = time.perf_counter()
        word = word.split(" ") 
        n = len(word)
        table = [[set() for _ in range(n)] for _ in range(n)]
        back = [[defaultdict(list) for _ in range(n)] for _ in range(n)]

        for i in range(n):
            terminals = self.getNonTerminals([word[i]])
            table[i][i].update(terminals)
            for t in terminals:
                back[i][i][t].append(word[i])

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1 
                for k in range(i, j):
                    for B in table[i][k]:
                        for C in table[k + 1][j]:
                            non_terminals = self.getNonTerminals([B, C])
                            table[i][j].update(non_terminals)
                            for A in non_terminals:
                                back[i][j][A].append((B, C, k))

        endTime = time.perf_counter()

        totalTime = endTime - startTime

        print(f"\033[92mTiempo: {totalTime * 1000:.4f} ms \033[0m")

        parsetree = self.buildSintaticTree(back, 0, n - 1, self.startSymbol)
        print(parsetree)
        if parsetree:
            graph = self.treeGraph(parsetree)
            self.d.render(f'Diagrama/Diagrama{2}', cleanup=False)
            graph.render("Tree/Tree{0}",cleanup=False)
 
        return self.startSymbol in table[0][n - 1], table

    
    def buildSintaticTree(self, back, i, j, symbol):
        if i == j:
            derivations = back[i][j].get(symbol, [])
            if derivations:
                return (symbol, derivations[0])
            else:
                return None
        else:
            derivations = back[i][j].get(symbol, [])
            if not derivations:
                return None
            B, C, k = derivations[0]
            left_tree = self.buildSintaticTree(back, i, k, B)
            right_tree = self.buildSintaticTree(back, k + 1, j, C)
            return (symbol, left_tree, right_tree)
    
    def treeGraph(self, tree, graph=None, parent=None):
        if graph is None:
            graph = Digraph(format="png")
            graph.node(str(id(tree)), tree[0])
            parent = str(id(tree))
        else:
            graph.node(str(id(tree)), tree[0])
            graph.edge(parent, str(id(tree)))

        if len(tree) == 2:
            graph.node(str(id(tree[1])), f'"{tree[1]}"')
            graph.edge(str(id(tree)), str(id(tree[1])))
        else:
            self.treeGraph(tree[1], graph, str(id(tree)))
            self.treeGraph(tree[2], graph, str(id(tree)))
        return graph
    
    
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
