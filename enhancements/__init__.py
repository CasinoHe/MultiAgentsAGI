import pkgutil
import os

# Import all modules in the current package
__path__ = pkgutil.extend_path(__path__, __name__)
for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    full_module_name = f"{__name__}.{module_name}"
    __import__(full_module_name)
