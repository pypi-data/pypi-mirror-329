"""
    Context-free grammars.
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
import re
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from types import SimpleNamespace
from typing import Callable, TypeAlias, Protocol
from typing import NamedTuple
from typing import Any
from enum import Enum


class LLMethod(str,Enum):
    LL1 = 'LL1'

class LRMethod(str,Enum):
    LR0 = 'LR0'
    SLR1 = 'SLR1'
    LALR1 = 'LALR1'

# PATTERNS
PATTERNS = SimpleNamespace()
PATTERNS.SPACE = re.compile(r'\s')
PATTERNS.ARROW = re.compile(r'\s*(?:->|\N{Rightwards Arrow})\s*')
PATTERNS.SEPARATOR = re.compile(r'\s*[|]\s*')

latex_translate_dict = {ord(x): '\\' + x for x in r'"%$_{}#&'}
latex_translate_dict.update({ord('\\'): '\\backslash{}', ord('~'): '\\textasciitilde{}',
                             ord('-'):'\\text{-}', ord('+'):'\\text{+}'})

def set_to_latex(s) :
    return r'\ensuremath{\{'+ ', '.join(str(x) for x in s) + r'\}}'


class Symbol (str) :
    """ Non empty space free string
    """
    def __new__(cls, s):
        assert s!='' and PATTERNS.SPACE.search(s) is None, f"{s} : invalid symbol"
        return super(Symbol, cls).__new__(cls, s)
    def to_latex(self):
        return self.translate(latex_translate_dict)

# reserved symbols
GRAMMAR_START = Symbol('_start')
EOD = Symbol('#')
EPSILON = Symbol('\N{Greek Small Letter Epsilon}') #'ε'


class Word (tuple) :
    """
        Immutable sequence of non-EPSILON Symbol(s)
        constructor : Word ( * symbols )
    """
    def __new__(cls, *parts):
        """
            *parts :  symbols.
            NB : EPSILON occurrences allowed but erased in Word content.
        """
        assert all(isinstance(x,Symbol) for x in parts), f"{parts} : each word component must be a symbol"
        # return super(Word, cls).__new__(cls, tuple(parts))
        return super().__new__(cls, filter(lambda s : s!=EPSILON, parts))

    def __str__(self):
        return EPSILON if self == () else ' '.join(self)
    def __repr__(self):
        return 'Word' + super().__repr__()

    def to_latex(self, separator=r'\ '):
        return r'\varepsilon{}' if self == () else separator.join(symbol.to_latex() for symbol in self)

    @staticmethod
    def from_string(s:str) -> 'Word':
        """
        :param s: sequence of symbols separated by space(s). May be empty
        :return: Word
        """
        s = s.strip()
        return Word( *map(Symbol, s.split()) ) if s != '' else Word()

class Rule (NamedTuple) :
    left: Symbol
    right: Word
    # class Rule(namedtuple('Rule', ('left', 'right'))):
    """
        Context free grammar rule (immutable)
        left : Symbol
        right : Word
    """
    # def __new__(cls, left, right):
    #     assert isinstance(left,Symbol)
    #     assert isinstance(right,Word)
    #     return super(Rule, cls).__new__(cls, left, right)
    def __repr__(self):
        return f'{self.__class__.__name__}({self})'
    def __str__(self):
        return f'{self.left} \N{Rightwards Arrow} {self.right}'
    def to_latex(self):
        return rf'${self.left.to_latex()}\ \rightarrow\ {self.right.to_latex()}$'

    @classmethod
    def from_string(cls, line:str):
        """
        :param line: string representation of rule : symbol arrow  word
        :return:
        """
        parts = PATTERNS.ARROW.split(line)
        assert len(parts) == 2, f"{line} : Error : line must contain exactly on arrow sign"
        left = Symbol(parts[0])
        right = Word.from_string(parts[1])
        return Rule(left, right)



class ConflictError(Exception) :
    pass

class ParseError(Exception) :
    pass

class Token(Protocol):
    type: str
    value: Any

SynthesisFunction: TypeAlias = Callable[[list[Any],SimpleNamespace, SimpleNamespace], Any]
TokenValueFunction: TypeAlias = Callable[[Token], Any]

class Semantic:
    __metaclass__ = ABCMeta
    """ define semantic actions  (synthetised attributes only)
        3 methods
            start-synth() : returns calculus associated with AST root
            rule_synth(rule) : returns calculus applying to rule
            token_semantic() : returns calculus applying to tokens
    """
    @abstractmethod
    def start_synth(self) -> SynthesisFunction:
        """
            returns function which to apply at the top of AST.
        """
        pass
    @abstractmethod
    def rule_synth(self, rule : Rule) -> SynthesisFunction:
        """
            returns function to apply for each rule instance
        """
        pass
    @abstractmethod
    def token_semantic(self) -> TokenValueFunction:
        """
            returns function to apply for tokens
        """
        pass

class BasicSemantic(Semantic):
    _default_functions = NamedTuple('default',(('start',Callable),('rule',Callable),('token',Callable)))(
        start = lambda p, _, __: p[0],
        rule = lambda p, _, __: True,
        token = lambda token: token.value,
    )
    _start_f, _rule_f, _token_f = None, None, None

    def start_synth(self) -> SynthesisFunction:
        return self._start_f  or self._default_functions.start

    def rule_synth(self, rule : Rule) -> SynthesisFunction:
        return self._rule_f or self._default_functions.rule
        # return lambda p, run, _ : f'{run.var} ( {" ".join(map(str,p))} )'

    def token_semantic(self) -> TokenValueFunction:
        return self._token_f or self._default_functions.token


class Parser:
    __metaclass__ = ABCMeta
    """
        "abstract" class
        Concrete class should implement parse_tokens_impl method
    """

    _meta_default_semantic_instance = BasicSemantic()
    class BasicToken(NamedTuple):
        type:str
        value:Any
    def __init__(self, default_semantic : Semantic|None  = None):
        if default_semantic is not None:
           self._default_semantic_instance = default_semantic
        else:
           self._default_semantic_instance = Parser._meta_default_semantic_instance


    def parse(self, data:Iterable[str|Symbol], semantic: Semantic = None, verbose:bool=False) -> Any:
        """
            data : Iterable[str] ou Iterable[Symbol]
        """
        wrap = lambda x : Parser.BasicToken(type=x,value=x)
        return self.parse_tokens(map(wrap, iter(data)), semantic, verbose=verbose)

    def parse_tokens(self, tokens:Iterable[Token], semantic: Semantic|None = None, verbose:bool =False) -> Any:
        """
            tokens : Iterable[Token] (without End Of Data token)
            Token :  any class with 'type' and 'value' attributes
        """
        if semantic is None:
            semantic = self._default_semantic_instance
        return self.parse_tokens_impl(tokens, semantic, verbose )

    @abstractmethod
    def parse_tokens_impl(self, tokens:Iterable[Token], semantic: Semantic, verbose:bool =False):
        """
            tokens : Iterable[Token] (without End Of Data token)
            Token :  any class with 'type' and 'value' attributes
        """
        pass

    @property
    @abstractmethod
    def method(self) -> LRMethod | LLMethod:
        pass

    @property
    @abstractmethod
    def table(self) -> Any: #'LRTable' | 'LL1Table':
        pass

    @property
    @abstractmethod
    def grammar(self) -> 'GrammarBase':
        pass
