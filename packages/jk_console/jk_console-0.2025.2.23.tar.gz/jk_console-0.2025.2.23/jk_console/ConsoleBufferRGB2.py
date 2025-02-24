



from .Console import *
from .ConsoleBufferRGB_Mixins import *
from ._Rect import _Rect
from .RGBColorMapper import RGBColorMapper
from .FramedBoxSettingsRGB import FramedBoxSettingsRGB
from .SimpleTable import *







_ConsoleBufferRGBCell2 = typing.NewType("_ConsoleBufferRGBCell2", object)

class _ConsoleBufferRGBCell2(object):

	def __init__(self, colorBG:int, colorFG:int, c:str = " "):
		self.data = [ colorBG, colorFG, c ]
	#

	def copyTo(self, other:_ConsoleBufferRGBCell2):
		if other.data != self.data:
			# other.data = list(self.data)
			other.data.clear()
			other.data.extend(self.data)
	#

#



#
# This class implements a buffer for the text console. It consists of individual cells, one for every character.
#
class ConsoleBufferRGB2(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, width:int = None, height:int = None, bgColor:int = None, bTransparent:bool = False):
		self.__width = Console.width() - 1 if width is None else width
		self.__height = Console.height() - 1 if height is None else height
		self.__widthM1 = self.__width - 1
		self.__heightM1 = self.__height - 1
		self.__numberOfCells = self.__width * self.__height
		self.__bTransparent = bTransparent
		self.__bgColor = bgColor

		self.__lineNumbers = tuple(range(0, self.__height))
		self.__columnNumbers = tuple(range(0, self.__width))

		c = None if bTransparent else " "
		self.__dataMatrix = [ [ _ConsoleBufferRGBCell2(bgColor, None, c) for x in self.__columnNumbers ] for y in self.__lineNumbers ]

		# ----------------------------------------------------------------

		self.__asserts()

		# ----------------------------------------------------------------
		# caching

		self.__colorMapper = RGBColorMapper()
		self.__oldData = None
		self.__oldX = None
		self.__oldY = None

		# ----------------------------------------------------------------

		self.defaultFramedBoxSettings = FramedBoxSettingsRGB()

		# ----------------------------------------------------------------

		# if bgColor is not None:
		# 	self.fill(bgColor, None, None)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns a tuple with two values: The width and height.
	#
	@property
	def size(self):
		return self.__width, self.__height
	#

	@property
	def width(self):
		return self.__width
	#

	@property
	def height(self):
		return self.__height
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __asserts(self):
		assert len(self.__lineNumbers) == self.__height
		assert len(self.__columnNumbers) == self.__width
		assert len(self.__dataMatrix) == self.__height
		for i in range(0, self.__height):
			assert len(self.__dataMatrix[i]) == self.__width
	#

	def __dumpToSimpleTable(self) -> SimpleTable:
		t = SimpleTable()
		for row in self.__dataMatrix:
			tRow = t.addRow()
			for cell in row:
				d = [
					IntRGB.toCSS(cell.data[0]) if cell.data[0] is not None else "-",
					IntRGB.toCSS(cell.data[1]) if cell.data[1] is not None else "-",
					repr(cell.data[2]) ]
				tRow.addCell().value = ":".join(d)

		for i in range(0, t.numberOfColumns - 1):
			t.column(i).vlineAfterColumn = True
		for i in range(0, t.numberOfRows - 1):
			t.row(i).hlineAfterRow = True

		return t
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	#
	# Grow the buffer vertically by the specified number of rows.
	#
	def growBufferY(self, nRows:int):
		assert isinstance(nRows, int)
		assert nRows >= 0

		if nRows == 0:
			return

		c = None if self.__bTransparent else " "
		for i in range(0, nRows):
			_row = [ _ConsoleBufferRGBCell2(self.__bgColor, None, c) for x in self.__columnNumbers ]
			self.__dataMatrix.append(_row)

		self.__height += nRows

		self.__heightM1 = self.__height - 1
		self.__numberOfCells = self.__width * self.__height
		self.__lineNumbers = tuple(range(0, self.__height))

		self.__asserts()

		# clear caching

		self.__oldData = None
		self.__oldX = None
		self.__oldY = None
	#

	def extract(self, r:Rect):
		rf = r.intersect(Rect(0, 0, self.__width, self.__height))
		if (rf.width == 0) or (rf.height == 0):
			return None
		b = ConsoleBufferRGB2(rf.width, rf.height)
		self.bufferToBufferCopy(-r.x, -r.y, b)
		return b
	#

	#
	# During rendering to the console color values are mapped from int to str.
	# This cache can grow as it is not cleared automatically. If you use a large variety of colors
	# you might want to clear this cache from time to time.
	#
	def clearColorRenderingCache(self):
		self.__colorMapper.clear()
	#

	def __str__(self):
		return "<ConsoleBufferRGB2 size=%dx%d at %x>" % (self.__width, self.__height, id(self))
	#

	def __repr__(self):
		return "<ConsoleBufferRGB2 size=%dx%d at %x>" % (self.__width, self.__height, id(self))
	#

	#
	# Copy the content of this buffer overwriting all data in the cells of the destination buffer.
	#
	def bufferToBufferCopy(self, ofsX:int, ofsY:int, other):
		assert isinstance(other, ConsoleBufferRGB2)

		sourceRect = _Rect(0, 0, self.__width, self.__height)
		destRect = _Rect(0, 0, other.__width, other.__height)
		destRect0 = sourceRect.clone().move(ofsX, ofsY).intersect(destRect)
		sourceRect0 = destRect0.clone().move(-ofsX, -ofsY)

		for y in range(0, destRect0.height):
			currentRowSrc = self.__dataMatrix[sourceRect0.y + y]
			currentRowDest = other.__dataMatrix[destRect0.y + y]
			for x in range(0, destRect0.width):
				currentCellSrc = currentRowSrc[sourceRect0.x + x]
				currentCellDest = currentRowDest[destRect0.x + x]

				if currentCellDest.data != currentCellSrc.data:
					currentCellDest.data = list(currentCellSrc.data)
	#

	#
	# Copy the content of this buffer overwriting only data in the cells of the destination buffer the source buffer can provide.
	# This allows copying color information only if no content is present.
	#
	def bufferToBufferMerge(self, ofsX:int, ofsY:int, other):
		assert isinstance(other, ConsoleBufferRGB2)

		sourceRect = _Rect(0, 0, self.__width, self.__height)
		destRect = _Rect(0, 0, other.__width, other.__height)
		destRect0 = sourceRect.clone().move(ofsX, ofsY).intersect(destRect)
		sourceRect0 = destRect0.clone().move(-ofsX, -ofsY)

		for y in range(0, destRect0.height):
			currentRowSrc = self.__dataMatrix[sourceRect0.y + y]
			currentRowDest = other.__dataMatrix[destRect0.y + y]
			for x in range(0, destRect0.width):
				currentCellSrc = currentRowSrc[sourceRect0.x + x]
				currentCellDest = currentRowDest[destRect0.x + x]

				for i, v in enumerate(currentCellSrc.data):
					if v is not None:
						currentCellDest.data[i] = v
	#

	def bufferToConsole(self, ofsX:int = 0, ofsY:int = 0):
		if self.__bTransparent:
			raise Exception("Transparent buffers can not be copied to the screen. Rendering would fail.")

		# calculate change matrix and cache all data

		bChangedMatrix = []
		if (self.__oldData is not None) and (self.__oldX == ofsX) and (self.__oldY == ofsY):
			oldData = self.__oldData
			for iy, row in enumerate(self.__dataMatrix):
				bChangedRow = []
				for ix, cell in enumerate(row):
					bChanged = oldData[iy][ix] != cell.data
					bChangedRow.append(bChanged)
					if bChanged:
						oldData[iy][ix] = list(cell.data)
				bChangedMatrix.append(bChangedRow)
		else:
			oldData = []
			for iy, row in enumerate(self.__dataMatrix):
				bChangedRow = []
				oldRow = []
				for ix, cell in enumerate(row):
					bChangedRow.append(True)
					oldRow.append(list(cell.data))
				oldData.append(oldRow)
				bChangedMatrix.append(bChangedRow)
			self.__oldX = ofsX
			self.__oldY = ofsY
			self.__oldData = oldData

		# print the new data

		characters = []
		for y in self.__lineNumbers:
			currentRow = self.__dataMatrix[y]
			bCurrentRowChanged = bChangedMatrix[y]

			# scan for changed areas

			bLineIsModified = False
			fromX = 999999
			toX = -1
			for x in self.__columnNumbers:
				if bCurrentRowChanged[x]:
					fromX = x
					bLineIsModified = True
					break

			if bLineIsModified:
				for x in reversed(self.__columnNumbers):
					if bCurrentRowChanged[x]:
						toX = x
						break
			else:
				# no changes => continue
				continue

			# now perform paint

			characters.clear()
			characters.append("\033[" + str(ofsY + y + 1) + ";" + str(ofsX + fromX + 1) + "H")	# position cursor

			lastCol = None
			for x in self.__columnNumbers[fromX:toX + 1]:
				currentCell = currentRow[x]
				currentCol = (currentCell.data[0], currentCell.data[1])
				if lastCol != currentCol:	# has the color changed compared to last cell?
					# yes it has changed
					lastCol = currentCol
					characters.append(self.__colorMapper(currentCol[0], currentCol[1]))

				c = currentCell.data[2]
				characters.append(" " if c is None else c)

			characters.append(Console.RESET)
			print("".join(characters), end='', flush=False)

		print(Console.RESET_TOPLEFT, end="", flush=True)	# reset color output and position cursor
	#

	def dump(self):
		t = self.__dumpToSimpleTable()
		t.print()
	#

	def dumpToFile(self, filePath:str):
		assert isinstance(filePath, str)

		t = self.__dumpToSimpleTable()
		with open(filePath, "w") as fout:
			for line in t.printToLines():
				fout.write(line)
				fout.write("\n")
	#

	#
	# Fill the entire buffer with the specified color and character.
	#
	def fill(self, bgColor:int, fgColor:int, character:str = " "):
		if character is not None:
			assert isinstance(character, str)
			assert len(character) == 1
		if bgColor is not None:
			assert isinstance(bgColor, int)
		if fgColor is not None:
			assert isinstance(fgColor, int)

		for y in self.__lineNumbers:
			for x in self.__columnNumbers:
				cell = self.__dataMatrix[y][x]

				if bgColor is not None:
					cell.data[0] = bgColor

				if fgColor is not None:
					cell.data[1] = fgColor

				if character is not None:
					cell.data[2] = character
	#

	#
	# Fill a single cell with color and character.
	#
	def set(self, x:int, y:int, bgColor:int, fgColor:int, character:str):
		cell = self.__dataMatrix[y][x]

		if bgColor is not None:
			assert isinstance(bgColor, int)
			cell.data[0] = bgColor

		if fgColor is not None:
			assert isinstance(fgColor, int)
			cell.data[1] = fgColor

		if character is not None:
			assert isinstance(character, str)
			assert len(character) == 1
			cell.data[2] = character
	#

	#
	# Fill a single cell with color and character.
	#
	def setSafe(self, x:int, y:int, bgColor:int, fgColor:int, character:str):
		if (x < 0) or (y < 0) or (x >= self.__width) or (y >= self.__height):
			return

		cell = self.__dataMatrix[y][x]

		if bgColor is not None:
			assert isinstance(bgColor, int)
			cell.data[0] = bgColor

		if fgColor is not None:
			assert isinstance(fgColor, int)
			cell.data[1] = fgColor

		if character is not None:
			assert isinstance(character, str)
			assert len(character) == 1
			cell.data[2] = character
	#

	def printText(self, x:int, y:int, bgColor:int, fgColor:int, text:str):
		assert isinstance(x, int)
		assert isinstance(y, int)
		if bgColor is not None:
			assert isinstance(bgColor, int)
		if fgColor is not None:
			assert isinstance(fgColor, int)
		assert isinstance(text, str)
		if len(text) == 0:
			return

		for i, c in enumerate(text):
			cell = self.__dataMatrix[y][x + i]

			if bgColor is not None:
				cell.data[0] = bgColor

			if fgColor is not None:
				cell.data[1] = fgColor

			cell.data[2] = c
	#

	def hline(self, x1:int, y:int, x2:int, bgColor:int, fgColor:int, character:str):
		assert isinstance(x1, int)
		assert isinstance(y, int)
		assert isinstance(x2, int)
		if bgColor is not None:
			assert isinstance(bgColor, int)
		if fgColor is not None:
			assert isinstance(fgColor, int)
		assert isinstance(character, str)
		assert len(character) == 1

		row = self.__dataMatrix[y]
		for ix in range(x1, x2 + 1):
			cell = row[ix]

			if bgColor is not None:
				cell.data[0] = bgColor

			if fgColor is not None:
				cell.data[1] = fgColor

			if cell.data[2] != character:
				cell.data[2] = character
	#

	def vline(self, x:int, y1:int, y2:int, bgColor:int, fgColor:int, character:str):
		assert isinstance(x, int)
		assert isinstance(y1, int)
		assert isinstance(y2, int)
		if bgColor is not None:
			assert isinstance(bgColor, int)
		if fgColor is not None:
			assert isinstance(fgColor, int)
		assert isinstance(character, str)
		assert len(character) == 1

		for iy in range(y1, y2 + 1):
			cell = self.__dataMatrix[iy][x]

			if bgColor is not None:
				cell.data[0] = bgColor

			if fgColor is not None:
				cell.data[1] = fgColor

			if cell.data[2] != character:
				cell.data[2] = character
	#

	def drawFrame(self, rect:Rect, settings:FramedBoxSettingsRGB = None):
		assert isinstance(rect, Rect)
		x1 = rect.x1
		y1 = rect.y1
		x2 = rect.x2 - 1		# TODO
		y2 = rect.y2 - 1		# TODO

		if settings is None:
			settings = self.defaultFramedBoxSettings
		else:
			assert isinstance(settings, FramedBoxSettingsRGB)

		self.hline(x1, y1, x2, settings.frameColorBG, settings.frameColorFG, settings.frameCharTop)
		self.hline(x1, y2, x2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottom)
		self.vline(x1, y1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharLeft)
		self.vline(x2, y1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharRight)
		self.set(x1, y1, settings.frameColorBG, settings.frameColorFG, settings.frameCharTopLeft)
		self.set(x2, y1, settings.frameColorBG, settings.frameColorFG, settings.frameCharTopRight)
		self.set(x1, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottomLeft)
		self.set(x2, y2, settings.frameColorBG, settings.frameColorFG, settings.frameCharBottomRight)
	#

	def fillRectangle(self, rect:Rect, bgColor:int, fgColor:int, character:str):
		assert isinstance(rect, Rect)
		x1 = rect.x1
		y1 = rect.y1
		x2 = rect.x2		# TODO
		y2 = rect.y2		# TODO

		if bgColor is not None:
			assert isinstance(bgColor, int)

		if fgColor is not None:
			assert isinstance(fgColor, int)

		assert isinstance(character, str)
		assert len(character) == 1

		for iy in range(y1, y2):
			row = self.__dataMatrix[iy]
			for ix in range(x1, x2):
				cell = row[ix]

				if bgColor is not None:
					cell.data[0] = bgColor

				if fgColor is not None:
					cell.data[1] = fgColor

				if cell.data[2] != character:
					cell.data[2] = character
	#

#



