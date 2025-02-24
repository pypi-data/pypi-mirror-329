



from .Console import *
from .Rect import *
from .IntRGB import *






class FramedBoxSettingsRGB(object):

	def __init__(self):
		self.bgColor = IntRGB.parseCSS("#000000")
		self.bgChar = " "
		self.frameColorBG = IntRGB.parseCSS("#000000")
		self.frameColorFG = IntRGB.parseCSS("#e0e0e0")
		self.frameCharLeft = "|"
		self.frameCharRight = "|"
		self.frameCharTop = "-"
		self.frameCharBottom = "-"
		self.frameCharTopLeft = "/"
		self.frameCharTopRight = "\\"
		self.frameCharBottomLeft = "\\"
		self.frameCharBottomRight = "/"
		self.textColorBG = IntRGB.parseCSS("#000000")
		self.textColorFG = IntRGB.parseCSS("#e0e0e0")
	#

#




class ConsoleBufferRGB_Mixins:

	def _Mixins_init(self):
		self.defaultFramedBoxSettings = FramedBoxSettingsRGB()
	#

	#
	# Fill the entire buffer with the default background color.
	#
	def clear(self):
		bgColor = self._bgColor
		for y in self._lineNumbers:
			for x in self._columnNumbers:
				cell = self._data[y][x]
				cell.c = " "
				cell.bgColor = bgColor
				cell.fgColor = None
				cell.bChanged = True
		self._bFullPaint = True
	#

	#
	# Fill the entire buffer with the specified color and character.
	#
	def fill(self, bgColor:int, fgColor:int, character:str):
		if character is not None:
			assert len(character) == 1

		for y in self._lineNumbers:
			for x in self._columnNumbers:
				cell = self._data[y][x]
				if character is not None:
					cell.c = character
				if bgColor is not None:
					cell.colBG = bgColor
				if fgColor is not None:
					cell.colFG = fgColor
		self._bFullPaint = True
	#

	#
	# Fill a single cell with color and character.
	#
	def set(self, x:int, y:int, bgColor:int, fgColor:int, character:str):
		cell = self._data[y][x]
		if character is not None:
			assert len(character) == 1
			cell.c = character
			cell.bChanged = True
		if bgColor is not None:
			cell.colBG = bgColor
			cell.bChanged = True
		if fgColor is not None:
			cell.colFG = fgColor
			cell.bChanged = True
	#

	#
	# Fill a single cell with color and character.
	#
	def setSafe(self, x:int, y:int, bgColor:int, fgColor:int, character:str):
		if (x < 0) or (y < 0) or (x >= self._width) or (y >= self._height):
			return
		cell = self._data[y][x]
		if character is not None:
			assert len(character) == 1
			cell.c = character
			cell.bChanged = True
		if bgColor is not None:
			cell.colBG = bgColor
			cell.bChanged = True
		if fgColor is not None:
			cell.colFG = fgColor
			cell.bChanged = True
	#

	def printText(self, x:int, y:int, bgColor:int, fgColor:int, text:str):
		assert len(text) > 0

		i = 0
		for c in text:
			cell = self._data[y][x + i]
			cell.c = c
			if bgColor is not None:
				cell.colBG = bgColor
			if fgColor is not None:
				cell.colFG = fgColor
			cell.bChanged = True
			i += 1
	#

	def hline(self, x1:int, y:int, x2:int, bgColor:int, fgColor:int, character:str):
		assert len(character) == 1

		row = self._data[y]
		for ix in range(x1, x2 + 1):
			cell = row[ix]
			cell.c = character
			if bgColor is not None:
				cell.colBG = bgColor
			if fgColor is not None:
				cell.colFG = fgColor
			cell.bChanged = True
	#

	def vline(self, x:int, y1:int, y2:int, bgColor:int, fgColor:int, character:str):
		assert len(character) == 1

		for iy in range(y1, y2 + 1):
			cell = self._data[iy][x]
			cell.c = character
			if bgColor is not None:
				cell.colBG = bgColor
			if fgColor is not None:
				cell.colFG = fgColor
			cell.bChanged = True
	#

	"""
	def printBoxedText(self, centerX:int, centerY:int, text:str, settings:FramedBoxSettingsRGB = None):
		if settings is None:
			settings = self.defaultFramedBoxSettings

		wtext = len(text)
		x1 = centerX - int(wtext/2) - 2
		x2 = x1 + 4 + wtext
		y1 = centerY - 2
		y2 = centerY + 2
		w = x2 - x1
		h = y2 - y1

		self.hline(x1, y1, x2, settings.frameColor, settings.frameCharTop)
		self.hline(x1, y2, x2, settings.frameColor, settings.frameCharBottom)
		self.vline(x1, y1, y2, settings.frameColor, settings.frameCharLeft)
		self.vline(x2, y1, y2, settings.frameColor, settings.frameCharRight)
		self.set(x1, y1, settings.frameColor, settings.frameCharTopLeft)
		self.set(x2, y1, settings.frameColor, settings.frameCharTopRight)
		self.set(x1, y2, settings.frameColor, settings.frameCharBottomLeft)
		self.set(x2, y2, settings.frameColor, settings.frameCharBottomRight)
		self.fill(x1 + 1, y1 + 1, w - 2, h - 2, settings.bgColor, settings.bgChar)
		self.printText(x1 + 2, y1 + 2, settings.textColor, text)
	#
	"""

	def drawFrame(self, rect:Rect = None, x1:int = None, y1:int = None, x2:int = None, y2:int = None, settings:FramedBoxSettingsRGB = None):
		if settings is None:
			settings = self.defaultFramedBoxSettings

		if rect:
			x1 = rect.x1
			y1 = rect.y1
			x2 = rect.x2 - 1
			y2 = rect.y2 - 1

		self.hline(x1, y1, x2, settings.frameColorBG, settings.frameColorFG, settings.frameCharTop)
		self.hline(x1, y2, x2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottom)
		self.vline(x1, y1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharLeft)
		self.vline(x2, y1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharRight)
		self.set(x1, y1, settings.frameColorBG, settings.frameColorFG, settings.frameCharTopLeft)
		self.set(x2, y1, settings.frameColorBG, settings.frameColorFG, settings.frameCharTopRight)
		self.set(x1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottomLeft)
		self.set(x2, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottomRight)
	#

	def fillRectangle(self, x:int, y:int, w:int, h:int, bgColor:int, fgColor:int, character:str):
		assert len(character) == 1

		for iy in range(y, y + h):
			row = self._data[iy]
			for ix in range(x, x + w):
				cell = row[ix]
				cell.c = character
				if bgColor is not None:
					cell.colBG = bgColor
				if fgColor is not None:
					cell.colFG = fgColor
				cell.bChanged = True
	#

#



