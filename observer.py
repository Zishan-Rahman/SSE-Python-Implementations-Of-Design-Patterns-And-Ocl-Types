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
    
    def set_data_without_notifying_views(self, x: int) -> None:
        self.data = x

    def set_data_and_notify_views(self, x: int) -> None:
        self.set_data_without_notifying_views(x)
        self.notify_views()

    def set_data(self, x: int) -> None:
        self.set_data_and_notify_views(x)

    def get_data(self) -> int:
        return self.data
    
    def clear(self) -> None:
        self.observers.clear()
        self.data = 0

@dataclass
class Observer:
    id: int = 0
    subject: Subject = field(default_factory=Subject)
    view_state: int = -1

    def get_subject(self) -> Subject:
        return self.subject

    def set_subject(self, s: Subject) -> None:
        self.subject = s
    
    def set_subject_and_get_observer(self, s: Subject) -> any:
        self.set_subject(s)
        return self

    def update(self) -> None:
        self.view_state = self.subject.get_data()
        print(self.view_state)

@dataclass
class ObserverTest:
    n_views: int = 100
    q: Subject = field(default_factory=Subject)
    all_views: list[Observer] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.fill()

    def fill(self) -> None:
        self.q.observers = list(map(lambda x: x.set_subject_and_get_observer(self.q), [Observer(i) for i in range(self.n_views)]))
        self.all_views = self.q.observers
    
    def test(self) -> None:
        for i, ox in enumerate(self.all_views):
            self.q.set_data_without_notifying_views(i)
            ox.update()

    def __clear_subject_views(self) -> None:
        self.q.clear()
        self.all_views.clear()

    def reset(self) -> None:
        self.__clear_subject_views()
        self.fill()

def main() -> None:
    test1 = ObserverTest()
    print(f"Time taken to perform test with {test1.n_views} observers for 1 subject: {time(test1.test)}ms")
    test1.fill()
    print(f"Time taken to perform test with {test1.n_views} observers for 1 subject: {time(test1.test)}ms")
    test1.reset()
    print(f"Time taken to perform test with {test1.n_views} observers for 1 subject: {time(test1.test)}ms")

if __name__=="__main__":
    main()
