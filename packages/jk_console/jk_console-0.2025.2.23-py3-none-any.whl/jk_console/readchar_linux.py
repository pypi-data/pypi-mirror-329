


import sys
import tty
import termios
import typing
from select import select




def readchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch
#

def readchar_loop():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		while True:
			yield sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#

def readkeydata_loop(timeout:typing.Union[float,int,None] = 0):
	if timeout is None:
		pass
	else:
		assert isinstance(timeout, (float,int))

	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		mode = termios.tcgetattr(fd)
		mode[6][termios.VMIN] = 0
		mode[6][termios.VTIME] = 0
		termios.tcsetattr(fd, termios.TCSAFLUSH, mode)

		if timeout:
			while True:
				rlist, _, _ = select([fd], [], [], timeout)
				if rlist:
					yield sys.stdin.buffer.read(4096)
				else:
					yield None

		else:
			while True:
				yield sys.stdin.buffer.read(4096)

	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#














