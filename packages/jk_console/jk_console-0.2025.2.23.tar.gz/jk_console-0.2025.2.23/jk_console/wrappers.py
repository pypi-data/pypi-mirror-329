

from .Console import Console as _Console
_ConsoleFG = _Console.ForeGround




def bold(text:str) -> str:
	return "\x1b[1m" + text + "\x1b[22m"
#

def underline(text:str) -> str:
	return "\x1b[4m" + text + "\x1b[24m"
#

def italic(text:str) -> str:
	return "\x1b[3m" + text + "\x1b[23m"
#



def stdBlack(text:str) -> str:
	return _ConsoleFG.STD_BLACK + text + "\x1b[39m"
#

def stdBlue(text:str) -> str:
	return _ConsoleFG.STD_BLUE + text + "\x1b[39m"
#

def stdGreen(text:str) -> str:
	return _ConsoleFG.STD_GREEN + text + "\x1b[39m"
#

def stdCyan(text:str) -> str:
	return _ConsoleFG.STD_CYAN + text + "\x1b[39m"
#

def stdRed(text:str) -> str:
	return _ConsoleFG.STD_RED + text + "\x1b[39m"
#

def stdPurple(text:str) -> str:
	return _ConsoleFG.STD_PURPLE + text + "\x1b[39m"
#

def stdDarkYellow(text:str) -> str:
	return _ConsoleFG.STD_DARKYELLOW + text + "\x1b[39m"
#

def stdLightGray(text:str) -> str:
	return _ConsoleFG.STD_LIGHTGRAY + text + "\x1b[39m"
#

def stdDarkGray(text:str) -> str:
	return _ConsoleFG.STD_DARKGRAY + text + "\x1b[39m"
#

def stdLightBlue(text:str) -> str:
	return _ConsoleFG.STD_LIGHTBLUE + text + "\x1b[39m"
#

def stdLightGreen(text:str) -> str:
	return _ConsoleFG.STD_LIGHTGREEN + text + "\x1b[39m"
#

def stdLightCyan(text:str) -> str:
	return _ConsoleFG.STD_LIGHTCYAN + text + "\x1b[39m"
#

def stdLightRed(text:str) -> str:
	return _ConsoleFG.STD_LIGHTRED + text + "\x1b[39m"
#

def stdLightPurple(text:str) -> str:
	return _ConsoleFG.STD_LIGHTPURPLE + text + "\x1b[39m"
#

def stdYellow(text:str) -> str:
	return _ConsoleFG.STD_YELLOW + text + "\x1b[39m"
#

def stdWhite(text:str) -> str:
	return _ConsoleFG.STD_WHITE + text + "\x1b[39m"
#



def black(text:str) -> str:
	return _ConsoleFG.BLACK + text + "\x1b[39m"
#

def darkGray(text:str) -> str:
	return _ConsoleFG.DARK_GRAY + text + "\x1b[39m"
#

def gray(text:str) -> str:
	return _ConsoleFG.GRAY + text + "\x1b[39m"
#

def lightGray(text:str) -> str:
	return _ConsoleFG.LIGHT_GRAY + text + "\x1b[39m"
#

def white(text:str) -> str:
	return _ConsoleFG.WHITE + text + "\x1b[39m"
#

def red(text:str) -> str:
	return _ConsoleFG.RED + text + "\x1b[39m"
#

def orange(text:str) -> str:
	return _ConsoleFG.ORANGE + text + "\x1b[39m"
#

def yellow(text:str) -> str:
	return _ConsoleFG.YELLOW + text + "\x1b[39m"
#

def yellowGreen(text:str) -> str:
	return _ConsoleFG.YELLOWGREEN + text + "\x1b[39m"
#

def green(text:str) -> str:
	return _ConsoleFG.GREEN + text + "\x1b[39m"
#

def greenCyan(text:str) -> str:
	return _ConsoleFG.GREENCYAN + text + "\x1b[39m"
#

