import sys
if sys.platform != "win32":
	import termios
	import tty
else:
	import msvcrt

def pause():
	if sys.platform == "win32":
		msvcrt.getch()
	else:
		TerminalSettings = termios.tcgetattr(sys.stdin.fileno())
		try:
			tty.setraw(sys.stdin.fileno())
			sys.stdin.read(1)
		finally:
			termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, TerminalSettings)