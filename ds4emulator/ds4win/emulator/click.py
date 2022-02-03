import sys

from . import __click as click_module


class click:  
    class __click_wrapper:
        def __new__(cls, func, *args, **kwargs):
            if not hasattr(cls, '__functions'):
                cls.__functions = {}
            if func not in cls.__functions.keys():
                cls.__functions[func] = super(getattr(click,'_click__click_wrapper'), cls).__new__(cls)
            return cls.__functions[func]
        def __init__(self, func, *args, **kwargs):
            self.__func_name = func
        def __call__(self, n = 1):
            self.n(n)
        def once(self):
            self.n(1)
        def twice(self):
            self.n(2)
        def n(self, n):
            for _ in range(n):
                getattr(click_module, self.__func_name)()
    
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(click, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        for i in click_module.list:
            setattr(self, i, getattr(click,'_click__click_wrapper')(i))
    
    def __call__(self, function, n=1):
        getattr(self, function).n(n)


sys.modules[__name__] = click()