# finddata version
try:
    from ._version import __version__  # noqa: F401
except ImportError:
    __version__ = "unknown"

# Import publish_plot functions from external package if available
# This maintains backward compatibility while removing local duplicate code
try:
    from plot_publisher import plot1d, plot_heatmap, publish_plot  # noqa: F401
except ImportError:
    # plot_publisher not available - functions will not be accessible
    # but module will still import successfully
    pass
