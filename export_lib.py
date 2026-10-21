import importlib
import inspect

from error import Error

LIBRARYERROR = Error("LibraryError", "Library could not be loaded.")

library_functions = {}

def load(*names):
    for name in names:
        try:
            module = importlib.import_module(f"lib.{name}")
        except ModuleNotFoundError:
            LIBRARYERROR.error(0, "", name, f"Library '{name}' not found.")
            continue

        funcs = dict(inspect.getmembers(module, inspect.isfunction))
        library_functions[name] = funcs

    return library_functions