import warnings
import importlib.util

# Emit deprecation warning
warnings.warn(
    "The \"pycpidr\" package is deprecated and will no longer be maintained. "
    "Please use \"ideadensity\" instead, which is the new name for this package.",
    DeprecationWarning,
    stacklevel=2
)

# Import and expose all functions from ideadensity
try:
    from ideadensity import cpidr, depid
    __all__ = ["cpidr", "depid"]
except ImportError:
    warnings.warn(
        "The \"ideadensity\" package is required but not installed. "
        "Please install it with: pip install ideadensity",
        ImportWarning,
        stacklevel=2
    )
    __all__ = []
