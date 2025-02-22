"""
    Context-free grammars. LR0/SLR1/LALR1 parsing tools
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
import itertools
from collections import defaultdict
from typing import NamedTuple, Any

from types import MappingProxyType

from collections.abc import Iterable, Set
from collections.abc import Mapping

from enum import Enum

import pandas

from ..grammar import GrammarBase

from ..common import LRMethod, Token
from ..common import GRAMMAR_START
from ..common import EOD
from ..common import Symbol
from ..common import Rule
from ..common import ConflictError
from ..common import ParseError
from ..common import Parser

from .automaton import StateId
from .automaton import LR0Automaton

from .lalr import LALR1Predictive, _LALR1PredictiveI

from ..semantic import RuleRun
from ..semantic import Semantic


class Key(NamedTuple):
    state_id: StateId
    symbol: Symbol
    def __str__(self):
        return f'({self.state_id},{self.symbol})'


class ActionType(Enum):
    S = 'Shift'
    R = 'Reduce'
    A = 'Accept'

    def __str__(self):
        return self.name


class Action(NamedTuple): # (namedtuple('Action', ['type', 'arg'])):
    type: ActionType | None
    arg : StateId | Rule | None
    def __str__(self):
        return f'<{self.type}({self.arg})>'


class LRTable:
    """
        dictionary
        keys : tuple: (state_id, symbol)
        values : tuple (Action|None, action argument : StateId|Rule|None )
        e.g. t[(3,'a')] = (Action.S, 6)
    """

    @staticmethod
    def _conflict_message(key, old, new) -> str:
        conflict_name = f'{old.type.value}/{new.type.value}'
        return f'conflict {conflict_name} at {key} : {old} vs {new}'

    class _InternalDict(dict[Key, Action]):
        def __init__(self, raise_exception: bool):
            super().__init__()
            self.__conflicts = defaultdict(set)
            self.raise_exception = raise_exception

        def __setitem__(self, key: Key, new_val):
            if key in self:   # conflict
                self.__conflicts[key].add(self[key])
                self.__conflicts[key].add(new_val)
                if self.raise_exception:
                    raise ConflictError(LRTable._conflict_message(key, self[key], new_val))
            else:
                dict.__setitem__(self, key, new_val)

        @property
        def conflicts(self) -> Mapping[Key,set[Action]]:
            return MappingProxyType(self.__conflicts)

    def __init__(self, automaton:LR0Automaton, method = LRMethod.SLR1, raise_exception:bool = True):
        """
            states_ids  :  Iterable[int]
            grammar : Grammar
            raise_exception : bool
        """
        super().__init__()
        self.__internal = LRTable._InternalDict(raise_exception)
        self._method: LRMethod = LRMethod(method)
        self._states_ids: Iterable[int] = range(len(automaton.states))
        self._grammar: GrammarBase = automaton.grammar
        self._terminals: tuple[Symbol,...] = (*automaton.grammar.terminals, EOD)
        self._variables: Set[Symbol] = automaton.grammar.variables
        self._predictive: LALR1Predictive | None = None

        match method:
            case LRMethod.LR0:
                reduce_letters = lambda _,__: self._terminals
            case LRMethod.SLR1:
                reduce_letters = lambda rule, _: self._grammar.suiv[rule.left] if rule.left != GRAMMAR_START else EOD
            case LRMethod.LALR1:
                self._predictive = _LALR1PredictiveI(automaton)
                reduce_letters = lambda rule, state_id: self._predictive[state_id][rule]
            case _:
                reduce_letters = None

        accepting_state = automaton.transitions[0][self._grammar.axiom]

        table = self.__internal
        table[Key(accepting_state.id, EOD)] = Action(ActionType.A, None)
        for state in automaton.states:
            for r in state.reduce_rules() :
                for letter in reduce_letters(r,state.id):
                    table[Key(state.id, letter)] = Action(ActionType.R, r.base_rule)
            for letter, dest in automaton.transitions[state.id].items():
                if automaton.grammar.is_var(letter) :
                    table[Key(state.id, letter)] = Action(None, dest.id)
                else :
                    table[Key(state.id, letter)] = Action(ActionType.S, dest.id)

    def __getitem__(self, key):
        return self.__internal.get(key)

    def get(self,key,default_value):
        return self.__internal.get(key, default_value)

    def items(self) -> Iterable[tuple[Key,Action]]:
        return self.__internal.items()

    def keys(self) -> Iterable[Key]:
        return self.__internal.keys()

    @property
    def method(self) -> LRMethod:
        return self._method

    @property
    def grammar(self) -> GrammarBase:
        return self._grammar

    @property
    def predictive(self) -> LALR1Predictive:
        return self._predictive


    def conflicts(self) -> Mapping[Key,set[Action]]:
        return self.__internal.conflicts

    def get_conflicts_messages(self) -> [str, ...]:
        return [LRTable._conflict_message(k, car, other) for k, (car, *cdr) in self.conflicts().items() for other in cdr]

    def has_conflict(self) -> bool:
        return bool(self.__internal.conflicts)

    def parser(self, default_semantic: bool = None) -> 'LRParser':
        return LRParser(self, default_semantic)

    def to_pandas(self, latex: bool = False) -> pandas.DataFrame:
        if self.has_conflict() :
            raise ConflictError("this table has conflicts. Use .get_conflicts() method")
        import pandas
        index = [*self._terminals, *self._variables]
        df = pandas.DataFrame(dict.fromkeys(self._states_ids, ''), index = index)
        for (state, symbol), (t,a) in self.items():
            if latex and isinstance(a,Rule) :
                a = a.to_latex()
            t = (t or '') and f'[{t}]'
            df.loc[symbol,state] = f'{t} {a}'
        df.columns.name = self._method
        if latex :
            df.index = df.index.map(Symbol.to_latex)
        return df

    def to_latex(self) -> str:
        df = self.to_pandas(latex=True)
        styler = df.style
        styler.set_table_styles([
            {'selector': 'midrule,toprule,bottomrule', 'props': ':hline; :hline;'},
        ], overwrite=False)
        # styler.set_table_styles({
        #     '\#': [{'selector': 'td,th', 'props': 'border-bottom : solid 3pt darkgrey'}, ]
        # }, overwrite=False, axis=1)
        # styler.set_table_styles([
        #     {'selector': 'rowcolors', 'props': ':{1}{pink}{red};'}
        # ], overwrite=False)
        import re
        return re.sub(r'#.*',r'/'
                               r'\g<0>\\hline',styler.to_latex(column_format=f'|c|*{{{len(df.columns)}}}{{c|}}'))

    def to_html(self) -> str:
        styler = self.to_pandas().style
        td = {'selector': 'td', 'props': 'border : solid 0.8pt; text-align:left'}
        th = {'selector':'th','props': 'text-align:center'}
        styler.set_table_styles({
            '#' : [{'selector': 'td,th', 'props': 'border-bottom : solid 3pt darkgrey'}, ]
        }, overwrite=False, axis=1)
        styler.set_table_styles([td, th],overwrite=False)
        return styler.to_html(hrules=True)

    def to_markdown(self) -> str:
        df = self.to_pandas()
        return df.to_markdown()

    def _repr_html_(self) -> str:
        return self.to_html()


class RunManager:
    def __init__(self, semantic : Semantic, verbose = False):
        self._stack = []
        self._token_semantic = semantic.token_semantic()
        self._semantic = semantic
        self._verbose = verbose

    def create_run(self, rule:Rule) -> None:
        created = RuleRun(rule=rule, semantic=self._semantic)
        self._verbose and print(f'    run : {created}')
        if len(rule.right)>0 :
            created.add_results(* self._stack[-len(rule.right):])
            del self._stack[-len(rule.right):]
        if created.is_complete() :
            self.add_result(created.synthetised)

    def add_token_result(self,token)-> None:
        self.add_result(self._token_semantic(token))

    def add_result(self, value: Any)-> None:
        self._stack.append(value)

    def get_result(self) -> Any:
        return self._stack[0]


class LRParser(Parser) :

    def __init__(self, table : LRTable, default_semantic:Semantic|None = None):
        super().__init__(default_semantic)
        self.__table: LRTable = table

    @property
    def method(self):
        return self.table.method

    @property
    def table(self) -> LRTable:
        return self.__table

    @property
    def grammar(self) -> GrammarBase:
        return self.table.grammar

    def parse_tokens_impl(self, tokens: Iterable[Token], semantic: Semantic, verbose:bool =False):
        """
            Tokens parsing
            tokens : Iterable[Token] (without End Of Data token)
            Token :  any class with 'type' and 'value' attributes
            semantic : Instance de Semantic (actions sémantiques associées) ou None
            Return : True if semantic is None or else axiom synthetised attribute
        """
        table = self.__table
        token_input = itertools.chain(tokens, [Parser.BasicToken(EOD, None)])
        current = next(token_input)
        stack = [0]
        sem_manager = RunManager(semantic, verbose = verbose)
        action_type , action_arg = table.get((stack[-1], current.type), (None, None))
        verbose and print(f'stack:{stack}, current: {current.type}')
        while action_type != ActionType.A :
            verbose and print(f'.. {action_type} {action_arg}')
            if action_type == ActionType.S :
                sem_manager.add_token_result(current)
                stack.append(action_arg)
                current = next(token_input)
            elif action_type == ActionType.R :
                sem_manager.create_run(action_arg)
                if len(action_arg.right)>0 :
                    del stack[-len(action_arg.right):]
                _, dest = table[(stack[-1],action_arg.left)]
                stack.append(dest)
            else :
                raise ParseError(f"Syntax Error. action_type : {action_type} stack : {stack} current : {current.type}  {list(token_input)}")
            action_type , action_arg = table.get((stack[-1], current.type), (None, None))
            verbose and print(f'stack:{stack}, current: {current.type}')

        sem_manager.create_run(self.__table.grammar.starting_rule)
        return sem_manager.get_result()



