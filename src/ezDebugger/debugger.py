from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import functools
import inspect

"""
Logger is a dataclass-based decorator that provides debug tracing for functions.
It logs when a function is called, including its parameters and locale information,
helping with debugging by showing the execution flow.
"""
@dataclass
class Logger:
    func:Callable = field(repr=False)
    active:Optional[bool] = True
    lvl:Optional[int] = 1
    """
    __post_init__ is called after the dataclass initialization.
    It sets up the wrapper for the function, retrieves the file where the function is defined,
    and initializes instance and owner attributes for descriptor behavior.
    """
    def __post_init__(self) -> None:
        functools.update_wrapper(self, self.func)
        self._file:     str = inspect.getfile(self.func)
        self._instance: Any = None
        self._owner:    Any = None

    """
    __get__ implements the descriptor protocol for instance method access.
    When accessed on an instance, it binds the instance and returns a partial function
    that will call __call__ with the instance as the first argument.
    If accessed on the class, it returns self.
    """
    def __get__(self, instance, owner) -> Any:
        if instance is None:
            self._owner = owner
            return self
        self._instance = instance
        self._owner    = owner
        return functools.partial(self.__call__, instance)

    """
    _debug_message is a property that generates the debug message string.
    It checks the debug level and whether the function is private (starts with _).
    It resolves the owning class by walking the call stack when __get__ is bypassed,
    such as when Logger is wrapped by @staticmethod. It constructs a message with
    the function name, class if applicable, and locale.
    Returns None if the function should not be logged.
    """
    @property
    def _debug_message(self) -> str | None:
        if self.lvl != None and self.lvl < 2 and self.func.__name__.startswith("_"):
            return None

        owner = self._owner
        if owner is None:
            frame = inspect.currentframe().f_back #type: ignore
            for cls in (v for v in frame.f_globals.values() if inspect.isclass(v)): #type: ignore
                for val in vars(cls).values():
                    inner = val.__func__ if isinstance(val, staticmethod) else val
                    if inner is self:
                        owner = cls
                        break
                if owner:
                    break

        if owner:
            locale = inspect.getfile(owner).replace("\\", "/").split("/")[-1]
            return (
                F"\nDEBUG: Function Running: {owner.__name__}.{self.func.__name__}()"
                F"\n| LOCALE -> {locale}"
            )

        locale = self._file.replace("\\", "/").split("/")[-1]
        return (
            F"\nDEBUG: Function Running: {self.func.__name__}()"
            F"\n| LOCALE -> {locale}"
        )

    """
    __call__ is invoked when the decorated function is called.
    It prints the debug message if active, filters out the instance from args for display,
    and then calls the original function with the provided arguments.
    """
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.active and (message := self._debug_message):
            params = tuple(a for a in args if a is not self._instance)
            debug = F"{message}\n| PARAMS -> {params}" if params else message
            debug += "\n↓\n"
            print(debug)

        return self.func(*args, **kwargs)
    
    def _set_log_type(self, l_type) -> None:
        pass
    
"""
The following block runs when the script is executed directly (not imported).
It demonstrates the Logger decorator by applying it to a simple function
and printing the string representation of Logger as well as any returns from
target function.
"""
if __name__ == "__main__":
    class Operations:
        @staticmethod
        @Logger
        def add(*args) -> int:
            return sum(args)
    print(Operations.add(1, 2, 3))