import sys
import builtins
from rich.text import Text
from rich.console import Console
from abc import ABCMeta

# Global configuration
SHOW_ATTRIBUTES = True
SHOW_METHODS = True

# Function to set global configuration
def custom_repr_config(attributes=True, methods=True):
    """
    Configure the output format of custom_repr.
    
    Args:
        attributes (bool): Whether to show attributes (default: True)
        methods (bool): Whether to show methods (default: True)
    
    Example:
        custom_repr_config(True, False)  # Show attributes only
        custom_repr_config(False, True)  # Show methods only
        custom_repr_config(True, True)   # Show both attributes and methods
        custom_repr_config(False, False) # Show class name only
    """
    global SHOW_ATTRIBUTES, SHOW_METHODS
    SHOW_ATTRIBUTES = attributes
    SHOW_METHODS = methods

# Save the original __build_class__ function
original_build_class = builtins.__build_class__


def custom_repr(self):
    """Custom representation for all classes."""
    console = Console()
    
    # Get attributes with colors
    attribute_list = []
    if SHOW_ATTRIBUTES:  # Check if attributes should be shown
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                formatted_value = Text(f'"{value}"', style="green")  # strings in green
            elif isinstance(value, bool):
                formatted_value = Text(str(value), style="cyan")  # booleans in red
            elif isinstance(value, (int, float)):
                formatted_value = Text(str(value), style="magenta")  # numbers in yellow
            else:
                formatted_value = Text(repr(value), style="white")
            
            key_text = Text(key, style="yellow")  # keys in cyan
            colon_text = Text(": ", style="white")
            attribute_string = Text.assemble(key_text, colon_text, formatted_value)
            attribute_list.append(attribute_string)
    
    # Get methods
    method_list = []
    if SHOW_METHODS:  # Check if methods should be shown
        for key, value in type(self).__dict__.items():
            if callable(value) and not key.startswith('__'):
                method_text = Text(f"{key}()", style="magenta")  # methods in magenta
                method_list.append(method_text)
    
    # Combine parts with colors
    class_name = Text(self.__class__.__name__, style="bold blue")
    
    # If attributes is False, only display the class name
    if not SHOW_ATTRIBUTES and not SHOW_METHODS:
        # Capture and return just the class name
        with console.capture() as capture:
            console.print(class_name)
        return capture.get().rstrip()
    
    # Otherwise, build the full output
    arrow = Text(" => ", style="white")
    
    # Build the output
    output = Text()
    output.append(class_name)
    output.append(arrow)
    
    if SHOW_ATTRIBUTES:
        output.append("{ ")
        if attribute_list:
            output.append(Text.join(Text(", "), attribute_list))
        output.append(" }")
    
    # Only append methods if there are any and they should be shown
    if SHOW_METHODS and method_list:
        output.append("\n[ ")
        output.append(Text.join(Text(", "), method_list))
        output.append(" ]")
    
    # Capture and return the colored output
    with console.capture() as capture:
        console.print(output)
    return capture.get().rstrip() # Remove any trailing whitespace/newline

# Update the CustomMeta class to handle ABC
class CustomMeta(ABCMeta):
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
    # Check if the class inherits from ABC but doesn't have a metaclass specified
    is_abc_class = any(arg.__name__ == 'ABC' for arg in args if hasattr(arg, '__name__'))
    has_metaclass = 'metaclass' in kwargs
    
    # If it inherits from ABC and doesn't have a metaclass, use CustomMeta
    if is_abc_class and not has_metaclass:
        kwargs['metaclass'] = CustomMeta
    # If metaclass is already something else, respect that
    elif not has_metaclass and not any(type(base) is not type for base in args):
        # For normal classes, apply CustomMeta
        kwargs['metaclass'] = CustomMeta
    
    # Call the original build class function with our updated kwargs
    return original_build_class(func, name, *args, **kwargs)


# Monkey-patch __build_class__
builtins.__build_class__ = custom_build_class