from .common import Rule
from .common import Symbol
from .common import Word
from .grammar import GrammarBase
from itertools import *


class Buckets :
    def __init__(self,level:int, ranks, rules ):
        self._buckets = [[] for i in range(level)]
        self.ranks = ranks
        self._final = []
        for r in rules:
            self.add_rule(r)
    def substitutions(self,bv):
        i = 0
        while i  < len(self._buckets) -1 :
            if self._buckets[i]:
                r = self._buckets[i].pop()
                for rr in bv[r.right[0]]:
                    new_r = Rule(r.left, Word(*rr.right, *r.right[1:]))
                    self.add_rule(new_r)
            if not self._buckets[i] :
                i += 1
        return self._buckets[-1], self._final

    def add_rule(self,r):
        if len(r.right) == 0 or r.right[0] not in self.ranks:
            self._final.append(r)
        else :
            rank = self.ranks[r.right[0]]
            if rank >= len(self._buckets):
                self._final.append(r)
            else:
                self._buckets[rank].append(r)




class Unrec (GrammarBase) :
    @staticmethod
    def supp_direct(var, dr, not_dr, byVar):  # rules : on empty set. rules must have the same left part
            new_var = next( symbol for symbol in
                            (Symbol(var+suffix) for suffix in chain("'",(f'_{i}' for i in count(1))))
                            if symbol not in byVar
                        )
            #new_var = Symbol(var + '_1')
            var_rules = [Rule(var, Word(*r.right, new_var)) for r in not_dr]
            new_var_rules = [Rule(new_var, Word(*r.right[1:], new_var)) for r in dr] + [Rule(new_var, Word())]
            return (var_rules, new_var_rules)

    def __new__(cls, g : GrammarBase):
        ranks = {v: i for i, v in enumerate(g.byVar.keys())}
        byVar = dict()
        for i,(var,rules) in enumerate(g.byVar.items()) :
            direct, byVar[var] = Buckets(i+1, ranks, rules).substitutions(byVar)
            if direct :
                v_rules, n_rules = Unrec.supp_direct(var,direct, byVar[var], byVar)
                byVar[var] = v_rules
                byVar[n_rules[0].left] = n_rules
        # return super().__new__(cls,g.terminals, g.axiom, byVar )
        return GrammarBase(g.terminals, g.axiom, byVar)









