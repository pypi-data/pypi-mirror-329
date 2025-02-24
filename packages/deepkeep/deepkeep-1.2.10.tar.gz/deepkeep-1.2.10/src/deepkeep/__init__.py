from __future__ import annotations
from ._client import Client, Deepkeep

__all__ = [
    "Client",
    "Deepkeep"
]


# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# deepkeep._exceptions.NotFoundError -> deepkeep.NotFoundError
__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "deepkeep"
        except (TypeError, AttributeError):
            # Some of our exported symbols are builtins which we can't set attributes for.
            pass
