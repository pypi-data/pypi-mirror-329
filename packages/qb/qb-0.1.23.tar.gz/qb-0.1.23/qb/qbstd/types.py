from dataclasses import dataclass
from warnings import warn


class Some[T]:
    def __init__(self, value: T):
        self.value = value

    def unwrap(self) -> T:
        return self.value


type maybe = Some | None
type either = Some | Exception


class collection():
    """A lazy evaluated collection, that behaves like a list, but immutable with some neat additional methods."""

    def __init__(self, *args):
        self.args = args

    def for_each(self, func):
        if len(self) == 0:
            return

        func(self[0])
        collection(*self[1:]).for_each(func)

    def map(self, func):
        if len(self) == 0:
            return self

        return collection(func(self[0]), *collection(*self[1:]).map(func))

    def filter(self, func):
        if len(self) == 0:
            return self

        if func(self[0]):
            return collection(self[0], *collection(*self[1:]).filter(func))
        else:
            return collection(*collection(*self[1:]).filter(func))
        
    def head(self):
        return self[0]
    
    def tail(self):
        return collection(*self[1:])

    @staticmethod
    def of(iterable):
        if hasattr(iterable, "__len__") and iterable.__len__() == float("inf"):
            warn("Passing an infinite range to collection.of will result in an infinite loop.")

        return collection(*iterable)

    def __iter__(self):
        return iter(self.args)

    def __getitem__(self, key):
        return self.args[key]

    def __len__(self):
        return len(self.args)

    def __repr__(self):
        return f"collection{self.args}"

    def __str__(self):
        return f"{self.args}"

    def __contains__(self, item):
        return item in self.args

    def __eq__(self, other):
        return self.args == other.args

    def __ne__(self, other):
        return self.args != other.args

    def __add__(self, other):
        return collection(*self.args, *other.args)


@dataclass()
class infinite_range:
    """Returns an object that can be used similar to a normal range object, but with no end."""

    start: int = 0
    step: int = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.start += self.step
        return self.start - self.step

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start else self.start
            stop = key.stop if key.stop else float("inf")
            step = key.step if key.step else self.step

            return [self.start + i * self.step for i in range(start, stop, step)]
        else:
            return self.start + key * self.step

    def __len__(self):
        return float("inf")

    def __repr__(self):
        return f"infinite_range(start={self.start}, step={self.step})"

    def __str__(self):
        return f"range({self.start}, inf)"

    def __contains__(self, item):
        return (item - self.start) % self.step == 0
