# -*- coding: utf-8 -*-

import importlib
from threading import local
import plum.lang

__copyright__ = u"Copyright (c), 2015, ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE (Theory and Simulation of Materials (THEOS) and National Centre for Computational Design and Discovery of Novel Materials (NCCR MARVEL)), Switzerland and ROBERT BOSCH LLC, USA. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.5.0"
__contributors__ = "Andrea Cepellotti, Giovanni Pizzi, Martin Uhrin"


override = plum.lang.override(check=False)
protected = plum.lang.protected(check=False)


class ProcessStack(object):
    # Use thread-local storage for the stack
    _thread_local = local()

    @staticmethod
    def scoped(process):
        return ProcessStack(process)

    @classmethod
    def top(cls):
        return cls.stack()[-1]

    @classmethod
    def stack(self):
        try:
            return self._thread_local.wf_stack
        except AttributeError:
            self._thread_local.wf_stack = []
            return self._thread_local.wf_stack

    @classmethod
    def push(cls, process):
        try:
            process._parent = cls.top()
        except IndexError:
            process._parent = None
        cls.stack().append(process)

    @classmethod
    def pop(cls):
        process = cls.stack().pop()
        process._parent = None

    def __init__(self, process):
        self._process = process

    def __enter__(self):
        self.push(self._process)

    def __exit__(self, type, value, traceback):
        self.pop()


def load_class(classstring):
    """
    Load a class from a string
    """
    class_data = classstring.split(".")
    module_path = ".".join(class_data[:-1])
    class_name = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_name)


def is_workfunction(func):
    try:
        return func._is_workfunction
    except AttributeError:
        return False
