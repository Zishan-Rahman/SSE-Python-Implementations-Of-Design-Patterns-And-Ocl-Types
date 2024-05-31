from sortedcontainers import SortedSet, SortedList
from operator import neg
from dataclasses import dataclass, field
from time import perf_counter, sleep

def time(method: callable) -> int:
    start: float = perf_counter()
    method()
    end: float = perf_counter()
    print("Operation finished")
    return round((end - start) * 1000) # converts to milliseconds, round to nearest integer

def rest(secs: float) -> None:
    print(f"Now resting for {secs} seconds")
    sleep(secs)

@dataclass
class SustainabilityTest: # for OCL sequences (lists)
    addcount: int = 100
    checkcount: int = addcount # Needed to prevent "NameError: name 'checkcount' is not defined"
    collection: list = field(default_factory=list)

    # Needed to make sure custom addcount also gets set to checkcount
    def __post_init__(self) -> None:
        self.__set_checkcount_to_addcount()

    def __set_checkcount_to_addcount(self) -> None:
        self.checkcount = self.addcount

    def set_new_addcount(self, new_addcount: int) -> None:
        self.addcount = new_addcount
        self.__set_checkcount_to_addcount()

    def fill(self) -> None:
        self.collection = list(range(self.addcount, 0, -1))

    def check(self) -> None:
        checks: list[bool] = [i in self.collection for i in range(self.checkcount, 0, -1)]

    def reset(self) -> None:
        self.collection.clear()

@dataclass
class SortedSetSustainabilityTest(SustainabilityTest):
    collection: SortedSet = field(default_factory=lambda: SortedSet(key=neg))

    def fill(self) -> None:
        self.collection = SortedSet(range(self.addcount, 0, -1))

@dataclass
class SortedListSustainabilityTest(SustainabilityTest):
    collection: SortedList = field(default_factory=lambda: SortedList(key=neg))

    def fill(self) -> None:
        self.collection = SortedList(range(self.addcount, 0, -1))

def main() -> None:
    number_of_items: int = 80000
    test1 = SustainabilityTest(number_of_items)
    test2 = SortedSetSustainabilityTest(number_of_items)
    test3 = SortedListSustainabilityTest(number_of_items)
    rest(5)
    print(f"Now filling sequence with {test1.addcount} items")
    print(f"Time taken to fill sequence with {test1.addcount} items: {time(test1.fill)}ms")
    rest(5)
    print(f"Now checking through sequence of {test1.checkcount} items")
    print(f"Time taken to check through sequence of {test1.checkcount} items: {time(test1.check)}ms")
    rest(5)
    print(f"Now filling sorted set with {test2.addcount} items")
    print(f"Time taken to fill sorted set with {test2.addcount} items: {time(test2.fill)}ms")
    rest(5)
    print(f"Now checking through sorted set of {test2.checkcount} items")
    print(f"Time taken to check through sorted set of {test2.checkcount} items: {time(test2.check)}ms")
    rest(5)
    print(f"Now filling sorted sequence with {test3.addcount} items")
    print(f"Time taken to fill sorted sequence with {test3.addcount} items: {time(test3.fill)}ms")
    rest(5)
    print(f"Now checking through sorted sequence of {test3.checkcount} items")
    print(f"Time taken to check through sorted sequence of {test3.checkcount} items: {time(test3.check)}ms")


if __name__=="__main__":
    main()
