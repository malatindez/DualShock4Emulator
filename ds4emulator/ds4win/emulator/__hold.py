from ..emulator import Signal
import time
def up(hold_for = 1):
    t = Signal('up', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def right(hold_for = 1):
    t = Signal('right', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def down(hold_for = 1):
    t = Signal('down', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def left(hold_for = 1):
    t = Signal('left', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();

def triangle(hold_for = 1):
    t = Signal('triangle', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def circle(hold_for = 1):
    t = Signal('circle', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def cross(hold_for = 1):
    t = Signal('cross', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def square(hold_for = 1):
    t = Signal('square', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();

def l1(hold_for = 1):
    t = Signal('l1', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def r1(hold_for = 1):
    t = Signal('r1', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();


def left_thumb(hold_for = 1):
    t = Signal('left_thumb', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def right_thumb(hold_for = 1):
    t = Signal('right_thumb', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
    
def options(hold_for = 1):
    t = Signal('options', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def share(hold_for = 1):
    t = Signal('share', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
def touchpad(hold_for = 1):
    t = Signal('touchpad', hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();
    
def left_trigger(hold_for = 1, *, x):
    t = Signal('left_trigger', x = x, hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();

def right_trigger(hold_for = 1, *, x):
    t = Signal('right_trigger', x = x, hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();

def move_left_thumb(hold_for = 1, *, x, y):
    t = Signal('move_left_thumb', x = x, y = y, hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();

def move_right_thumb(hold_for = 1,  *, x, y):
    t = Signal('move_right_thumb', x = x, y = y, hold_for = hold_for)
    if (t.is_set()):
        time.sleep(0.02); t.clear(); time.sleep(0.02)
    t.set();