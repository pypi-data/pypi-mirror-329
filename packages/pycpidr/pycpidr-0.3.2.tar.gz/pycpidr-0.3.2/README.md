# pycpidr - DEPRECATED

**This package is deprecated. Please use [ideadensity](https://pypi.org/project/ideadensity/) instead.**

`pycpidr` has been renamed to `ideadensity` for better clarity about the purpose of the package. 
This package only exists as a compatibility layer that will install the `ideadensity` package
and show a deprecation warning when imported.

## Migration

To migrate from `pycpidr` to `ideadensity`, simply:

1. Install the new package:
   ```
   pip install ideadensity
   ```

2. Update your imports from:
   ```python
   from pycpidr import cpidr, depid
   ```
   to:
   ```python
   from ideadensity import cpidr, depid
   ```

The functionality remains exactly the same - only the package name has changed.

## Python Version Compatibility

**Note**: This package (and ideadensity) currently supports Python 3.10-3.12 due to dependency constraints with spaCy. If you're using Python 3.13, you'll need to use a virtual environment with Python 3.12. See the [ideadensity documentation](https://github.com/jrrobison1/pycpidr#python-version-compatibility) for detailed instructions.
