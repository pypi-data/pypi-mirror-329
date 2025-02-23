from cfgrammar.builder import ParserBuilder

parser = ParserBuilder.from_dict({
    'E -> E + T ': lambda p,*_ : p.E + p.T,
    'E -> T' : lambda p,*_: p.T,
    'T -> T * F ': lambda p,*_ : p.T * p.F,
    'T -> F' : lambda p,*_: p.F,
    'F -> ( E )' : lambda p,*_ : p.E,
    'F -> 0|1|2|3|4|5|6|7|8|9' : lambda p,*_ : int(p[0])
})
print('Value: ',parser.parse('2*(4+5*(1+1))'))
print(parser.grammar)
print(parser.method)

from cfgrammar.semantic import GraphvizAST
display_ast  = GraphvizAST()
dot_source = parser.parse('2*(4+5*(1+1))',display_ast)

from graphviz import Source
Source(dot_source).view()

from cfgrammar.semantic import LatexForestAST
display_latex_ast  = LatexForestAST()
latex_source = parser.parse('2*(4+5*(1+1))',display_latex_ast)


#print(parser.table.to_markdown())