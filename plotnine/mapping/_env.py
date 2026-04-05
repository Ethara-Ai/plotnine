from __future__ import annotations

from collections.abc import MutableMapping
from contextlib import suppress
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Hashable, Protocol, Self

    from patsy.eval import EvalEnvironment

    class SupportsGetItem(Protocol):
        """
        Supports __getitem__
        """

        def __getitem__(self, key: str, /) -> Any: ...

        def __iter__(self) -> Iterator[Hashable]: ...


__all__ = ("Environment",)


@dataclass
class Environment:
    """
    A Python execution environment.

    Encapsulates a namespace for variable lookup
    """

    namespaces: list[SupportsGetItem]

    def __post_init__(self):
        self.namespace = StackedLookup(self.namespaces)
        """Where to look up variables from the encapsulated environment"""

    def with_outer_namespace(self, outer_namespace):
        """
        Return a new Environment with an extra namespace added.

        This namespace will be used only for variables that are not found
        in any existing namespace, i.e., it is "outside" them all.
        """
        pass

    def eval(self, expr: str, inner_namespace: SupportsGetItem = {}):
        """
        Evaluate some Python code in the encapsulated environment.

        Parameters
        ----------

        expr :
            A string containing a Python expression.

        inner_namespace :
            A dict-like object that will be checked first when `expr` attempts
            to access any variables.

        Returns
        -------
        :
            The value of `expr`.
        """
        pass

    @classmethod
    def capture(cls, eval_env: int | Self = 0):
        """
        Capture an execution environment from the stack.

        Parameters
        ----------
        eval_env :
            If `eval_env` is already an `Environment`, it is
            returned unchanged.

            Otherwise, we walk up the stack by `eval_env` steps and capture
            that function's evaluation environment.

        """
        pass

    def to_patsy_env(self) -> EvalEnvironment:
        """
        Convert a plotnine environment to a patsy environment
        """
        pass

    def _namespace_ids(self):
        pass

    def __eq__(self, other):
        return (
            isinstance(other, Environment)
            and self._namespace_ids() == other._namespace_ids()
        )

    def __hash__(self):
        return hash((Environment, tuple(self._namespace_ids())))

    def __getstate__(self):
        """
        Return state with no namespaces
        """
        return {"namespaces": [], "namespace": StackedLookup([])}

    def __deepcopy__(self, memo: dict[Any, Any]) -> Environment:
        """
        Shallow copy
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        for key, item in old.items():
            new[key] = item
            memo[id(new[key])] = new[key]

        return result


@dataclass
class StackedLookup(MutableMapping):
    """
    Iterative lookup in a stack of dicts

    Assignments go into an internal dict that is also the first place
    where a lookup is done.
    """

    stack: list[SupportsGetItem]

    def __post_init__(self):
        self._dict = {}
        self.stack = [self._dict] + list(self.stack)

    def __getitem__(self, key):
        for d in self.stack:
            with suppress(KeyError):
                return d[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __contains__(self, key):
        with suppress(KeyError):
            self[key]
            return True
        return False

    def __iter__(self):
        """
        Unique keys in stacking order
        """
        return iter({key: None for d in self.stack for key in d})

    def __len__(self):
        """
        Number of unique keys
        """
        return len({key for d in self.stack for key in d})

    def get(self, key: str, default: Any = None) -> Any:
        with suppress(KeyError):
            return self[key]
        return default

    def __repr__(self):
        return f"{self.__class__.__name__}({self.stack})"

    def __getstate__(self):
        """
        Return state with no namespace
        """
        d = {}
        return {"stack": [d], "_dict": d}

    def copy(self):
        pass

    def __deepcopy__(self, memo: dict[Any, Any]) -> StackedLookup:
        """
        Shallow copy
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        old = self.__dict__
        new = result.__dict__

        for key, item in old.items():
            new[key] = item
            memo[id(new[key])] = new[key]

        return result


@lru_cache(maxsize=256)
def _compile_eval(source):
    """
    Cached compile in eval mode
    """
    pass
