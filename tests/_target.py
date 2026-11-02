"""Point the test suite at either your attempts or the reference solutions.

By default the tests import from `drills/`, which is where you work.
Set PPHR_TARGET=solutions to run the identical tests against the reference
answers - if those ever fail, the test is wrong, not you. Worth doing after
you add a new drill of your own.
"""
import importlib
import os

TARGET = os.environ.get("PPHR_TARGET", "drills")


def mod(name):
    """Import one week's module from whichever target is selected.

    :param name: module name without the package, e.g. "week01_data_structures"
    :return: the imported module
    """
    return importlib.import_module(f"{TARGET}.{name}")
