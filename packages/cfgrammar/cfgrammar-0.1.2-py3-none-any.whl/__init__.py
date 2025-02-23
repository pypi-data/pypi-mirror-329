from collections.abc import Iterable, MutableMapping, Set

from .builder import GrammarBuilder
from .grammar import GrammarBase
from .common import Symbol, LRMethod, Rule, ConflictError, LLMethod
from .lr import LR0Automaton, LRTable

from .ll1 import LL1Table

class Grammar(GrammarBase):

    def __init__(self,
                 terminals: Iterable[Symbol],
                 axiom: Symbol,
                 rules_by_var: MutableMapping[Symbol, Set[Rule]]
                 ):
        """
        :param terminals: terminal symbols
        :param axiom: axiom symbol
        :param rules_by_var: grammar rule sets, indexed by variables (left-hand side symbols)
        """
        self.__lr0: LR0Automaton | None = None
        self.__lr_tables = dict[LRMethod,LRTable|bool]() # None : waiting computation, False : grammar incompatible with method

        self._ll1_computed: bool = False
        self._ll1_table: LL1Table|None = None
        self.ll1_error = None

        super().__init__(terminals, axiom, rules_by_var)


    def lr0_automaton(self) -> LR0Automaton : #| None:
        """
            return LR(0) automaton (LR0Automaton)
        """
        if self.__lr0 is not None :
            return self.__lr0
        if not self.is_reduced() :
            raise Exception('grammar should be reduced first')
        try:
            self.__lr0 = LR0Automaton(self)
        finally:
            return self.__lr0

    def tableLR(self, method: LRMethod | str) -> LRTable|bool:
        """  LR table

        :param method: parsing method
        :return: LRTable or False if not compatible
        """
        method = LRMethod(method)
        if self.__lr_tables.get(method,None) is None:  # let's compute the table
            try:
                self.__lr_tables[method] = self.lr0_automaton().table(method,  raise_exception = True)
            except ConflictError:
                self.__lr_tables[method] = False

        return self.__lr_tables[method]

    def isLR(self, method: LRMethod | str) -> bool:
        """Predicate : is grammar compatible with method ?

        :param method: parsing methode
        :return: bool
        """
        return bool(self.tableLR(method))

    def tableLR0(self,raise_exception = False) -> LRTable :
        return self.lr0_automaton().table(LRMethod.LR0,raise_exception)

    def tableSLR1(self, raise_exception=False) -> LRTable:
        return self.lr0_automaton().table(LRMethod.SLR1, raise_exception)

    def tableLALR1(self, raise_exception=False) -> LRTable:
        return self.lr0_automaton().table(LRMethod.LALR1, raise_exception)

    def isLR0(self) -> bool :
        return self.isLR(LRMethod.LR0)

    def isSLR1(self) -> bool:
        return self.isLR(LRMethod.SLR1)

    def isLALR1(self) -> bool :
        return self.isLR(LRMethod.LALR1)

    def ll1_table(self, raise_exception: bool = True) -> LL1Table:
        """
            returns LL(1) table (LL1Table instance)
            or None if grammar is not LL(1)
        """
        if self._ll1_computed :
            return self._ll1_table
        # else try to compute LL(1) parser
        if not self.is_reduced() :
            raise Exception('grammar should be reduced first')
        try :
            self._ll1_table = LL1Table(self,raise_exception)
        except ConflictError as e :
            self.ll1_error = str(e)  # self._ll1_table remains None
        finally:
            self._ll1_computed = True
            return self._ll1_table

    def tableLL1(self, raise_exception: bool = True) -> LL1Table:
        """
            returns LL(1) table (LL1Table instance)
            or None if grammar is not LL(1)
        """
        return self.ll1_table(raise_exception)

    def isLL1(self) -> bool :
        """
            predicate : "is this grammar LL(1) ?"
        """
        return self.ll1_table() is not None

    def parser(self, method: LRMethod|LLMethod|str = LRMethod.LALR1):
        try:
            method = LRMethod(method)
        except ValueError:
            try:
                method = LLMethod(method)
            except ValueError:
                raise ValueError(f'{method} is not a correct method')
        if isinstance(method,LRMethod):
            return self.lr0_automaton().table(method).parser()
        else:
            return self.tableLL1().parser()



    @staticmethod
    def from_string(source : str) -> 'Grammar':
        return Grammar(* GrammarBuilder.from_string(source))

