# __init__.py
from .core import custom_repr, CustomMeta, custom_build_class, custom_repr_config
import builtins

# Apply the monkey-patch when the library is imported
builtins.__build_class__ = custom_build_class

# Optional: Export any public APIs or symbols
__all__ = ['custom_repr', 'custom_repr_config']

__version__ = "2.1.1"