import builtins
import sys
# Save the original __build_class__ function
original_build_class = builtins.__build_class__

# Define the custom repr function
def custom_repr(self):
    """Custom representation for all classes."""
    # Get attributes
    attribute_list = []
    for key, value in self.__dict__.items():
        if isinstance(value, str):
            formatted_value = f'"{value}"'
        else:
            formatted_value = repr(value)
        attribute_string = f"{key}: {formatted_value}"
        attribute_list.append(attribute_string)
    
    # Get methods
    method_list = []
    for key, value in type(self).__dict__.items():
        if callable(value) and not key.startswith('__'):
            method_string = f"{key}()"
            method_list.append(method_string)
    
    # Combine attributes and methods
    parts = []
    if attribute_list:
        parts.append("{ " + ", ".join(attribute_list) + " }")
    if method_list:
        parts.append(" || " + ", ".join(method_list))
    
    result = f"{self.__class__.__name__} => {''.join(parts)}"
    return result

# Define a custom metaclass
class CustomMeta(type):
    def __new__(cls, name, bases, dct):
        if '__repr__' not in dct:
            dct['__repr__'] = custom_repr
        return super().__new__(cls, name, bases, dct)

def is_user_module(module_name, module_file):
    """Check if the module is a user-created module."""
    if not module_file:  # Built-in modules don't have a file
        return False
        
    # Get the virtual environment path if it exists
    venv_path = sys.prefix

    # Check if the module is from standard library or site-packages
    is_stdlib = module_file.startswith(sys.prefix) or module_file.startswith(sys.base_prefix)
    is_site_packages = 'site-packages' in module_file or 'dist-packages' in module_file
    
    return not (is_stdlib or is_site_packages)

# Define a custom __build_class__ function
def custom_build_class(func, name, *args, **kwargs):
    # If metaclass is specified anywhere, use original build
    if 'metaclass' in kwargs or (args and any(type(base) is not type for base in args)):
        return original_build_class(func, name, *args, **kwargs)
    
    # Get the calling frame
    frame = sys._getframe(1)
    module_name = frame.f_globals.get('__name__', '')
    module_file = frame.f_globals.get('__file__', '')

    # Only apply custom metaclass to user modules
    if is_user_module(module_name, module_file):
        kwargs['metaclass'] = CustomMeta
    
    return original_build_class(func, name, *args, **kwargs)

# Monkey-patch __build_class__
builtins.__build_class__ = custom_build_class