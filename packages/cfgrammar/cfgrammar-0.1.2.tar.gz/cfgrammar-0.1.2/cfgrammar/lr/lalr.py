import itertools
from abc import ABCMeta
from collections import deque
from typing import Mapping, NamedTuple

from ..grammar import GrammarBase
from ..common import Symbol, Word
from ..common import EOD

from .automaton import LR0Automaton
from .automaton import _LR0Item

class _FirstEps(NamedTuple):
    first: set[Symbol]
    eps: bool

def _suffixes_props(w: Word, g:GrammarBase) -> Mapping[int, _FirstEps]:
    """
    :param w: word (right hand side of a rule)
    :param g: grammar
    :return: mapping
        keys : i such as w[i] is a variable
        values : two properties of suffixe w[i+1:]
            prem : set of terminals : First(w[i+1:])
            eps : bool : is w[i+1:] eps-productive ?
    """
    follows = dict[int, _FirstEps]()
    current, eps = set[Symbol](), True
    for i, x in zip(reversed(range(len(w))), reversed(w)):
        if g.is_var(x):
            follows[i] = _FirstEps(first=current.copy(), eps=eps)
        if x in g.eps_prod.vars:
            current |= g.prem[x]
        else:
            current = g.prem[x].copy() if g.is_var(x) else {x}
            eps = False
    return follows


class LALR1Predictive(tuple) :
    __metaclass__ = ABCMeta
    """
        Abstract class. Implemented by
                LALR1PredictiveI (iterative implementation)
                LALR1PredictiveR (recursive implementation)

        tuple (ordered by state ids) of dictionaries LR0_Item => set of predictive symbols
        e.g :
           pred[5][LR0Item(V->u.v)] is predictive symbol list for V->u.v in state 5
    """
    def __new__(cls, tuple_of_dict, automaton: LR0Automaton):
        instance = super().__new__(cls,  tuple_of_dict)
        instance.automaton = automaton
        return instance

    def display(self) -> None:
        for state_id, pred_dict in enumerate(self) :
            print(f'== state {state_id} ==')
            for item, pred in pred_dict.items() :
                print(f'  {item} , {list(pred.keys())}')

    def to_dot(self) -> str:
        preds = lambda state,item : ','.join(self[state.id][item].keys())
        # ⁞
        rules_list = lambda state: '\n'.join(map(lambda item: f'<tr><td align="left" cellpadding="4">{item}</td><td align="left" cellpadding="4" border="1" sides="L" style="dashed">{preds(state,item)}</td></tr>', state))
        node_state = lambda \
            state: f'{state.id} [id="{state.id}", label=<<table cellspacing="0" cellborder="0" style="rounded"><tr><td colspan="2" border="1" sides="b" cellpadding="2"><font color="red"><b>{state.id}</b></font></td></tr>{rules_list(state)}</table>>\n]'
        make_trans = lambda from_index, to_index, letter: f' {from_index}->{to_index} [label=<<i>{letter}</i>>]'
        transitions = ((from_index, dest[letter].id, letter) for from_index, dest in self.automaton.transitions.items() for letter
                       in dest)
        return '\n'.join(itertools.chain(
            ('digraph AutLR0 {', 'bgcolor=transparent', 'rankdir=LR', 'node[shape=plain]'),
            map(node_state, self.automaton.states),
            itertools.starmap(make_trans, transitions),
            ('}',)
        ))


class _LALR1PredictiveI(LALR1Predictive) :
    """
        Iterative implementation

        tuple (ordered by state ids) of dictionaries LR0_Item => set of predictive symbols
        e.g :
           pred[5][LR0Item(V->u.v)] is predictive symbol list for V->u.v in state 5
    """
    def __new__(cls, automaton: LR0Automaton):
        todo = deque()
        registered = tuple( {item:{} for item in state} for state in automaton.states )
        cf = {r: _suffixes_props(r.right, automaton.grammar) \
                        for r in ( *automaton.grammar.rules, automaton.grammar.starting_rule ) }

        def add_symbol(state_id : int, item : _LR0Item, symbol : Symbol) :
            if symbol not in registered[state_id][item] :
                already_visited = bool(registered[state_id][item])
                registered[state_id][item].update({symbol:None})
                todo.append((state_id,item,symbol,already_visited))

        def cascade(state_id: int, item: '_LR0Item', symbol: Symbol, already_visited: bool) :
                # saturation :
                if item.point_pos in cf[item.base_rule] : # variable
                    # if not already_visited :
                    #     print(f'first visit for {state_id}-{item}')
                    first = () if already_visited else cf[item.base_rule][item.point_pos].first
                    inherit = cf[item.base_rule][item.point_pos].eps * (symbol,)
                    for new_symbol in (*first,*inherit) :
                        for sat_item in item.saturation_step(automaton.grammar):
                            add_symbol(state_id,sat_item,new_symbol)
                # transition :
                if item.is_not_ending_point_rule() :
                    dest_state_id = automaton.transitions[state_id][item.follow_point].id
                    add_symbol(dest_state_id, item.shift(), symbol)

        add_symbol(0, automaton.states[0][0], EOD)
        while todo :
            cascade( * todo.popleft() )

        return super().__new__(cls,  registered, automaton)


class _LALR1PredictiveR(LALR1Predictive) :
    """
        Recursive implementation

        tuple (ordered by state ids) of dictionaries LR0_Item => set of predictive symbols
        e.g :
           pred[5][LR0Item(V->u.v)] is predictive symbol list for V->u.v in state 5
    """
    def __new__(cls, automaton : LR0Automaton):
        registered = tuple( {item:{} for item in state} for state in automaton.states )
        cf = {r: _suffixes_props(r.right, automaton.grammar) \
                        for r in ( *automaton.grammar.rules, automaton.grammar.starting_rule ) }

        def add_symbol(state_id : int, item : _LR0Item, symbol : Symbol) :
            if symbol not in registered[state_id][item] :
                already_visited = bool(registered[state_id][item])
                registered[state_id][item].update({symbol:None})
                # saturation :
                if item.point_pos in cf[item.base_rule] : # variable
                    first = () if already_visited else cf[item.base_rule][item.point_pos].first
                    inherit = cf[item.base_rule][item.point_pos].eps * (symbol,)
                    for new_symbol in (*first,*inherit) :
                        for sat_item in item.saturation_step(automaton.grammar):
                            add_symbol(state_id,sat_item,new_symbol)
                # transition :
                if item.is_not_ending_point_rule() :
                    dest_state_id = automaton.transitions[state_id][item.follow_point].id
                    add_symbol(dest_state_id, item.shift(), symbol)

        add_symbol(0, automaton.states[0][0], EOD)

        return super().__new__(cls,  registered, automaton)

