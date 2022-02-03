import sys

from . import signals
from . import click as click_module, hold as hold_module
from . import __click as _click
from . import move

_buttons__thismodule = sys.modules[__name__]

class _buttons__button_wrapper:
    def __new__(cls, func, *args, **kwargs):
        if not hasattr(cls, '__functions'):
            cls.__functions = {}
        if func not in cls.__functions.keys():
            cls.__functions[func] = super(_buttons__button_wrapper, cls).__new__(cls)
        return cls.__functions[func]
    def __init__(self, func, *args, **kwargs):
        if func in _click.list:
            self.click = getattr(click_module,func)
        if func in signals.list:
            self.hold = getattr(hold_module,func)
        if func in move.list:
            self.move = getattr(move,func)
    def __call__(self, n = 1):
        self.click(n)

for i in signals.list + ['l2', 'r2']:
    setattr(_buttons__thismodule, i, _buttons__button_wrapper(i))

click = click_module
hold = hold_module

