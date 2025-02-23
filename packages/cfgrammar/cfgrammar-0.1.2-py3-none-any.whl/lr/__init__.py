from ..common import LRMethod
from ..common import ConflictError
from .automaton import LR0Automaton as AutImpl
from .tables import LRTable


class LR0Automaton(AutImpl):
    def table(self, method: LRMethod|str = LRMethod.LR0, raise_exception: bool = True): # -> LRTable:
        """
            Builds and returns LRTable (either LR0, SLR1 or LALR1)
        """
        return LRTable(self, method, raise_exception)

    def isLR(self, method: LRMethod|str) -> bool:
        try:
            self.table(method, raise_exception=True)
            return True
        except ConflictError:
            return False

    def isLR0(self) -> bool:
        return self.isLR(LRMethod.LR0)

    def isSLR1(self) -> bool:
        return self.isLR(LRMethod.SLR1)

    def isLALR1(self) -> bool:
        return self.isLR(LRMethod.LALR1)
