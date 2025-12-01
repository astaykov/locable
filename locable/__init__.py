"""
Package shim so the nested `locable/locable` code can be imported as `locable.*`.

We extend the package search path to include the inner folder so that imports
like `locable.agent` and `locable.rag` resolve correctly after the repo was
restructured.
"""

from pathlib import Path
import pkgutil

# Allow both the outer and inner folders to serve modules under the `locable` namespace.
__path__ = pkgutil.extend_path(__path__, __name__)  # type: ignore[name-defined]

_inner = Path(__file__).resolve().parent / "locable"
if _inner.exists():
    inner_path = str(_inner)
    if inner_path not in __path__:
        __path__.append(inner_path)
