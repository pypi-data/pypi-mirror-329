import os
import glob

# Get all .py files in the current package directory
module_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

# Import each module (excluding __init__.py)
__all__ = []
for file in module_files:
    module_name = os.path.basename(file)[:-3]  # Remove ".py" extension
    if module_name != "__init__":  # Avoid importing __init__.py
        __all__.append(module_name)
        exec(f"from .{module_name} import *")  # Import everything from the module
