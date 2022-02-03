import sys

from . import signals
from . import __hold as hold_module

_HOLD__HOLD_CONST = 1

class hold:  
    class __hold_wrapper:
        def __new__(cls, func, *args, **kwargs):
            if not hasattr(cls, '__functions'):
                cls.__functions = {}
            if func not in cls.__functions.keys():
                cls.__functions[func] = super(getattr(hold,'_hold__hold_wrapper'), cls).__new__(cls)
            return cls.__functions[func]
        def __init__(self, func, *args, **kwargs):
            self.__func_name = func
        def __call__(self, hold_for=_HOLD__HOLD_CONST, *, x=None, y=None):
            if x is None:
                getattr(hold_module, self.__func_name)(hold_for)
            elif y is not None:
                getattr(hold_module, self.__func_name)(hold_for, x, y)
            else:
                getattr(hold_module, self.__func_name)(hold_for,x)
        def one_second(self,*, x=None, y=None):
            self.__call__(1, x=x, y=y)
        def two_seconds(self, *,x=None,y=None):
            self.__call__(2,x=y,y=y)
    
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(hold, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        for i in signals.list:
            setattr(hold, i, getattr(hold,'_hold__hold_wrapper')(i))
            
    
    def __call__(self, function, hold_for=_HOLD__HOLD_CONST, *, x=None, y=None):
        getattr(self, function)(hold_for,x=x,y=y)

sys.modules[__name__] = hold()