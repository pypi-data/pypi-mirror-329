from cfgrammar import Grammar
from cfgrammar.common import LRMethod
from cfgrammar.ll1 import LL1Table
from cfgrammar.lr.tables import LRTable

from cfgrammar.semantic import *





g = Grammar.from_string('''
    S → ( S ) S | C
    C → T L
    L → , C |
    T →  a | b| c
''')

g = Grammar.from_string('''
    S → a S b S | T U
    T → c T | ε
    U →  d U | ε
''')
print(g)
print('eps_prod: ', g.eps_prod)
print('first: ', g.first)
print('follow: ',g.follow)
print('LL(1):', g.isLL1())
print(g.tableLL1().to_markdown())



# t = LL1Table(g,False)
# print(t.conflicts_str())
# print(t.to_markdown())
#
# t = LRTable(g.lr0_automaton(),'LALR1',False)
# print(t.to_markdown())
#
#
# parser = t.parser(LatexForestAST2(token_marker=''))
#
# print (parser.parse('(a,b)'))
#

a = g.lr0_automaton()

print(a)

t0 = a.table('LR0',False)
print(f'{t0.method} conflict:{t0.has_conflict()}')
t1 = a.table('SLR1')
print(f'{t1.method} conflict:{t1.has_conflict()}')
t2 = a.table('LALR1')
print(f'{t2.method} conflict:{t2.has_conflict()}')

# import graphviz
# graphviz.Source(t2.predictive.to_dot()).view()



for method in LRMethod :
    if g.isLR(method) :
        print(f'table {method.name}')
        print(g.tableLR(method).to_markdown())
    else:
        print(f'non {method.name}')