def cyan(text:str) -> str:
	return _ConsoleFG.CYAN + text + "\x1b[39m"
#

def cyanBlue(text:str) -> str:
	return _ConsoleFG.CYANBLUE + text + "\x1b[39m"
#

def blue(text:str) -> str:
	return _ConsoleFG.BLUE + text + "\x1b[39m"
#

def blueViolet(text:str) -> str:
	return _ConsoleFG.BLUEVIOLET + text + "\x1b[39m"
#

def violet(text:str) -> str:
	return _ConsoleFG.VIOLET + text + "\x1b[39m"
#

def violetRed(text:str) -> str:
	return _ConsoleFG.VIOLETRED + text + "\x1b[39m"
#







def darkRed(text:str) -> str:
	return _ConsoleFG.DARK_RED + text + "\x1b[39m"
#

def darkOrange(text:str) -> str:
	return _ConsoleFG.DARK_ORANGE + text + "\x1b[39m"
#

def darkYellow(text:str) -> str:
	return _ConsoleFG.DARK_YELLOW + text + "\x1b[39m"
#

def darkYellowGreen(text:str) -> str:
	return _ConsoleFG.DARK_YELLOWGREEN + text + "\x1b[39m"
#

def darkGreen(text:str) -> str:
	return _ConsoleFG.DARK_GREEN + text + "\x1b[39m"
#

def darkGreenCyan(text:str) -> str:
	return _ConsoleFG.DARK_GREENCYAN + text + "\x1b[39m"
#

def darkCyan(text:str) -> str:
	return _ConsoleFG.DARK_CYAN + text + "\x1b[39m"
#

def darkCyanBlue(text:str) -> str:
	return _ConsoleFG.DARK_CYANBLUE + text + "\x1b[39m"
#

def darkBlue(text:str) -> str:
	return _ConsoleFG.DARK_BLUE + text + "\x1b[39m"
#

def darkBlueViolet(text:str) -> str:
	return _ConsoleFG.DARK_BLUEVIOLET + text + "\x1b[39m"
#

def darkViolet(text:str) -> str:
	return _ConsoleFG.DARK_VIOLET + text + "\x1b[39m"
#

def darkVioletRed(text:str) -> str:
	return _ConsoleFG.DARK_VIOLETRED + text + "\x1b[39m"
#







def lightRed(text:str) -> str:
	return _ConsoleFG.LIGHT_RED + text + "\x1b[39m"
#

def lightOrange(text:str) -> str:
	return _ConsoleFG.LIGHT_ORANGE + text + "\x1b[39m"
#

def lightYellow(text:str) -> str:
	return _ConsoleFG.LIGHT_YELLOW + text + "\x1b[39m"
#

def lightYellowGreen(text:str) -> str:
	return _ConsoleFG.LIGHT_YELLOWGREEN + text + "\x1b[39m"
#

def lightGreen(text:str) -> str:
	return _ConsoleFG.LIGHT_GREEN + text + "\x1b[39m"
#

def lightGreenCyan(text:str) -> str:
	return _ConsoleFG.LIGHT_GREENCYAN + text + "\x1b[39m"
#

def lightCyan(text:str) -> str:
	return _ConsoleFG.LIGHT_CYAN + text + "\x1b[39m"
#

def lightCyanBlue(text:str) -> str:
	return _ConsoleFG.LIGHT_CYANBLUE + text + "\x1b[39m"
#

def lightBlue(text:str) -> str:
	return _ConsoleFG.LIGHT_BLUE + text + "\x1b[39m"
#

def lightBlueViolet(text:str) -> str:
	return _ConsoleFG.LIGHT_BLUEVIOLET + text + "\x1b[39m"
#

def lightViolet(text:str) -> str:
	return _ConsoleFG.LIGHT_VIOLET + text + "\x1b[39m"
#

def lightVioletRed(text:str) -> str:
	return _ConsoleFG.LIGHT_VIOLETRED + text + "\x1b[39m"
#



