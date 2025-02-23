"""
    Context-free grammars.
    (cc) CC BY-NC-SA Creative Commons -  Bruno.Bogaert@univ-lille.fr
"""
from collections import defaultdict
# from functools import total_ordering
from typing import NamedTuple
from collections.abc import Iterable, MutableSet, Callable
from collections.abc import Mapping
from collections.abc import MutableMapping
from collections.abc import Set

from .common import EOD
from .common import GRAMMAR_START
from .common import Symbol
from .common import Word
from .common import Rule
from .utils import OrderedSet

class Closure(NamedTuple):
    vars: set[Symbol]
    rules: set[Rule]

    def __repr__(self):
        return f'(vars={self.vars}, rules={self.rules})'

class GrammarBase:
    """ Context free grammar
    Attributes and pseudo attributes :
        terminals : set of terminals (Symbols)
        variables : set of variables (Symbols)
        axiom : axiom (Symbol)
        rules : rules iterator
        eps_prod : "epsilon-productive" property (vars : set of variables, rules : set of rules)
        productive : "productive property" (vars : set of variables, rules : set of rules)
        accessible : set of accessible variables
        prem : "First" sets  (dict of sets indexed by variables and rules)
        suiv : "Follow" sets  (dict of sets indexed by variables)
    """

    def to_compact_string(self) -> str:
        return '\n'.join(f'{left} -> {" | ".join(str(w) for v,w in rules)}' for left,rules in self.byVar.items())

    def to_latex(self) -> str:
        sep =r'\quad |\quad '
        inner = '\\\\\n'.join(rf'{left} &\longrightarrow\quad {sep.join(w.to_latex() for v,w in rules)}' for left,rules in self.byVar.items())
        return '\\begin{align*}\n'+ inner +'\n\\end{align*}\n'


    def _repr_latex_(self) -> str:
        return self.to_latex()

    def __repr__(self):
            return f'''{self.__class__.__name__}(
     terminals : {' '.join(self.terminals)}
     variables : {' '.join(self.variables)}
     axiom : {self.axiom}
     rules : {list(str(r) for r in self.rules)}
    )'''

    def __init__ (self,
                  terminals: Iterable[Symbol],
                  axiom: Symbol,
                  rules_by_var: MutableMapping[Symbol, Set[Rule]]
                  ) :

        assert axiom in rules_by_var.keys(), 'axiom {axiom} must have at least on rule'
        assert EOD not in terminals, 'EOD symbol "{EOD}" is reserved'
        assert EOD not in rules_by_var.keys(),'EOD symbol "{EOD}" is reserved'

        # main  definition attributes :
        self.terminals: list[Symbol] = list(terminals)
        self.terminals.sort()
        self.axiom: Symbol = axiom
        self.byVar: MutableMapping[Symbol,Set[Rule]] = rules_by_var  # dict of rulesets, indexed by var. e.g {'E':{('T','+','E'),('T')},'T':{('F','*','T'),('F')}, 'F':{'(E)',('x')}}

        # computed properties
        self.__eps_prod: Closure =  self.__compute_eps_prod()  # epsilon-productive vars and rules (type Closure)
        self.__productive: Closure = self.__compute_prod()  # productive vars and rules (type Closure)
        self.__accessible: set[Symbol] = self.__compute_accessible() # set of variables

        # waiting properties (computed when needed)
        self.__first: Mapping[Symbol | Rule,set[Symbol]] | None = None
        self.__follow : Mapping[Symbol,set[Symbol]] | None = None

    def get_vars(self) -> Iterable[Symbol]:
        return self.byVar.keys()

    @property
    def variables(self) -> set[Symbol]:
        return set(self.byVar.keys())
    @property
    def rules(self) -> Iterable[Rule]:
        for ruleset in self.byVar.values() :
            for r in ruleset :
                yield r
    @property
    def eps_prod(self):
        return self.__eps_prod
    @property
    def productive(self):
        return self.__productive
    @property
    def accessible(self) -> set[Symbol]:
        return self.__accessible
    @property
    def starting_rule(self) -> Rule:
        return Rule(GRAMMAR_START, Word(self.axiom))

    def is_reduced(self) -> bool:
        """
             predicate "is this grammar reduced ?"
        """
        return len(self.productive.vars) == len(self.byVar) and len(self.accessible) == len(self.byVar)

    def is_var(self, name) -> bool:
        """
            name : str
            predicate " does name represent a variable symbol ? "
        """
        return name in self.byVar.keys()

    @property
    def first(self) -> Mapping[Symbol | Rule, set[Symbol]]:
        """
            "First" sets (dict of sets, indexed by variables and rules)
            e.g.
                prem[myvar] : set of terminal symbols Prem(myvar)
                prem[somerule] : Prem (right part of the rule)
        """
        if self.__first is None :
            self.__compute_first()
        return self.__first

    @property
    def follow(self) -> Mapping[Symbol, set[Symbol]]:
        """
            "Follow" sets (dict of sets, indexed by variables)
            e.g.
                suiv[myvar] : set of terminal symbols Suiv(myvar)
        """
        if self.__follow is None :
            self.__compute_follow()
        return self.__follow

    @property
    def suiv(self) -> Mapping[Symbol, set[Symbol]]:
        return self.follow

    @property
    def prem(self) -> Mapping[Symbol | Rule, set[Symbol]]:
        return self.first

    def __compute_eps_prod(self) -> Closure:
        return self.__compute_closure(
            (lambda r: not r.right ),
            (lambda r, found: all( x in found for x in r.right) )
        )

    def __compute_prod(self) -> Closure:
        return self.__compute_closure(
            (lambda r: all(not self.is_var(x) for x in r.right)),
            (lambda r, found: all(not self.is_var(x) or x in found for x in r.right))
        )

    def __compute_closure(self,
                          select_init: Callable[[Rule],bool],
                          select_step: Callable[[Rule,Set[Symbol]],bool]
                          ) -> Closure:
        """
            returns (variables set, rules set)
            select_init : function(Rule):bool   select initial rules
            select_step : function(Rule, found vars set):bool  select new Rules
        """
        rules = set(self.rules)
        result = Closure(set(), set())
        rules_selection = {r for r in rules if select_init(r)}
        new = {v for v, w in rules_selection}
        rules -= rules_selection
        while new:
            result.vars.update(new)
            result.rules.update(rules_selection)
            rules_selection = {r for r in rules if select_step(r, result.vars)}
            new = {v for v, w in rules_selection if v not in result.rules}
            rules -= rules_selection
        result.rules.update(rules_selection)
        return result

    def __compute_accessible(self) -> set[Symbol]:
        result = {self.axiom}
        todo = {self.axiom}
        while todo:
            v = todo.pop()
            for r in self.byVar[v]:
                for x in r.right:
                    if self.is_var(x) and x not in result:
                        result.add(x)
                        todo.add(x)
        return result

    def reduce(self) :
        """
            reduce this grammar  (/!\\ modifies current grammar)
        """
        if not self.is_reduced() :
            productive_vars, productive_rules = self.productive
            unproductive_vars = self.byVar.keys() - productive_vars

            if unproductive_vars :
                for var in self.byVar.keys() :
                    # self.byVar[var] &=  productive_rules
                    self.byVar[var] = OrderedSet[Rule](self.byVar[var] & productive_rules)
                            #(dict((r,None) for r in self.byVar[var] if r in productive_rules)
                for v in unproductive_vars :
                    self.byVar.pop(v)
                if self.axiom not in self.byVar :
                    raise Exception('unproductive grammar')

            inaccessibles = self.byVar.keys() - self.__compute_accessible()
            for v in inaccessibles :
                self.byVar.pop(v)

            # update properties :
            self.__eps_prod =  self.__compute_eps_prod()    # epsilon-productive vars and rules (type Property)
            self.__productive = self.__compute_prod()  # productive vars and rules (type Property)
            self.__accessible = self.__compute_accessible()  # set of variables

    @staticmethod
    def __lfp(
            sets: MutableMapping[Symbol|Rule,MutableSet[Symbol]],
            supersets: Mapping[Symbol|Rule,Set[Symbol|Rule]]
        ):
        """ complete sets using least fixed point algo (lfp)
            /!\\ side effect : sets will be modified
        """
        modified = defaultdict[Symbol|Rule, MutableSet[Symbol]](set)
        modified |= {v:content for v, content in sets.items() if content}
        while modified:
            v, new_values = modified.popitem()
            for sup_set_key in supersets[v]:
                to_add = new_values - sets[sup_set_key]
                if to_add :
                    sets[sup_set_key] |= to_add
                    modified[sup_set_key] |= to_add

    def __compute_first(self):
        """
            compute "First" sets
        """
        # ensembles premiers (pour les variables);
        #   clé : variable valeur : symbole
        prem: dict[Symbol|Rule,set[Symbol]] = {var: set().copy() for var in self.get_vars()}
        # relation d'inclusion entre ensembles premiers (pour les variables);
        #   clé : variable,  valeur : variable ou règle
        supersets: dict[Symbol|Rule,set[Symbol|Rule]]  = {var: set().copy() for var in self.get_vars()}

        for r in self.rules:
            prem[r] = set()
            supersets[r] = set()
            for symbol in r.right:  # /!\ break when prefix is no more eps-prod
                if self.is_var(symbol):  # symbol est une variable
                    supersets[symbol].add(r.left)
                    supersets[symbol].add(r)
                    if symbol not in self.eps_prod.vars:
                        break
                else:
                    prem[r.left].add(symbol)
                    prem[r].add(symbol)
                    break
        prem = dict(prem)
        supersets = dict(supersets)
        self.__lfp(prem, supersets)
        self.__first = prem

    def __compute_follow(self):
        """
            computes "Follow" sets
        """
        suiv = {var: set().copy() for var in self.get_vars()}
        supersets = {var: set().copy() for var in self.get_vars()}
        suiv[self.axiom] = {EOD}
        for r in self.rules:  # compute suiv base content and  suiv supersets
            suffix_eff = True
            e = set()  # cumul d'ensembles prem
            for x in r.right[::-1]:  # visit in reverse order
                if self.is_var(x):  # x est une variable
                    suiv[x].update(e)
                    if suffix_eff:
                        supersets[r.left].add(x)
                    if x in self.eps_prod.vars:
                        e.update(self.prem[x])
                    else:
                        e = self.prem[x].copy()
                        suffix_eff = False
                else:  # x est une lettre terminale
                    e = {x}
                    suffix_eff = False

        self.__lfp(suiv, supersets)  # plus petit point fixe
        self.__follow = suiv


