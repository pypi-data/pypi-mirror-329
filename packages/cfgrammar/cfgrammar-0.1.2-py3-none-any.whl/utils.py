from typing import TypeVar, Generic, AbstractSet
from collections.abc import Iterator, Iterable, MutableSet, Set

T = TypeVar('T')
class OrderedSet(MutableSet,Generic[T]):
    """
        Set iterable by  insertion order
    """
    def __init__(self, iterable: Iterable[T] = tuple[T]()):
        self.__elements = dict[T,None]()
        self.update(iterable)

    def __iter__(self) -> Iterator[T]:
        return iter(self.__elements)

    def __contains__(self, value) ->bool:
        return value in self.__elements

    def __len__(self) -> int:
        return len(self.__elements)

    def __repr__(self) ->str:
        return f"{{{','.join(map(str, self.__elements))}}}"

    def add(self,value:T):
        self.__elements[value]=None

    def discard(self, value: T):
        self.__elements.pop(value, None)

    def remove(self, value: T):
        self.__elements.pop(value)

    def update(self, others: AbstractSet[T]):
        return self.__ior__(others)

    def intersection_update(self, others: AbstractSet[T]):
        return self.__iand__(others)

    def difference_update(self, others: AbstractSet[T]):
        return self.__isub__(others)

    def symetric_difference_update(self, others: AbstractSet[T]):
        return self.__ixor__(others)

    def union(self, others:AbstractSet[T]):
        return self.__or__(others)

    def intersection(self, others:AbstractSet[T]):
        return self.__and__(others)

    def difference(self, others:AbstractSet[T]):
        return self.__sub__(others)

    def symetric_difference(self, others:AbstractSet[T]):
        return self.__xor__(others)

    def issuperset(self, others: AbstractSet[T]):
        return self.__ge__(others)

    def issubset(self, others:AbstractSet[T]):
        return self.__le__(others)


