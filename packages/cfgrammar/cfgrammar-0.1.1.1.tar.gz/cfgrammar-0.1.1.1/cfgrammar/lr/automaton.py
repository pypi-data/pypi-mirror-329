"""
    Context-free grammars. LR0/SLR1/LALR1 parsing tools
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
import itertools
from collections import deque, defaultdict

from collections.abc import Iterable, Mapping
from typing import TypeAlias
# from typing import Self, Any

from graphviz import Source

from ..common import GRAMMAR_START
from ..common import Symbol
from ..common import Rule
from ..common import Word

from ..grammar import GrammarBase
from ..utils import OrderedSet

StateId : TypeAlias = int


class _LR0Item:
    """
        tuple : (left_var, right_word, point_position)
    """

    def __init__(self, rule:Rule, point_pos: int):
        """

            private instance attributes :
                _rule : base rule
                _point_pos : point position
            public instance attributes :
        """
        # assert len(t) == 3
        left, right = rule
        assert 0 <= point_pos <= len(right), f"/{left}/{right}/{point_pos}/" # len(right)+1 positions for separator
        self.__rule = rule
        self.__point_pos = point_pos

    def __hash__(self):
        return (self.__rule, self.point_pos).__hash__()

    def __eq__(self ,other) :
        return (self.__rule, self.point_pos).__eq__((other.__rule, other.point_pos))

    def __str__(self) :
        k = self.point_pos
        before = Word(*self.right[0:k]) if k>0  else ''
        after =  Word(*self.right[k:]) if k<len(self.right) else ''
        return f'{self.left}  \N{RIGHTWARDS ARROW WITH TAIL}  {before} \u2022 {after}'

    def __repr__(self) :
        return self.__str__()

    @property
    def left(self) -> Symbol:
        """
            left part of the rule (variable symbol)
        """
        return self.__rule.left
    @property
    def right(self) -> Word:
        """
            right part of the rule (sequence of symbols)
        """
        return self.__rule.right
    @property
    def base_rule(self) -> Rule:
        """
            right part of the rule (sequence of symbols)
        """
        return self.__rule
    @property
    def point_pos(self) -> int:
        """
            point position (between 0 and len(right part))
        """
        return self.__point_pos
    @property
    def follow_point(self) -> Symbol | None:  # | None:
        """
            symbol following  point.
            None if point is at last position
        """
        try :
            return self.right[self.point_pos]
        except IndexError:
            return None

    def is_reduce_action_rule(self) -> bool:
        return self.point_pos == len(self.right) and self.left != GRAMMAR_START

    def is_not_ending_point_rule(self) -> bool:
        return self.point_pos < len(self.right)

    def saturation_step(self, grammar) -> tuple['_LR0Item',...]:
        """
            computes first step closure of this pointed rule
                grammar : related grammar
                return :  list [LR0Item]
        """
        if not grammar.is_var(self.follow_point):
            return tuple()
        else:
            return tuple(
                _LR0Item(rule=r, point_pos=0)
                for r in grammar.byVar[self.follow_point]
            )

    def shift(self) -> "_LR0Item":
        """
            create shifted rule
            param : grammar:
            return : LR0Item, shifting point to right
        """
        return _LR0Item(rule=self.__rule, point_pos=self.point_pos + 1)


class _LR0State(tuple[_LR0Item,...]):
    def __new__(cls, kernel: Iterable[_LR0Item], grammar, state_id: StateId):
        """
            _LR0State  : tuple [_LR0Item,...] (in construction order, so tuple begins with kernel)
            kernel :  tuple [_LR0Item,...]
            grammar : related grammar
        """
        items = OrderedSet[_LR0Item](kernel)
        todo = deque(kernel)
        while todo:
            item = todo.popleft()
            for new_item in item.saturation_step(grammar):
                if new_item not in items:
                    items.add(new_item)
                    todo.append(new_item)

        return super().__new__(cls, items)

    def __init__(self, kernel: tuple[_LR0Item,...], grammar, state_id: StateId):
        self.__kernel_cardinal = len(kernel)
        self.__grammar = grammar
        self.__id = state_id
        self.__reduce_action_rules = \
            tuple(r for r in self if r.is_reduce_action_rule())
        # compute transitions:
        trans = defaultdict(list)  # key : symbol, value : list of LR0Item
        for rule in self :
            if rule.is_not_ending_point_rule() :
                symbol = rule.follow_point
                trans[symbol].append(rule.shift())
        # same dict without default and replacing lists by tuples,
        # so self._transitions :  Mapping[Symbol,tuple[LR0Item,..]]
        self.__transitions = {x : tuple(l) for x ,l in trans.items()}

    @property
    def kernel(self) -> tuple[_LR0Item,...]:
        """
            state kernel (tuple)
        """
        return self[:self.__kernel_cardinal]
    @property
    def id(self) -> StateId:
        return self.__id
    @property
    def transitions(self) -> Mapping[Symbol,tuple[_LR0Item]]:
        return self.__transitions

    def reduce_rules(self) -> tuple[_LR0Item,...]:
        """
            returns tuple of "reduce_action" rules
        """
        return self.__reduce_action_rules

    def __str__(self) -> str:
        items = '\n'.join(f'   {s}' for s in (*self[:len(self.kernel)], '---', *self[len(self.kernel):]))
        return f'state {self.id}\n{items}\n'


class LR0Automaton:
    """
        LR0 automaton
        private instance attributes :
            _grammar : related grammar (Grammar instance)
        public instance attributes :
            states : states tuple, ordered by index
            kernels : dictionary
                key : state kernel (tuple of LR0Item)
                value : state (LR0State instance)
            transitions : dict (key : state index) of dict(key : symbol, value : state instance)
    """
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__kernels = dict()  # Mapping[tuple[_LR0Item,...], _LR0State]
        self.__create_automaton()
        self.__states = tuple(self.__kernels.values())  # states, ordered by index
        self.__transitions = {
            i: {letter:self.__kernels[dest] for letter, dest in state.transitions.items()}
            for i, state in enumerate(self.states)
        }

    def __ensure_state(self, kernel: tuple[_LR0Item,...]) -> tuple[_LR0State, bool]:
        """
            search or create a state for this kernel
            returns tuple ( state, is_new (boolean) )
        """
        try:
            return self.__kernels[kernel], False
        except KeyError:  # kernel unknown
            state = _LR0State(kernel, grammar=self.__grammar, state_id=len(self.__kernels))  # build state
                # new state, record it
            self.__kernels[kernel] = state  # record kernel
            return state, True

    def __create_automaton(self) -> None:
        """
            Creates states. Updates self._kernels dict
        """
        initial_kernel = (_LR0Item(rule=self.__grammar.starting_rule, point_pos=0),) #tuple
        initial_state, _ = self.__ensure_state(initial_kernel)
        todo = deque([initial_state])  #
        while todo:
            state = todo.popleft()
            # print (f'treating state {index[state]} : {state}')
            for kernel in state.transitions.values():
                dest, is_new = self.__ensure_state(kernel)
                if is_new:
                    todo.append(dest)

    @property
    def grammar(self) -> 'GrammarBase':
        return self.__grammar

    @property
    def states(self) -> tuple[_LR0State,...]:
        """
            tuple of automaton states, ordered by index
        """
        return self.__states

    @property
    def kernels(self) -> Mapping[tuple[_LR0Item,...], _LR0State]:
        """
            dictionary
                key : kernel
                value : state instance
        """
        return self.__kernels
    @property
    def transitions(self) -> Mapping[int, Mapping[Symbol, _LR0State]]:
        """
            dictionary
                key : state index
                value : dictionary
                    key : symbol,
                    value : LR0state
            e.g : transitions[i][s] -> state
        """
        return self.__transitions

    def __str__(self) -> str :
        trans_id = lambda state: {k:s.id for k,s in self.transitions[state.id].items()}
        return '\n'.join(f'{state}{trans_id(state)}\n------' for state in self.states)

    def to_dot(self, lalr = False ) -> str:
        """
            return DOT (graphviz source text) automaton representation
        """
        # if lalr :
        #     return '_LALR1PredictiveI'(self).to_dot()

        rules_list = lambda state : '\n'.join(map(lambda item : f'{item}<br align="left"/>',state))
        node_state = lambda state: f'{state.id} [id="{state.id}", label=<<font color="red"><b>{state.id}</b></font><br/>{rules_list(state)}>\n]'
        make_trans = lambda from_index, to_index, letter: f' {from_index}->{to_index} [label=<<i>{letter}</i>>]'
        transitions = ((from_index, dest[letter].id, letter) for from_index, dest in self.transitions.items() for letter in dest)
        return '\n'.join(itertools.chain(
            ('digraph AutLR0 {','bgcolor=transparent','rankdir=LR','node[shape=box,style=rounded]'),
            map(node_state, self.states),
            itertools.starmap(make_trans,transitions),
            ('}',)
        ))

    def to_gv(self, lalr = False) -> Source:
        """
            return graphviz object
        """
        return Source(self.to_dot(lalr = lalr))

    def _repr_svg_(self) -> str:
        return Source(self.to_dot(),format='svg').pipe(encoding='utf-8')

