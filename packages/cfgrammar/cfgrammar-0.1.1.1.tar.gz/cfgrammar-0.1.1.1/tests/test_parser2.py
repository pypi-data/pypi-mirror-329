from cfgrammar import Grammar
from cfgrammar.builder import ParserBuilder
from cfgrammar.semantic import BasicSemantic
from cfgrammar.semantic import DictSemantic

def unique(p,run,sn):
    print(p,run,sn)
dico = {
    'E -> E + T ': unique,
    'E -> T' : unique,
    'T -> T * F ': unique,
    'T -> F' : unique,
    'F -> ( E )' : unique,
    'F -> 0|1|2|3|4|5|6|7|8|9' : unique,
}



sem = DictSemantic(dico)

print (sem.token_semantic())
parser = ParserBuilder.from_dict(dico)

print(parser.grammar.to_compact_string())

print(parser.parse('2*(4+5*(1+1))'))
# print(parser.method)
# print(parser.table.to_markdown())