from __future__ import annotations
from abc import ABC
from typing import Callable, Dict, Self, Type, TypeVar, override

class Singleton(ABC):
    """
        Derived classes virtually become Singletons.
        You can create an instance of the class, but it will always return the same
        object. The object is initialized using the constructor() method.
        Never forget to call `super().constructor()` in the derived classes.
    """
    _singletons: Dict[Type[Singleton], Singleton] = {}

    @classmethod
    def _new_instance(cls) -> Self:
        return super().__new__(cls)

    @classmethod
    def _create_singleton(cls, *args, **kwargs) -> None:
        Singleton._singletons[cls] = cls._new_instance()

    @classmethod
    def _fetch_singleton(cls, *args, **kwargs) -> Self:
        return Singleton._singletons.get(cls)

    def __new__(cls, *args, **kwargs) -> Self:
        """Prevents creation of separate instances of a Singleton class."""
        if cls._fetch_singleton(*args, **kwargs) is None:
            cls._create_singleton(*args, **kwargs)
        return cls._fetch_singleton(*args, **kwargs)

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

class GlobalCollection[G](Singleton):
    """
        Global Collection support for a class.

        Derived classes can be instantiated, which automatically adds them
        to the singleton list. They are indexed by their key given through their constructor.
    """
    _singletons: Dict[Type[Singleton], Dict[G, Singleton]] = {}

    @classmethod
    def _create_singleton(cls, key: G = None, *args, **kwargs) -> Self:
        if GlobalCollection._singletons.get(cls) is None:
            GlobalCollection._singletons[cls] = {}
        GlobalCollection._singletons[cls][key] = cls._new_instance()

    @classmethod
    def _fetch_singleton(cls, key: G = None, *args, **kwargs) -> Self:
        return GlobalCollection._singletons.get(cls, {}).get(key)

    @override
    def __init__(self, key: G = None, *args, **kwargs):
        """
            Calls the constructor and passes all arguments only the first
            time when the object is initialized.
        """
        if not hasattr(self, '_initialized'):
            self.constructor(key, *args, **kwargs)
            self._initialized = True

    def constructor(self, key: G = None) -> None:
        """
            Override this method to initialize your singleton.
        """
        self.key = key
        print(f'Global Collection element {self.__class__.__name__}[{key}] initializing.')

    @classmethod
    def clear(cls) -> None:
        GlobalCollection._singletons.get(cls, {}).clear()

    @classmethod
    def count(cls) -> int:
        return len(GlobalCollection._singletons.get(cls, {}))

    def pop(self) -> Self:
        return GlobalCollection._singletons.get(self.__class__, {}).pop(self.key)


T = TypeVar('T', bound='Bindable')

class BoundProperty[T]:
    def __init__(self, cls: Type[T], func: Callable[..., T], safe: bool = True) -> None:
        self.cls = cls
        self.func = func
        self.safe = safe

    def __get__(self, instance, owner) -> T:
        if self.safe:
            return self.cls()
        return Singleton._singletons.get(self.cls)

class Bindable(Singleton):
    @classmethod
    def bind(cls: Type[T], func: Callable[..., T], safe: bool = True) -> BoundProperty[T]:
        """
            Transform the method into a property that returns the Bindable singleton.

            ### Parameters
            `safe`: `default=True` The provider can be instatiated without any problems. One of the reasons you may want
            to have an unsafe binding is if you're (for whatever reason) copying values from one provider to the other.
            ### Usage
            ```
            class MyBinding(Bindable): ...

            class MyClass:
                @MyBinding.bind
                def binding(self) -> MyBinding: ...

                def my_method(self):
                    assert self.binding = MyBinding(), 'magic does not work!'
            ```
        """
        return BoundProperty[T](cls, func, safe)