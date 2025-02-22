from cfgrammar import Grammar
from cfgrammar.builder import ParserBuilder

parser = ParserBuilder.from_dict({
    'E -> E + T ': lambda p,_,__ : p.E + p.T,
    'E -> T' : lambda p,_,__: p.T,
    'T -> T * F ': lambda p,_,__ : p.T * p.F,
    'T -> F' : lambda p,_,__: p.F,
    'F -> ( E )' : lambda p,_,__ : p.E,
    'F -> 0|1|2|3|4|5|6|7|8|9' : lambda p,_,__ : int(p[0])
})
print(parser.grammar.to_compact_string())

print(parser.parse('2*(4+5*(1+1))'))
print(parser.method)
print(parser.table.to_markdown())