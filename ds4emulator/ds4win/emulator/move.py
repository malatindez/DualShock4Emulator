import sys
import re
from . import __hold as hold
__vlist = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
__alist = {'slightly': 64, 'hard': 128}
def _to_xy(name):
    def is_int(val):
        try:
            int(val)
        except:
            return False
        return True
    name = re.findall('(slightly|hard|up|down|right|left|[-]{0,1}[0-9]+|[a-z]+)',name)
    x,y = (0,0)
    pa, pb = (0,0)
    nval = 96
    for key in name:
        if key in __alist.keys():
            nval = __alist[key]
        elif key in __vlist.keys():
            x += pa * nval; y += pb * nval
            if pa != 0 or pb != 0:
                nval = 96
            pa, pb = __vlist[key]
        elif is_int(key):
            nval = int(key)
    if pa != 0 or pb != 0:
        x += pa * nval; y += pb * nval
    return (x,y)

class move:
    list = ['left_thumb', 'right_thumb']
    class _left_thumb:
        def __call__(cls, hold_for=1, x=None, y=None, *args, **kwargs):
            if x is None or y is None:
                raise ValueError('You should pass x or y keyword arguments to use this function.')
            hold.move_left_thumb(hold_for, x=x, y=y)
        def __getattribute__(self, name: str):
            if name == 'move':
                return self
            x,y = _to_xy(name)
            t = lambda hold_for=1: hold.move_left_thumb(hold_for, x=x, y=y)
            t.x = x; t.y = y
            return t
    class _right_thumb:
        def __call__(cls, hold_for=1, x=None, y=None, *args, **kwargs):
            if x is None or y is None:
                raise ValueError('You should pass x or y keyword arguments to use this function.')
            hold.move_right_thumb(hold_for, x=x, y=y)
        def __getattribute__(self, name: str):
            if name == 'move':
                return self
            x,y = _to_xy(name)
            t = lambda hold_for=1: hold.move_right_thumb(hold_for, x=x, y=y)
            t.x = x; t.y = y
            return t
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(move, cls).__new__(cls)
            cls.left_thumb = move._left_thumb()
            cls.right_thumb = move._right_thumb()
        return cls._instance



sys.modules[__name__] = move()