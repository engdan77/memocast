import os
import pkgutil
import importlib
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))  # Load all modules dynamically

for module in (_ for _ in __all__ if not 'baseclass' in _):
    importlib.import_module(f'.{module}', __package__)