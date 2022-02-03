from ds4win.emulator import click, hold, buttons, move

# You can click at any button as you wish:
click.right(); buttons.right.click(); buttons.click.right(); 
buttons.click('right'); click('right')
# And hold it (the default argument is 1 second):
hold.right(); buttons.right.hold(); buttons.hold.right()

# Do you want to hold left dpad button for 5 seconds?
buttons.left.hold(5) # done!

# Use move_left_thumb or move_right_thumb function to move thumbs around.
# You should use both x and y keyword arguments. They should be integer
# ranging from -128 to 127; if the value is bigger or less than the range
# then it will be clumped.
hold.move_right_thumb(2, x=127, y=127)
hold.move_right_thumb(2, x=256, y=1000) # both x and y are clumped to 127.
hold.move_left_thumb(5,x=0,y=256) # y is clumped to 127
# To ease the syntax you can use module move and its subclasses
# left_thumb, right_thumb:
move.left_thumb(2, 25, 25)
# Or use this functions:
move.left_thumb.right()
move.left_thumb.slightly_right()
move.left_thumb.hard_right()
# Or even this:
from ds4win.emulator.move import left_thumb, right_thumb 
left_thumb.move.slightly_left_and_up()
left_thumb.move.hard_right_and_up()
left_thumb.move.hard_right_and_slightly_up()
left_thumb.move.hard_right_slightly_up() # same as hard_right_and_slightly_up()
# In fact, you can use it with any attribute:
from ds4win.emulator.move import left, right
left.move.right90slightlyup() # 90, 64
right.move.SlIGhTlYRight_and_even_write_anything_hereUp1234() # 64, 127