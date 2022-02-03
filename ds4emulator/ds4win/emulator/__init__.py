import ctypes, time
import signal, atexit, struct 
from ctypes import c_ulonglong
from threading import Lock
from . import signals

RELEASE_CONST = 0.1
lib = None
try:
    lib = ctypes.CDLL(__file__+f'\\..\\..\\DS4Emulator{struct.calcsize("P")*8}.dll')
except OSError:
    print('You can not use this library in more than 1 process.\nIt is already loaded somewhere.')
except FileNotFoundError:
    raise FileNotFoundError("Rather DS4Emulator.dll is not located within the ds4win folder or you haven't installed ViGEmBus:\nhttps://github.com/ViGEm/ViGEmBus/releases")
if lib is None:
    raise ModuleNotFoundError('')
time.sleep(0.1) # wait until the library is initialized

# just a simple structure to store controller signals.
# hold_for paramemeter defines amount of time to hold the button, in seconds.
# hold_until parameter defines when button should be released, in seconds
class Signal:
    def __init__(self, function, *, hold_for = None, hold_until = None, x = None, y = None):
        if function not in signals.list:
            raise ValueError(f'Unknown signal {function}')
        if not ((hold_for is None) ^ (hold_until is None)):
            raise ValueError('Neither hold_for or hold_until keyword arguments were given' if 
                             hold_for is None else 'hold_for and hold_until cannot be passed simultaneously')
              

        if not str(function):
            raise ValueError(f'__Signal() argument must be a string, not {type(function)}')
        if function not in signals.list:
            raise ValueError(f'{function} is not a valid Signal to call')
        if 'trigger' not in function and 'move' not in function and (x is not None or y is not None):
            raise ValueError(f'{function} does not need a x or y arguments.')
        if 'trigger' in function and x is None:
            raise ValueError(f'{function} needs a keyword argument x')
        if 'move' in function and (x is None or y is None):
            raise ValueError(f'{function} needs both x and y keyword arguments')
        self.function = function
        self.hold_for = hold_for
        self.hold_until = hold_until
        self.x = x; self.y = y
        
    def set(self):
        from .. import emulator
        emulator.set_signal(self)
    
    def set_if_not_set(self):
        from .. import emulator
        emulator.set_if_not_set(self)
    
    def clear(self):
        from .. import emulator
        emulator.clear_signal(self)
    
    def is_set(self):
        from .. import emulator
        return emulator.is_pressed(self.function)


