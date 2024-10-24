import __static__

import copy
import itertools
import operator
from functools import wraps
from typing import Dict, Generic, NoReturn, Optional, Callable, Tuple, List, TypeVar, Union, Any

W = TypeVar("W")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Self_cached_property = TypeVar("Self", bound="cached_property")
Self_classproperty = TypeVar("Self", bound="classproperty")
Self_LazyObject = TypeVar("Self", bound="LazyObject")

### SECTION SEPARATOR ###

class cached_property(Generic[W]):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    A cached property can be made out of an existing method:
    (e.g. ``url = cached_property(get_absolute_url)``).
    """

    name: Optional[str] = None

    @staticmethod
    def func(instance: object) -> Union[W, NoReturn]:
        raise TypeError(
            "Cannot use cached_property instance without calling "
            "__set_name__() on it."
        )

    ## why does noReturn not work here?
    def __init__(self: Self_cached_property, func: Callable[..., W]) -> None:
        self.real_func: Callable[..., W] = func
        self.__doc__: str = getattr(func, "__doc__")

    ### SECTION SEPARATOR ###

    # conflicts with typing NoReturns and None
    # see: https://github.com/python/typing/issues/695#issue-539279471
    # block could raise an error (never passes back control) or implicitly return None
    # Optional[NoReturn] should work but raises an error saying no explicit return
    # None is misleading
    def __set_name__(self: Self_cached_property, owner: NoReturn, name: Optional[str]) -> None:
        if self.name is None:
            self.name = name
            setattr(self, "func", self.real_func)
            # self.func = self.real_func ## mypy does not like this. 
            # callable not smart enough for bound and unbound funcs
            # see: https://github.com/python/mypy/issues/2427#issuecomment-259677994

        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )
    
    ### SECTION SEPARATOR ###

    def __get__(self: Self_cached_property, instance: object, cls: Optional[NoReturn] = None) -> Union[Self_cached_property, W]:
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self

        res: W = self.func(instance)
        instance.__dict__[self.name] = res #type: ignore
        # how do i convince mypy that name exists?
        # if statements not working. occurrence bug?
        return res

### SECTION SEPARATOR ###

class classproperty(Generic[W]):
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self: Self_classproperty, method: Optional[Callable[..., W]] = None) -> None:
        if method:
            self.fget: Callable[..., W] = method

    ### SECTION SEPARATOR ###

    def __get__(self: Self_classproperty, instance: NoReturn, cls: Optional[object] = None) -> W:
        return self.fget(cls)

    ### SECTION SEPARATOR ###

    def getter(self: Self_classproperty, method: Callable[..., W]) -> Self_classproperty:
        self.fget = method
        return self

### SECTION SEPARATOR ###

class Promise:
    """
    Base class for the proxy class created in the closure of the lazy function.
    It's used to recognize promises in code.
    """

    pass

# dibri:
# Callable[[Tuple[W, ...], Dict[str, X]], Y]
# proxy not defined yet
# how to describe an object with secific props
ResultClasses = Tuple[W, ...]

def lazy(func: Callable[..., Any], *resultclasses: object) -> Any:
    """
    Turn any callable into a lazy evaluated callable. result classes or types
    is required -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """
    Self_lazy = TypeVar("Self", bound="__proxy__")

    class __proxy__(Promise, Generic[X]):
        """
        Encapsulate a function call and act as a proxy for methods that are
        called on the result of that function. The function is not evaluated
        until one of the methods on the result is called.
        """

        def __init__(self: Self_lazy, args: Tuple[W, ...], kw: Dict[str, X]) -> None:
            self._args = args
            self._kw = kw
            
        ### SECTION SEPARATOR ###

        def __reduce__(self: Self_lazy) -> Tuple[Callable[..., Any], Tuple[Any, ...]]:
            return (
                _lazy_proxy_unpickle,
                (func, self._args, self._kw) + resultclasses,
            )

        def __deepcopy__(self: Self_lazy, memo: Dict[int, Self_lazy]) -> Self_lazy:
            # Instances of this class are effectively immutable. It's just a
            # collection of functions. So we don't need to do anything
            # complicated for copying.
            memo[id(self)] = self
            return sel

        def __cast(self: Self_lazy) -> Self_lazy:
            return func(*self._args, **self._kw)

        # Explicitly wrap methods which are defined on object and hence would
        # not have been overloaded by the loop over resultclasses below.

        def __repr__(self: Self_lazy) -> str:
            return repr(self.__cast())

        def __str__(self: Self_lazy) -> str:
            return str(self.__cast())

        def __eq__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() == other

        def __ne__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() != other

        def __lt__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() < other

        def __le__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() <= other

        def __gt__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() > other

        def __ge__(self: Self_lazy, other: object) -> bool:
            if isinstance(other, Promise):
                other = other.__cast() #type: ignore
            return self.__cast() >= other

        def __hash__(self: Self_lazy) -> int:
            return hash(self.__cast())

        def __format__(self: Self_lazy, format_spec: str) -> str:
            return format(self.__cast(), format_spec)

        # Explicitly wrap methods which are required for certain operations on
        # int/str objects to function correctly.

        # dibri: redefined. see: 166
        def __ge__(self: Self_lazy, other: Promise) -> Any:
            return self.__cast() + other

        def __radd__(self: Self_lazy, other: Promise) -> Any:
            return other + self.__cast()

        def __mod__(self: Self_lazy, other: Promise) -> Any:
            return self.__cast() % other

        def __mul__(self: Self_lazy, other: Promise) -> Any:
            return self.__cast() * other

    # Add wrappers for all methods from resultclasses which haven't been
    # wrapped explicitly above.
    for resultclass in resultclasses:
        for type_ in resultclass.mro(): #type: ignore
            for method_name in type_.__dict__:
                # All __promise__ return the same wrapper method, they look up
                # the correct implementation when called.
                if hasattr(__proxy__, method_name):
                    continue

                # Builds a wrapper around some method. Pass method_name to
                # avoid issues due to late binding.
                def __wrapper__(self, *args, __method_name = method_name, **kw) -> __proxy__:
                    # Automatically triggers the evaluation of a lazy value and
                    # applies the given method of the result type.
                    result = func(*self._args, **self._kw)
                    return getattr(result, __method_name)(*args, **kw)

                setattr(__proxy__, method_name, __wrapper__)
    
    ### SECTION SEPARATOR ###

    # dibri: issue distinguishing this from wrapper defined earlier?
    @wraps(func) # type: ignore
    def __wrapper__(*args: Tuple[W, ...], **kw: Dict[str, X]) -> __proxy__:
        # Creates the proxy object, instead of the actual value.
        return __proxy__(args, kw)

    return __wrapper__

### SECTION SEPARATOR ###

def _lazy_proxy_unpickle(func: Callable[..., W], args: Tuple[X, ...], kwargs: Dict[str, Y], *resultclasses: Z) -> Z:
    return lazy(func, *resultclasses)(*args, **kwargs)

### SECTION SEPARATOR ###

# dibri: or text: Callable[[], str]
def lazystr(text: str) -> str:
    """
    Shortcut for the common case of a lazy callable that returns str.
    """
    return lazy(str, str)(text)

### SECTION SEPARATOR ###

# dibri: how do you type functions that may not return?
def keep_lazy(*resultclasses: W) -> Union[NoReturn,  Callable[[Callable[..., X]], Callable[..., X]]]:
    """
    A decorator that allows a function to be called with one or more lazy
    arguments. If none of the args are lazy, the function is evaluated
    immediately, otherwise a __proxy__ is returned that will evaluate the
    function when needed.
    """
    if not resultclasses:
        raise TypeError("You must pass at least one argument to keep_lazy().")

    def decorator(func: Callable[..., X]) -> Callable[..., X]:
        lazy_func = lazy(func, *resultclasses)

        @wraps(func)
        def wrapper(*args: Tuple[Y, ...], **kwargs: Dict[str, Z]):
            if any(
                isinstance(arg, Promise)
                for arg in itertools.chain(args, kwargs.values())
            ):
                return lazy_func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator

### SECTION SEPARATOR ###

def keep_lazy_text(func: Callable[..., str]) -> Union[NoReturn,  Callable[..., str]]:
    """
    A decorator for functions that accept lazy arguments and return text.
    """
    return keep_lazy(str)(func)

### SECTION SEPARATOR ###

empty = object()

def new_method_proxy(func: Callable[..., "LazyObject"]) -> Callable[["LazyObject", Tuple[X, ...]], "LazyObject"]:
    def inner(self: "LazyObject", *args: Tuple[X, ...]) -> "LazyObject":
        if (_wrapped := self._wrapped) is empty:
            self._setup()
            _wrapped = self._wrapped
        return func(_wrapped, *args)

    inner._mask_wrapped = False #type: ignore
    return inner

### SECTION SEPARATOR ###

class LazyObject(Generic[X]):
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.
    By subclassing, you have the opportunity to intercept and alter the
    instantiation. If you don't need to do that, use SimpleLazyObject.
    """

    # Avoid infinite recursion when tracing __init__ (#19456).
    _wrapped = None

    def __init__(self: Self_LazyObject) -> None:
        # Note: if a subclass overrides __init__(), it will likely need to
        # override __copy__() and __deepcopy__() as well.
        self._wrapped = empty
    
    ### SECTION SEPARATOR ###

    def __getattribute__(self: Self_LazyObject, name: str) -> Union[NoReturn, X]:
        if name == "_wrapped":
            # Avoid recursion when getting wrapped object.
            return super().__getattribute__(name)
        value: X = super().__getattribute__(name)
        # If attribute is a proxy method, raise an AttributeError to call
        # __getattr__() and use the wrapped object method.
        if not getattr(value, "_mask_wrapped", True):
            raise AttributeError
        return value

    ### SECTION SEPARATOR ###

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self: Self_LazyObject, name: str, value: W) -> None:
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)
    
    ### SECTION SEPARATOR ###

    def __delattr__(self: Self_LazyObject, name: str) -> None:
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)
    
    ### SECTION SEPARATOR ###

    def _setup(self: Self_LazyObject) -> NoReturn:
        """
        Must be implemented by subclasses to initialize the wrapped object.
        """
        raise NotImplementedError(
            "subclasses of LazyObject must provide a _setup() method"
        )
        
    ### SECTION SEPARATOR ###

    # Because we have messed with __class__ below, we confuse pickle as to what
    # class we are pickling. We're going to have to initialize the wrapped
    # object to successfully pickle it, so we might as well just pickle the
    # wrapped object since they're supposed to act the same way.
    #
    # Unfortunately, if we try to simply act like the wrapped object, the ruse
    # will break down when pickle gets our id(). Thus we end up with pickle
    # thinking, in effect, that we are a distinct object from the wrapped
    # object, but with the same __dict__. This can cause problems (see #25389).
    #
    # So instead, we define our own __reduce__ method and custom unpickler. We
    # pickle the wrapped object as the unpickler's argument, so that pickle
    # will pickle it normally, and then the unpickler simply returns its
    # argument.
    def __reduce__(self: Self_LazyObject) -> Tuple[Callable[["LazyObject"], "LazyObject"], Tuple[Any]]:
        if self._wrapped is empty:
            self._setup()
        return (unpickle_lazyobject, (self._wrapped,))
    
    ### SECTION SEPARATOR ###

    def __copy__(self: Self_LazyObject) -> Union[object, "LazyObject"]:
        if self._wrapped is empty:
            # If uninitialized, copy the wrapper. Use type(self), not
            # self.__class__, because the latter is proxied.
            return type(self)()
        else:
            # If initialized, return a copy of the wrapped object.
            return copy.copy(self._wrapped)
        
    ### SECTION SEPARATOR ###

    def __deepcopy__(self: Self_LazyObject, memo: Dict[int, "LazyObject"]) -> Union[object, "LazyObject"]:
        if self._wrapped is empty:
            # We have to use type(self), not self.__class__, because the
            # latter is proxied.
            result = type(self)()
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)
    
    ### SECTION SEPARATOR ###

    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Need to pretend to be the wrapped class, for the sake of objects that
    # care about this (especially in equality tests)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)

    # List/Tuple/Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)

