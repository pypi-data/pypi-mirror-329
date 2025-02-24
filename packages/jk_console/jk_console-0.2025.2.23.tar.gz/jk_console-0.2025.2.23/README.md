jk_console
==========

Introduction
------------

This python module provides a variety of essential functionality for implementing versatile programs using the console. This includes:

* reading single key stokes from STDIN
* modifying cursor color
* retrieving the dimensions of the console
* placeing the cursor at (almost) any position within the console

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-console)
* [pypi.python.org](https://pypi.python.org/pypi/jk_console)

Why this module?
----------------

If you want to write some more sophisticated command line programs it will get complicated. Python does not provide any support for
reading single key strokes, colorizing output as well as more detailed control of the cursor is nothing Python takes care of. This
module fills the gap.

Limitations of this module
--------------------------

Special keys like function keys, cursor keys and similar are communicated by console windows using escape codes. Whenever you press these
keys a sequence of characters is sent by the console.

Reading these kind of key strokes from console is therefore based on reading multiple keys. Unfortunately you cannot know how many keys are
sent. Therefor you need to know how to interpret these sequences as they greatly differ in length.

The `Console` class contains a register of these sequences for common key strokes. Whenever such a key is read the class tries to parse it.
If a known keystroke is encountered it is returned as a complete string. This way `readKey()` will try to always return a single key - even
if this key is represented by multiple characters.

That implies: The `Console` class needs to know about all these character sequences. That means: **All special keys this module should
recognize must be hard coded into this module.** Whenever a known sequence is encountered it can be read completely and be recognized
as a single key stroke event. (And if the sequence is not known this mechanism will not work properly.)

This module has been adapted to recognize all common special keys a user could press in a standard Linux console window. This has been tested
on Ubuntu Linux. Please have in mind that this might differ from other platforms or even from other console implementations. At the moment
of writing these lines I as the author of `Console` have no information about how well other platforms and terminal implementations follow
these standards. I have no possibility to test this on other platforms at this point in time. So if you encounter any difficulties or have
more information please contact me. I'll gladly extend this module.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
from jk_console import Console
```

### Reading single key strokes

In order to read a single key stroke invoke the following command:

```python
key = Console.Input.readKey()
```

The variable `key` will then contain either a single character if a regular key or a set of characters if some specicial key has been pressed.

Please note that Ctrl+C is not catched by the application if you invoke `readKey()` but returned as a regular key stroke.

Please see *Limitations of this module* for information about when decoding key strokes might fail.

### Converting key strokes to text

In order to get a human readable representation of a key stroke use the following code:

```python
keyStr = Console.Input.ALL_KEYS_TO_KEY_NAME.get(key)
```

### Clearing the console screen

You can clear the current console screen by invoking the following method:

```python
Console.clear()
```

### Move cursor to a specific position on the console screen

You can move the cursor to a specific line and column number in a console using the following code:

```python
Console.moveCursorTo(lineNo, colNo)
```

Please note that row and column numbers are **always** counted starting at zero. So `(0, 0)` specifies the upper left corner of the console.

### Print text at a specific position on the console screen

You can print some text at a specific line and column number using the following code:

```python
Console.printAt(lineNo, colNo, someText)
```

Please note that row and column numbers are **always** counted starting at zero. So `(0, 0)` specifies the upper left corner of the console.

Please also note that this command will move the cursor as well. This implies that printing at the very end of a line will cause a wrap around
and the cursor will be moved to the beginning of the next line. If that happens at the very last character of your console window this will
cause the console to add a new line and thus scrolling all existing text one line upwards.

### Get current cursor position

In order to retrieve the current cursor position invoke `getCursorPosition()`:

```python
lineNo, colNo = Console.getCursorPosition()
```

Please note that row and column numbers are **always** counted starting at zero. So `(0, 0)` specifies the upper left corner of the console.

### Get the size of the console

In order to retrieve the dimensions of your console view port invoke `getSize()` and/or `width()` and `height()`:

```python
height, width = Console.getSize()
```

### Use color methods

You can perfom colorized output using the predefined constants for foreground and background.

Example:

```python
print(Console.ForeGround.CYAN + "Hello World!" + Console.RESET)
```

Alternatively you can invoke one of these color methods:

* `rgb256(r, g, b)` - which will create a text string representing your color using `int` values in the range of [0..255]
* `rgb1(r, g, b)` - which will create a text string representing your color using `float` values in the range of [0..1]
* `hsl1(h, s, l)` - which will create a text string representing your color using `float` values in the range of [0..1]

Example:

```python
print(Console.BackGround.rgb256(128, 0, 0) + "Hello World!" + Console.RESET)
```
Please note that the current color settings are valid for all future printing to the console.

### Resetting color

In order to reset color settings use the following code:

```python
print(Console.RESET)
```

### Styling text via wrapper functions

There are some functions provided for convenience that can wrap text into styling and color codes. Example:

```python
from jk_console.wrappers import *

print("This text is " + bold("bold") + ", this text is " + italic("italic"))
```

The following functions are provided:

* Styling
	* `bold(...)`
	* `italic(...)`
	* `underline(...)`
* Standard colors
	* `stdBlack(...)`
	* `stdBlue(...)`
	* `stdGreen(...)`
	* `stdCyan(...)`
	* `stdRed(...)`
	* `stdPurple(...)`
	* `stdDarkYellow(...)`,
	* `stdLightGray(...)`,
	* `stdDarkGray(...)`,
	* `stdLightBlue(...)`,
	* `stdLightGreen(...)`,
	* `stdLightCyan(...)`,
	* `stdLightRed(...)`,
	* `stdLightPurple(...)`,
	* `stdYellow(...)`
	* `stdWhite(...)`
* RGB colors
	* `black(...)`
	* `darkGrey(...)`
	* `grey(...)`
	* `lightGrey(...)`
	* `white(...)`
	* `darkRed(...)`
	* `red(...)`
	* `lightRed(...)`
	* `darkOrange(...)`
	* `orange(...)`
	* `lightOrange(...)`
	* `darkYellow(...)`
	* `yellow(...)`
	* `lightYellow(...)`
	* `darkYellowGreen(...)`
	* `yellowGreen(...)`
	* `lightYellowGreen(...)`
	* `darkGreen(...)`
	* `green(...)`
	* `lightGreen(...)`
	* `darkGreenCyan(...)`
	* `greenCyan(...)`
	* `lightGreenCyan(...)`
	* `darkCyan(...)`
	* `cyan(...)`
	* `lightCyan(...)`
	* `darkCyanBlue(...)`
	* `cyanBlue(...)`
	* `lightCyanBlue(...)`
	* `darkBlue(...)`
	* `blue(...)`
	* `lightBlue(...)`
	* `darkBlueViolet(...)`
	* `blueViolet(...)`
	* `lightBlueViolet(...)`
	* `darkViolet(...)`
	* `violet(...)`
	* `lightViolet(...)`
	* `darkVioletRed(...)`
	* `violetRed(...)`
	* `lightVioletRed(...)`

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



