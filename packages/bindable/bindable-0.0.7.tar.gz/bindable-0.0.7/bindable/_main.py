from __future__ import annotations
from typing import Callable, Dict, Self, Type, TypeVar

T = TypeVar('T', bound='Bindable')

class BoundProperty[T]:
    def __init__(self, cls: Type[T], func: Callable[..., T], safe: bool = True) -> None:
        self.cls = cls
        self.func = func
        self.safe = safe

    def __get__(self, instance, owner) -> T:
        if self.safe:
            return self.cls()
        return Bindable._singletons.get(self.cls)

class Bindable:
    """
        Derived classes virtually become Singletons.
        You can create an instance of the class, but it will always return the same
        object. The object is initialized using the constructor() method.
        Never forget to call `super().constructor()` in the derived classes.
    """
    _singletons: Dict[Type[Bindable], Bindable] = {}

    def __new__(cls, *args, **kwargs) -> Self:
        """Prevents creation of separate instances of a Bindable class."""
        if Bindable._singletons.get(cls) is None:
            Bindable._singletons[cls] = super().__new__(cls)
        return Bindable._singletons[cls]

    def __init__(self, *args, **kwargs):
        """
            Calls the constructor and passes all arguments only the first
            time when the object is initialized.
        """
        if not hasattr(self, '_initialized'):
            self.constructor(*args, **kwargs)
            self._initialized = True

    def constructor(self) -> None:
        """
            Override this method to initialize your singleton.
        """
        print(f'Bindable Class {self.__class__.__name__} initializing.')

    @property
    def ready(self) -> bool:
        return hasattr(self, '_initialized') and self._initialized

    @classmethod
    def bind(cls: Type[T], func: Callable[..., T], safe: bool = True) -> BoundProperty[T]:
        """
            Transform the method into a property that returns the Bindable.


            ### Parameters
            `safe`: `default=True` The provider can be instatiated without any problems. One of the reasons you may want
            to have an unsafe binding is if you're (for whatever reason) copying values from one provider to the other.
            ### Usage
            ```
            class MyBinding(Binding): ...

            class MyClass:
                @MyBinding.bind
                def binding(self) -> MyBinding: ...

                def my_method(self):
                    assert self.binding = MyBinding(), 'magic does not work!'
            ```
        """
        return BoundProperty[T](cls, func, safe)
