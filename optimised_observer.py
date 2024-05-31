from dataclasses import dataclass, field
from time import perf_counter

def time(method: callable) -> int:
    start: float = perf_counter()
    method()
    end: float = perf_counter()
    print("Operation finished")
    return round((end - start) * 1000) # converts to milliseconds, round to nearest integer

@dataclass
class Subject:
    data: int = 0
    observers: list = field(default_factory=list)

    # I had to take out the Observer type hints in the Subject class to prevent 
    # errors caused by circular dependencies and/or not fully initialised classes

    def add_view(self, obs) -> None:
        self.observers.append(obs)
        obs.set_subject(self)

    def notify_views(self) -> None:
        for obs in self.observers:
            obs.update()

    def set_data(self, x: int) -> None:
        self.data = x
        self.notify_views()

    def get_data(self) -> int:
        return self.data

@dataclass
class Observer:
    id: int = 0
    subject: Subject = field(default_factory=Subject)
    view_state: int = -1

    def set_subject(self, s: Subject) -> None:
        self.subject = s
    
    def update(self) -> None:
        self.view_state = self.subject.get_data()
        print(self.view_state)

@dataclass
class ObserverTest:
    n_views: int = 100
    q: Subject = field(default_factory=Subject)
    all_views: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.fill()
        self.all_views = self.q.observers

    def fill(self) -> None:
        for i in range(self.n_views):
            ox: Observer = Observer(i)
            self.q.add_view(ox)
    
    def test(self) -> None:
        for i, ox in enumerate(self.all_views):
            self.q.data = i
            # The Observer ox is already being retrieved by the for-loop itself
            # using the enumerate function, which simultaneously returns both a
            # list item and its index in that list
            ox.update()

    def reset(self) -> None:
        self.q = field(default_factory=Subject)
        self.all_views = field(default_factory=list)
        self.__post_init__()

def main() -> None:
    test1 = ObserverTest(8000)
    print(f"Time taken to perform test with {test1.n_views} observers for 1 subject: {time(test1.test)}ms")

if __name__=="__main__":
    main()
