import itertools
from collections import defaultdict
from collections.abc import Set, Mapping, Callable
from typing import Iterable, MutableMapping, NamedTuple, Any

from .grammar import GrammarBase
from .common import Word, Symbol, PATTERNS, Rule, EOD, Semantic, Parser, LRMethod, LLMethod
from .lr.automaton import LR0Automaton
from .lr.tables import LRTable, LRParser
from .ll1 import LL1Table, LL1Parser
from .semantic import DictSemantic
from .utils import OrderedSet


class GrammarComponents(NamedTuple):
    terminals:Iterable[Symbol]
    axiom:Symbol
    rules_by_var:MutableMapping[Symbol, Set[Rule]]

class GrammarBuilder :  # static methods
    @staticmethod
    def parse_right(s) -> OrderedSet[Word]:
        """
            s syntax : word [ | word ]*
        """
        return OrderedSet[Word]( Word.from_string(s) for s in PATTERNS.SEPARATOR.split(s) )

    @staticmethod
    def decompose_line(line: str) -> tuple[Symbol, OrderedSet[Word]]:
        """
            decompose line
            line syntax :  symbol ->  word [ | word]*
        """
        parts = PATTERNS.ARROW.split(line)
        assert len(parts) == 2, f"{line} : Error : line must contain exactly one arrow sign"
        return Symbol(parts[0]), GrammarBuilder.parse_right(parts[-1])

    @staticmethod
    def parse_line(line) -> OrderedSet[Rule]:
        """
            l : stripped string
            returns list of Rules (Rules have same left side)
        """
        left, right = GrammarBuilder.decompose_line(line)
        return OrderedSet( Rule(left, word) for word in right )

    @staticmethod
    def from_rules(rules : Iterable[Rule]) -> GrammarComponents:
        """
            Static method
            Creates grammar from rules
            rules : Iterable of rules.
                    left variable of the first rule is regarded as axiom
            returns Grammar instance
        """
        # rules by var :
        rbv: MutableMapping[Symbol, OrderedSet[Rule]]  = defaultdict(OrderedSet[Rule])
        symbols: OrderedSet[Symbol] = OrderedSet[Symbol]()  # symbols (terminals or variables)
        for rule in rules:
            symbols.update(set(rule.right))
            symbols.add(rule.left)
            rbv[rule.left].add(rule)

        assert EOD not in symbols, f"forbidden symbol : {EOD}"
        return GrammarComponents(
            terminals = symbols - rbv.keys(),
            axiom = next(iter(rbv)),
            rules_by_var = dict(rbv) # same mapping without default
        )


    @staticmethod
    def from_string(source : str) -> GrammarComponents:
            """
                Static method
                returns new Grammar instance
                source : multiline string containing context-free grammar definition. e.g :
                    E -> E + T | T
                    T -> T * F | F
                    F -> * F  | ( E ) | i
                symbols must be separated by at least one blank
                the first used variable is regarded as axiom
            """
            lines = filter( bool,  map(str.strip, source.splitlines()) ) #iterator through non empty stripped lines
            rules = itertools.chain.from_iterable(map(GrammarBuilder.parse_line, lines)) #iterator through rules
            return GrammarBuilder.from_rules(rules)


class ParserBuilder:

    @staticmethod
    def from_dict(definitions: Mapping[str, Callable], method:LRMethod|LLMethod|str = LRMethod.LALR1) -> Parser:
        """
            create LALR(1) parser from dictionary :
                key : grammar multirule strings
                value : callable (synthetised attribute computation)

        """
        try:
            method = LRMethod(method)
        except ValueError:
            try:
                method = LLMethod(method)
            except ValueError:
                raise ValueError(f'{method} is not a correct method')

        #dico = {rule: definitions[line] for line in definitions for rule in GrammarBuilder.parse_line(line)}
        sem = DictSemantic(definitions)
        grammar = GrammarBase(*GrammarBuilder.from_rules(sem.rules()))

        if isinstance(method,LRMethod):
            return LRParser(
                table = LRTable(LR0Automaton(grammar), method),
                default_semantic = sem
            )
        else:
            return LL1Parser(
                table = LL1Table(grammar),
                default_semantic = sem
            )



