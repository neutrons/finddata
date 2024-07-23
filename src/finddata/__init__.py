# finddata version
try:
    from ._version import __version__  # noqa: F401
except ImportError:
    __version__ = "unknown"

from .publish_plot import publish_plot # noqa: F401
