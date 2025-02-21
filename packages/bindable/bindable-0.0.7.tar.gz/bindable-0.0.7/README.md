# Bindable singleton objects similar to Angular Services

## Installation

`pip install bindable`

## Usage 1 - binding to properties

The singleton object is first initialized whenever it is bound to a property or when the first constructor is called.

```py
from typing import override
from bindable import Bindable

class MyBindable(Bindable):
    @override
    def constructor(self) -> None:
        self.value = 3

    def method(self) -> str:
        return "Success"

class MyUsingClass:
    @MyBindable.bind
    def my_binding(self) -> MyBindable: ... # This code is overridden. Just use ... or pass.

    def some_method(self):
        print(self.my_binding.value)
        print(self.my_binding.method())
```

## Usage 2 - Singleton

The singleton object is first initialized whenever the first constructor is called.

```py
from bindable import Bindable

class MyBindable(Bindable):
    @override
    def constructor(self) -> None:
        self.value = 3

    def method(self) -> str:
        return "Success"

def do_something() -> None:
    my_bindable = MyBindable()
    print(my_bindable.value)
    print(my_bindable.method())
    print(MyBindable().value) # always returns the same object.
    print(MyBindable().method()) # always returns the same object.
```