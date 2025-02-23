# *-* encoding: utf-8 *-*
"""
Copyright (c) 2024, IsBenben and all contributors
Licensed under the Apache License, Version 2.0
"""

from .chars import Chars
from ..ansi import Ansi, ansi_print
from typing import Optional, NoReturn, Self
from .panel import Panel
from .align import align_type, align
from .base import text_width

class Column:
    def __init__(self, name: str | None, style: Ansi = Ansi.reset(), align: align_type = 'left', head_style: Ansi = Ansi.style('bold')):
        self.name = name
        self.style = style
        self.width = text_width(name) if name is not None else 0
        self.align: align_type = align
        self.head_style = head_style
    
    def print_head(self, panel: Optional[Panel] = None) -> None:
        if self.name is None:
            raise ValueError("Column has no name")
        ansi_print(align(self.name, self.align, self.width), self.head_style, panel)

class Table:
    def __init__(self, columns: Optional[list[Column | str]] = None):
        if columns is not None:
            self.columns_none = False
            self.columns = [(Column(column) if isinstance(column, str) else column) for column in columns]
            self._calu_width()
        else:
            self.columns_none = True
            self.columns = columns
        self.rows = []
    
    def _calu_width(self):
        if not self.columns:
            raise ValueError("Table has no columns")
        self.width = 1
        for column in self.columns:
            self.width += column.width + 1

    def add_row(self, row: list[str]) -> Self:
        self.rows.append(row)
        if self.columns is None:
            self.columns = [Column(None) for _ in range(len(row))]
        if len(row) != len(self.columns):
            raise ValueError("Row length not match with columns length")
        
        for item, column in zip(row, self.columns):
            column.width = max(column.width, text_width(item))
        self._calu_width()
        return self

    def from_list(self, data: list[list[str]]):
        for row in data:
            self.add_row(row)
        return self

    def print(self, chars: Chars, panel: Optional[Panel]=None) -> Self | NoReturn:
        if not self.columns:
            raise ValueError("Table has no columns")

        row_id = 0
        last_row = len(self.rows) + (self.columns is not None)
        def _print_line(row: int) -> None:
            if self.columns is None:
                turns = [0]
            else:
                turns = [0]
                for column in self.columns:
                    turns.append(turns[-1] + column.width + 1)
            config = {
                'style': None,
                'panel': panel,
                'auto_reset': False
            }
            ansi_print('', chars.style, panel=panel, auto_reset=False)
            for i in range(self.width):
                if i == 0:
                    if row == 0:
                        ansi_print(chars.left_top, **config)
                    elif row == last_row:
                        ansi_print(chars.left_bottom, **config)
                    else:
                        ansi_print(chars.left, **config)
                elif i == self.width - 1:
                    if row == 0:
                        ansi_print(chars.right_top, **config)
                    elif row == last_row:
                        ansi_print(chars.right_bottom, **config)
                    else:
                        ansi_print(chars.right, **config)
                elif i in turns:
                    if row == 0:
                        ansi_print(chars.top, **config)
                    elif row == last_row:
                        ansi_print(chars.bottom, **config)
                    else:
                        ansi_print(chars.center, **config)
                else:
                    ansi_print(chars.horizontal, **config)
            ansi_print('\n', panel=panel)
        colored_vertical = chars.style.code + chars.vertical + Ansi.reset().code

        # Print head
        if not self.columns_none:
            _print_line(0)
            row_id = 1
            for i, column in enumerate(self.columns):
                ansi_print(colored_vertical, panel=panel)
                column.print_head(panel)
            ansi_print(colored_vertical, panel=panel)
            ansi_print('\n', panel=panel)
        
        if not self.rows:
            ansi_print('No data', Ansi.string('black').light().style('italic'), panel=panel)
            return self
        
        # Print rows
        for row in self.rows:
            _print_line(row_id)
            for item, column in zip(row, self.columns):
                ansi_print(colored_vertical, panel=panel)
                ansi_print(align(item, column.align, column.width), column.style, panel)
            ansi_print(colored_vertical, panel=panel)
            ansi_print('\n', panel=panel)
            row_id += 1

        _print_line(last_row)
        return self
