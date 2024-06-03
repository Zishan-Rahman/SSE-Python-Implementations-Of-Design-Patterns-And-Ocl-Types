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
    initial_addcount: int = addcount
    initial_checkcount: int = checkcount

    # Needed to make sure custom addcount also gets set to checkcount, and also to ensure that
    # initial_addcount and initial_checkcount are also set to custom addcount and checkcount
    def __post_init__(self) -> None:
        self.initial_addcount = self.addcount
        self.checkcount = self.addcount
        self.initial_checkcount = self.checkcount

    # def add_to_collection(self, item) -> None:
    #     self.collection.append(item)

    def fill(self) -> None:
        while self.addcount > 0:
            # self.add_to_collection(self.addcount)
            self.collection.append(self.addcount)
            self.addcount -= 1
        # self.addcount = self.__reset_addcount()

    def check(self) -> None:
        while self.checkcount > 0:
            check: bool = self.checkcount in self.collection
            self.checkcount -= 1
        # self.checkcount = self.__reset_checkcount()

    def reset(self) -> None:
        self.__reset_addcount()
        self.__reset_checkcount()
        self.__reset_collection()

    def __reset_addcount(self) -> None:
        self.addcount = self.initial_addcount

    def __reset_checkcount(self) -> None:
        self.checkcount = self.initial_checkcount

    def __reset_collection(self) -> None:
        self.collection.clear()

@dataclass
class SortedSetSustainabilityTest(SustainabilityTest):
    collection: SortedSet = field(default_factory=lambda: SortedSet(key=neg))

    # def add_to_collection(self, item) -> None:
    #     self.collection.add(item)

    def fill(self) -> None:
        while self.addcount > 0:
            # self.add_to_collection(self.addcount)
            self.collection.add(self.addcount)
            self.addcount -= 1
        # self.addcount = self.__reset_addcount()

# Inherited from SortedSetSustainabilityTest instead of SustainabilityTest 
# so its fill method can be inherited without rewriting the whole method 
# (self.collection.add(self.account) applies to both SortedSet and SortedList)
@dataclass
class SortedListSustainabilityTest(SortedSetSustainabilityTest):
    collection: SortedList = field(default_factory=lambda: SortedList(key=neg))

@dataclass
class SpeedySortedListSustainabilityTest(SortedListSustainabilityTest):
    def fill(self) -> None:
        proxy: list[int] = list()
        while self.addcount > 0:
            proxy.append(self.addcount)
            self.addcount -= 1
        self.collection = SortedList(proxy, key=neg)
        # self.addcount = self.__reset_addcount()
        

def main() -> None:
    number_of_items: int = 80000
    test1 = SustainabilityTest(number_of_items)
    test2 = SortedSetSustainabilityTest(number_of_items)
    test3 = SortedListSustainabilityTest(number_of_items)
    test4 = SpeedySortedListSustainabilityTest(number_of_items)
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
    rest(5)
    print(f"Now filling sorted sequence with {test4.addcount} items")
    print(f"Time taken to fill sorted sequence with {test4.addcount} items: {time(test4.fill)}ms")
    rest(5)
    print(f"Now checking through sorted sequence of {test4.checkcount} items")
    print(f"Time taken to check through sorted sequence of {test4.checkcount} items: {time(test4.check)}ms")

if __name__=="__main__":
    main()
