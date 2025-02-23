from sly import Lexer

from cfgrammar import Grammar
from cfgrammar.builder import ParserBuilder
from cfgrammar.semantic import DictSemantic

# g = Grammar.from_string('''
# Expression -> Unaire
# Unaire -> * Unaire | Postfixe
# Postfixe -> Postfixe + +  | Primaire
# Primaire -> i | ( Expression )
# ''');
#
# print(g)

class ExpLexer(Lexer):
    tokens = {NUMBER}
    literals = ('+', '*', '-', '/')  # un literal est un caractère traité comme un token
    NUMBER = '[0-9]+'
    ignore = ' \t'

g_postfix = Grammar.from_string('S → S S + | S S * | S S − | S S / | NUMBER')

parser_postfix = g_postfix.lr0_automaton().table('LALR1').parser()

print(parser_postfix.method)

lexer = ExpLexer()

tokens = [* lexer.tokenize('23 451+6*')]

print(tokens)

res = parser_postfix.parse_tokens(tokens)

print(res)

postfix_dict = {
    'S-> S S +' : lambda p,run,ns : p.S0 + p.S1,
    'S-> S S -' : lambda p,run,ns : p.S0 - p.S1,
    'S-> S S *' : lambda p,run,ns : p.S0 * p.S1,
    'S-> S S /' : lambda p,run,ns : p.S0 / p.S1,
    'S-> NUMBER' : lambda p,run,ns : int(p.NUMBER)
}
res = parser_postfix.parse_tokens(
    tokens,
    semantic = DictSemantic(postfix_dict)
)

print(res)

other_parser = ParserBuilder.from_dict(postfix_dict,'SLR1')

print(other_parser.method)
print(other_parser.grammar)

res = other_parser.parse_tokens(tokens)
print(res)
