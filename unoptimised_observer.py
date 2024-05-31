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
    
    def clear(self) -> None:
        self.observers.clear()
        self.data = 0

@dataclass
class Observer:
    id: int = 0
    subject: Subject = field(default_factory=Subject)
    view_state: int = -1

    def set_subject(self, s: Subject) -> None:
        self.subject = s
    
    def update(self) -> None:
        self.view_state = self.subject.get_data()
        if self.view_state % 100 == 0:
            print(self.view_state)

@dataclass
class ObserverTest:
    n_views: int = 100
    q: Subject = field(default_factory=Subject)

    def __post_init__(self):
        self.fill()

    def fill(self):
        for i in range(self.n_views):
            self.q.add_view(Observer(i))
    
    def test(self):
        for i in range(self.n_views):
            self.q.set_data(i)

    def reset(self):
        self.q.clear()
        self.fill()

def main() -> None:
    test1 = ObserverTest(8000)
    print(f"Time taken to perform test with {test1.n_views} observers for 1 subject: {time(test1.test)}ms")

if __name__=="__main__":
    main()