### SECTION SEPARATOR ###

# dibri: why?
def unpickle_lazyobject(wrapped: W) -> W:
    """
    Used to unpickle lazy objects. Just return its argument, which will be the
    wrapped object.
    """
    return wrapped

### SECTION SEPARATOR ###

class SimpleLazyObject(LazyObject):
    """
    A lazy object initialized from any function.
    Designed for compound objects of unknown type. For builtins or objects of
    known type, use django.utils.functional.lazy.
    """

    def __init__(self: Self_LazyObject, func: Callable[..., W]) -> None:
        """
        Pass in a callable that returns the object to be wrapped.
        If copies are made of the resulting SimpleLazyObject, which can happen
        in various circumstances within Django, then you must ensure that the
        callable can be safely run more than once and will return the same
        value.
        """
        self.__dict__["_setupfunc"] = func
        super().__init__()
    
    ### SECTION SEPARATOR ###

    def _setup(self: Self_LazyObject) -> None:
        self._wrapped = self._setupfunc()
    
    ### SECTION SEPARATOR ###

    # Return a meaningful representation of the lazy object for debugging
    # without evaluating the wrapped object.
    def __repr__(self: Self_LazyObject) -> str:
        if self._wrapped is empty:
            repr_attr = self._setupfunc
        else:
            repr_attr = self._wrapped
        return "<%s: %r>" % (type(self).__name__, repr_attr)
    
    ### SECTION SEPARATOR ###

    def __copy__(self: Self_LazyObject) -> Union[object, "SimpleLazyObject"]:
        if self._wrapped is empty:
            # If uninitialized, copy the wrapper. Use SimpleLazyObject, not
            # self.__class__, because the latter is proxied.
            return SimpleLazyObject(self._setupfunc)
        else:
            # If initialized, return a copy of the wrapped object.
            return copy.copy(self._wrapped)
        
    ### SECTION SEPARATOR ###

    def __deepcopy__(self, memo: Dict[int, "SimpleLazyObject"]) -> Union[object, "SimpleLazyObject"]:
        if self._wrapped is empty:
            # We have to use SimpleLazyObject, not self.__class__, because the
            # latter is proxied.
            result = SimpleLazyObject(self._setupfunc)
            memo[id(self)] = result
            return result
        return copy.deepcopy(self._wrapped, memo)
    
    ### SECTION SEPARATOR ###

    __add__ = new_method_proxy(operator.add)

    @new_method_proxy
    def __radd__(self: Self_LazyObject, other: "SimpleLazyObject") -> "SimpleLazyObject":
        return self + other
    
### SECTION SEPARATOR ###

def partition(predicate: Callable[[int], bool], values: List[int]) -> Tuple[List[int], List[int]]:
    """
    Split the values into two sets, based on the return value of the function
    (True/False). e.g.:
        >>> partition(lambda x: x > 3, range(5))
        [0, 1, 2, 3], [4]
    """
    results: Tuple[List[int], List[int]] = ([], [])
    for item in values:
        results[predicate(item)].append(item)
    return results