class Updater:
    @staticmethod
    def __clump(x, a, b):
        return int(a if x < a else b if x > b else x)
    @staticmethod
    def __up(microsec):
        lib.HoldUp(c_ulonglong(microsec))
    @staticmethod
    def __right(microsec):
        lib.HoldRight(c_ulonglong(microsec))
    @staticmethod
    def __down(microsec):
        lib.HoldDown(c_ulonglong(microsec))
    @staticmethod
    def __left(microsec):
        lib.HoldLeft(c_ulonglong(microsec))
    @staticmethod
    def __triangle(microsec):
        lib.HoldTriangle(c_ulonglong(microsec))
    @staticmethod
    def __circle(microsec):
        lib.HoldCircle(c_ulonglong(microsec))
    @staticmethod
    def __cross(microsec):
        lib.HoldCross(c_ulonglong(microsec))
    @staticmethod
    def __square(microsec):
        lib.HoldSquare(c_ulonglong(microsec))
    @staticmethod
    def __l1(microsec):
        lib.HoldLeftShoulder(c_ulonglong(microsec))
    @staticmethod
    def __r1(microsec):
        lib.HoldRightShoulder(c_ulonglong(microsec))
    @staticmethod
    def __left_thumb(microsec): # click on left thumb
        lib.HoldLeftThumb(c_ulonglong(microsec))
    @staticmethod
    def __right_thumb(microsec): # click on right thumb
        lib.HoldRightThumb(c_ulonglong(microsec))
        
    @staticmethod
    def __options(microsec):
        lib.HoldOptions(c_ulonglong(microsec))
    @staticmethod
    def __share(microsec):
        lib.HoldShare(c_ulonglong(microsec))
    @staticmethod
    def __touchpad(microsec):
        lib.HoldTouchpad(c_ulonglong(microsec))
    @staticmethod
    def __left_trigger(microsec, x):
        x = Updater.__clump(x, 0, 255); 
        lib.LeftTrigger(c_ulonglong(microsec), ctypes.c_uint8(x))
    @staticmethod
    def __right_trigger(microsec, x):
        x = Updater.__clump(x, 0, 255); 
        lib.RightTrigger(c_ulonglong(microsec), ctypes.c_uint8(x))
        
    @staticmethod
    def __move_left_thumb(microsec, x, y):
        x = Updater.__clump(x, -128, 127); y = Updater.__clump(y, -128, 127)
        lib.MoveLeftThumb(c_ulonglong(microsec), ctypes.c_int8(x), ctypes.c_int8(y))
        
    @staticmethod
    def __move_right_thumb(microsec, x, y):
        x = Updater.__clump(x, -128, 127); y = Updater.__clump(y, -128, 127)
        lib.MoveRightThumb(c_ulonglong(microsec), ctypes.c_int8(x), ctypes.c_int8(y))
        
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Updater, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__signals = {
            key: [] for key in signals.list
        }
        self.__signal_mutex = Lock()
        self.__signals = {key: None for key in signals.list}
        
    def status(self):
        return [
            value for value in self.__signals.values() 
                if value is not None and value.hold_until > time.time()
        ]
    
    def is_pressed(self, str):
        if str not in self.__signals.keys():
            raise ValueError('Unknown signal {str}')
        return self.__signals[str] is not None and self.__signals[str].hold_until > time.time()
    

    
    
    def set_signal(self, signal): 
        if not isinstance(signal, Signal):
            raise ValueError(f'set_signal() argument must be a Signal, not {type(signal)}')
        if  not hasattr(self, '_Updater__' + signal.function):
            raise ValueError(f'Unknown function {signal.function}')
        self.__signal_mutex.acquire()
        try:
            if signal.hold_until is None:
                signal.hold_until = time.time() + signal.hold_for
            self.__signals[signal.function] = signal
            x,y = signal.x, signal.y
            if x is None:
                getattr(self, '_Updater__' + signal.function)(int(signal.hold_until*1e6))
            elif y is not None:
                getattr(self, '_Updater__' + signal.function)(int(signal.hold_until*1e6), x, y)
            else:
                getattr(self, '_Updater__' + signal.function)(int(signal.hold_until*1e6), x)
        finally:
            self.__signal_mutex.release()
    
    def clear_signal(self, signal): 
        if not isinstance(signal, Signal):
            raise ValueError(f'clear_signal() argument must be a Signal, not {type(signal)}')
        if  not hasattr(self, '_Updater__' + signal.function):
            raise ValueError(f'Unknown function {signal.function}')
        self.__signal_mutex.acquire()
        try:
            self.__signals[signal.function] = signal
            x,y = signal.x, signal.y
            if x is None:
                getattr(self, '_Updater__' + signal.function)(0)
            elif y is not None:
                getattr(self, '_Updater__' + signal.function)(0, x, y)
            else:
                getattr(self, '_Updater__' + signal.function)(0, x)
        finally:
            self.__signal_mutex.release()

__updater = Updater()

"""
Returns signals that are present.
"""
def status():
    return __updater.status()


"""
Returns true if the signal is present.
The argument str should be a string.
"""
def is_pressed(str):
    return __updater.is_pressed(str)

"""
Sets Signal to the emulator.
The argument signal should be an instance of emulator.Signal
"""
def set_signal(signal): 
    __updater.set_signal(signal)

"""
Sets Signal to the emulator if it's not present.
The argument signal should be an instance of emulator.Signal
"""
def set_if_not_set(signal):
    if not __updater.is_pressed(signal.function):
        __updater.set_signal(signal)

"""
Clears the signal.
The argument signal should be an instance of emulator.Signal
"""
def clear_signal(signal): 
    __updater.clear_signal(signal)

from math import ceil
def f(target, depth = 4, prev = 0):
    if depth == 0:
        if prev == target ** 5:
            return []
        else:
            return None
    dist = target - 1
    i = dist
    while dist > 0 and i > 0:
        dist = ceil(dist / 2)
        if prev + i ** 5 > target ** 5:
            i -= dist
            if dist == 1 and prev + i ** 5 <= target ** 5:
                break
        else:
            i += dist
    while i > 0:
        k = f(target, depth - 1, prev + i ** 5) 
        if k is not None:
            k.append(i)
            return k
        i -= 1