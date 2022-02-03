import time

from ..emulator import Signal
from .signals import list as signal_list

list = signal_list[:15] + ['l2', 'r2']

def up():
    t = Signal('up', hold_for = 0.05);
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def right():
    t = Signal('right', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def down():
    t = Signal('down', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def left():
    t = Signal('left', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()

def triangle():
    t = Signal('triangle', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def circle():
    t = Signal('circle', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def cross():
    t = Signal('cross', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def square():
    t = Signal('square', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()

def l1():
    t = Signal('l1', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def r1():
    t = Signal('r1', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()


def left_thumb():
    t = Signal('left_thumb', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def right_thumb():
    t = Signal('right_thumb', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
    
def options():
    t = Signal('options', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def share():
    t = Signal('share', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
def touchpad():
    t = Signal('touchpad', hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()
    
def l2():
    t = Signal('left_trigger', x = 255, hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()

def r2():
    t = Signal('right_trigger', x = 255, hold_for = 0.05); 
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set()