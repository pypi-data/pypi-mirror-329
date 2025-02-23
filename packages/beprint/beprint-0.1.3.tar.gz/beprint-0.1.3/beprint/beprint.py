# *-* encoding: utf-8 *-*
"""
Copyright (c) 2024, IsBenben and all contributors
Licensed under the Apache License, Version 2.0
"""

from typing import Any, Optional, overload, Callable
from .layout.panel import Panel
from .layout.base import GetStdout
from .ansi import Ansi, ansi_print
from dataclasses import is_dataclass

class BeprintStyle:
    string = Ansi.string('cyan')
    number = Ansi.string('blue')
    true = Ansi.string('green').style('italic')
    false = Ansi.string('red').style('italic')
    none = Ansi.string('magenta').style('italic')
    symbol = Ansi.string('black').light().style('bold')
    obj = Ansi.string('yellow')

class Attrs:
    NO = DIABLED = 0
    YES = ENABLED = 1
    MAGIC = 2
    CLASS = 4

def beprint(*obj: Any, panel: Optional[Panel] = None, attrs: int=Attrs.DIABLED, maxdepth: int=3):
    if len(obj) == 1:
        obj = obj[0]
    i = '  '
    printed_objectes = {}
    def _bp(obj: Any, indent_depth: int = 0, depth: int = 0):
        if printed_objectes.get(id(obj)):
            ansi_print('circular references', BeprintStyle.symbol, panel)
            return None
        
        indent = i * indent_depth
        printed_objectes.setdefault(id(obj), 0)
        printed_objectes[id(obj)] += 1
        repr_obj = repr(obj)

        if isinstance(obj, bool):
            if obj:
                ansi_print(repr_obj, BeprintStyle.true, panel)
            else:
                ansi_print(repr_obj, BeprintStyle.false, panel)
        elif isinstance(obj, str):
            ansi_print(repr_obj, BeprintStyle.string, panel)
        elif isinstance(obj, (int, float)):
            ansi_print(repr_obj, BeprintStyle.number, panel)
        elif obj is None:
            ansi_print(repr_obj, BeprintStyle.none, panel)
        elif type(obj) in (list, tuple, set, frozenset):
            first_char = repr_obj[0] if type(obj) != frozenset else 'frozenset({'
            last_char = repr_obj[-1] if type(obj) != frozenset else '})'
            if depth >= maxdepth:
                ansi_print(first_char + ' exceeding the maximum depth ' + last_char, BeprintStyle.symbol, panel)
            elif len(obj) <= 1:
                ansi_print(first_char, BeprintStyle.symbol, panel)
                for item in obj:
                    _bp(item, 0, depth + 1)
                ansi_print(last_char, BeprintStyle.symbol, panel)
            else:
                ansi_print(first_char + '\n', BeprintStyle.symbol, panel)
                for item in obj:
                    ansi_print(indent + i, BeprintStyle.symbol, panel)
                    _bp(item, depth + 1, depth + 1)
                    ansi_print(',\n', BeprintStyle.symbol, panel)
                ansi_print(indent + last_char, BeprintStyle.symbol, panel)
        elif type(obj) == dict:
            if depth >= maxdepth:
                ansi_print('{ exceeding the maximum depth }', BeprintStyle.symbol, panel)
            elif len(obj) <= 1:
                ansi_print('{', BeprintStyle.symbol, panel)
                for key, value in obj.items():
                    _bp(key, 0, depth + 1)
                    ansi_print(': ', BeprintStyle.symbol, panel)
                    _bp(value, 0, depth + 1)
                ansi_print('}', BeprintStyle.symbol, panel)
            else:
                ansi_print('{\n', BeprintStyle.symbol, panel)
                for key, value in obj.items():
                    ansi_print(indent + i, BeprintStyle.symbol, panel)
                    _bp(key, depth + 1, depth + 1)
                    ansi_print(': ', BeprintStyle.symbol, panel)
                    _bp(value, depth + 1, depth + 1)
                    ansi_print(',\n', BeprintStyle.symbol, panel)
                ansi_print(indent + '}', BeprintStyle.symbol, panel)
        else:
            if (attrs & Attrs.ENABLED \
                   or (obj.__repr__ == object.__repr__ and obj.__str__ == object.__str__) \
                   or (is_dataclass(obj) and type(obj) != type)) \
                   and depth < maxdepth:
                if hasattr(obj, '__module__') and obj.__module__:
                    class_name = obj.__module__ + '.' + type(obj).__name__
                else:
                    class_name = type(obj).__name__
                ansi_print('<' + class_name + ' object at ' + hex(id(obj)), BeprintStyle.obj, panel)
                flag = True
                for attr_name in dir(obj):
                    if not hasattr(obj, attr_name):
                        continue
                    if attrs & Attrs.CLASS or not hasattr(type(obj), attr_name):
                        if attrs & Attrs.MAGIC or not attr_name.startswith('__'):
                            if flag:
                                ansi_print('\n', BeprintStyle.symbol, panel)
                                flag = False
                            attr_value = getattr(obj, attr_name)
                            ansi_print(indent + i, BeprintStyle.symbol, panel)
                            ansi_print(attr_name, BeprintStyle.string, panel)
                            ansi_print('=', BeprintStyle.symbol, panel)
                            _bp(attr_value, depth + 1, depth + 1)
                            ansi_print(',\n', BeprintStyle.symbol, panel)
                if flag:
                    ansi_print('>', BeprintStyle.obj, panel)
                else:
                    ansi_print(indent + '>', BeprintStyle.obj, panel)
            else:
                ansi_print(repr_obj, BeprintStyle.obj, panel)
    
        printed_objectes[id(obj)] -= 1
    res = _bp(obj)
    print()
    return res

bp = beprint

@overload
def add_beprint(attrs: int, *, maxdepth: int) -> Callable: ...
@overload
def add_beprint(attrs: type) -> type: ...

def add_beprint(attrs = Attrs.ENABLED, *, maxdepth: int = 3):  # type: ignore[return-type]
    def decorator(func: type):
        def wrapper(self):
            assert isinstance(attrs, int)
            with GetStdout() as stdout:
                beprint(self, attrs=attrs, maxdepth=maxdepth)
            return stdout.value
        func.__str__ = wrapper
        return func
    if isinstance(attrs, type):
        func = attrs
        attrs = Attrs.ENABLED
        return decorator(func)
    return decorator
