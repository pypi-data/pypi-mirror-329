


import typing

from .Console import Console






class SimpleTableConstants(object):

	HALIGN_LEFT = 0
	HALIGN_CENTER = 1
	HALIGN_RIGHT = 2

	CASE_NORMAL = 0
	CASE_LOWER = 1
	CASE_UPPER = 2

#



class SimpleTableCell(SimpleTableConstants):

	def __init__(self, table):
		self.__table = table
		self.halign = None
		self.__value = None
		self.__len:int = -1
		self.color = None
		self.textTransform = None
	#

	@property
	def value(self):
		return self.__value
	#

	@value.setter
	def value(self, value) -> None:
		self.__value = value
		self.__len = -1
	#

	def __str__(self):
		if self.__value is None:
			return ""
		else:
			return str(self.__value)
	#

	def __len__(self):
		if self.__len < 0:
			if self.__value is None:
				self.__len = 0
			else:
				self.__len = len(Console.stripESCSequences(str(self.__value)))

		return self.__len
	#

#



class SimpleTableColumn(SimpleTableConstants):

	def __init__(self, table, columnIndex:int, rows:list):
		self.columnIndex = columnIndex
		self.__table = table
		#self.__columnData = columnData
		self.halign = None
		self.textTransform = None
		self.__rows = rows
		self.color = None
		self.vlineAfterColumn = False
		self.marginLeft = 1
		self.marginRight = 1
	#

	def getMaxWidth(self):
		return max([ (len(row) if row else 0) for row in self.__rows ])
	#

	"""
	@property
	def halign(self) -> int:
		return self.__columnData.get("halign", SimpleTableConstants.HALIGN_DEFAULT)
	#

	@halign.setter
	def halign(self, v:int):
		self.__columnData["halign"] = v
	#
	"""

	def __getitem__(self, index:int):
		assert isinstance(index, int)
		if index >= len(self.__rows):
			return None
		return self.__rows[index]
	#

	def __setitem__(self, index:int, v):
		raise NotImplementedError()
	#

	def __len__(self):
		return len(self.__rows)
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, type, value, traceback):
		pass
	#

#



class SimpleTableRow(SimpleTableConstants):

	def __init__(self, table):
		self.__table = table
		self.__cells = []
		table._getColumnsList(0).append(self)
		self.halign = None
		self.color = None
		self.textTransform:int = None
		self.hlineAfterRow = False
	#

	def _removeColumn(self, nColumn:int):
		del self.__cells[nColumn]
	#

	def addCell(self) -> SimpleTableCell:
		c = SimpleTableCell(self.__table)
		self.__table._getColumnsList(len(self.__cells)).remove(self)
		self.__cells.append(c)
		self.__table._getColumnsList(len(self.__cells)).append(self)
		return c
	#

	def addCells(self, *args):
		self.__table._getColumnsList(len(self.__cells)).remove(self)
		for a in args:
			c = SimpleTableCell(self.__table)
			self.__cells.append(c)
			c.value = a
		self.__table._getColumnsList(len(self.__cells)).append(self)
	#

	def __getitem__(self, index:int) -> typing.Union[SimpleTableCell,None]:
		assert isinstance(index, int)
		if index >= len(self.__cells):
			return None
		return self.__cells[index]
	#

	def __setitem__(self, index:int, v):
		raise NotImplementedError()
	#

	def __len__(self):
		return len(self.__cells)
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, type, value, traceback):
		pass
	#

#



class SimpleTable(SimpleTableConstants):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.__rows:typing.List[SimpleTableRow] = []
		self.__columns_cached:typing.Dict[int,SimpleTableColumn] = {}

		# groups rows with the same number of columns under the same key.
		# the reason for that is no longer known.
		self.__nColumns:typing.Dict[int,typing.List[SimpleTableRow]] = {
			0: []
		}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def numberOfColumns(self) -> int:
		return max(self.__nColumns.keys())
	#

	@property
	def numberOfRows(self) -> int:
		return len(self.__rows)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _getColumnsList(self, n:int) -> typing.List[SimpleTableRow]:
		cols = self.__nColumns.get(n)
		if cols is None:
			cols = []
			self.__nColumns[n] = cols
		return cols
	#

	#
	# Calculate the width of the specific column.
	#
	def _getColumnWidth(self, nColumn:int) -> int:
		cells = self.__getColumnCells(nColumn)
		if cells:
			return max([ (len(c) if c else 0) for c in cells ])
		else:
			return 0
	#

	#
	# Calculate the width of all columns.
	#
	def _getColumnWidths(self) -> typing.List[int]:
		return [ self._getColumnWidth(n) for n in range(0, self.numberOfColumns) ]
	#

	def __getColumnCells(self, nColumn:int) -> typing.List[SimpleTableCell]:
		columnCells:typing.List[SimpleTableCell] = []
		for row in self.__rows:
			columnCells.append(row[nColumn])
		return columnCells
	#

	def __printToBuffer(self, outBuffer:list, prefix:str = "", gapChar = " ", vLineChar = "|", hLineChar = "-", crossChar = "|", useColors:bool = True):
		columnWidths = self._getColumnWidths()

		for row in self.__rows:
			rowCells = [ prefix ]
			data = []
			for nColumn in range(0, len(columnWidths)):
				bIsLastColumn = nColumn == (len(columnWidths) - 1)
				column = self.column(nColumn)
				halign, color, textTransform, text, textLen = self.__getCellData(row, column, row[nColumn])
				if not useColors:
					color = None
				if color:
					rowCells.append(color)
				text = self.__hformatCellText(text, textLen, halign, textTransform, columnWidths[nColumn], column.marginLeft, column.marginRight)
				rowCells.append(text)
				if color:
					rowCells.append(Console.RESET)

				if column.vlineAfterColumn:
					rowCells.append(vLineChar)
				else:
					if not bIsLastColumn:
						rowCells.append(gapChar)

				data.append((nColumn, column, text))

			outBuffer.append("".join(rowCells))

			if row.hlineAfterRow:
				rowCells.clear()
				rowCells.append(prefix)
				rowGapHLine = hLineChar * len(gapChar)
				for nColumn, column, text in data:
					hline = hLineChar * len(text)
					rowCells.append(hline)

					if column.vlineAfterColumn:
						rowCells.append(crossChar)
					else:
						rowCells.append(rowGapHLine)

				outBuffer.append("".join(rowCells))
	#

	def __getCellData(self, row:SimpleTableRow, column:SimpleTableColumn, cell:SimpleTableCell) -> typing.Tuple[int,str,int,str,int]:
		# collect data: cell vs. row vs. column

		if cell:
			s = str(cell)
			lenS:int = len(cell)
			halign:int = cell.halign
			color:str = cell.color
			textTransform:int = cell.textTransform
		else:
			s = ""
			lenS:int = 0
			halign:int = None
			color:str = None
			textTransform:int = None

		if halign is None:
			halign = row.halign
		if halign is None:
			halign = column.halign

		if color is None:
			color = row.color
		if color is None:
			color = column.color

		if textTransform is None:
			textTransform = row.textTransform
		if textTransform is None:
			textTransform = column.textTransform

		return halign, color, textTransform, s, lenS
	#

	#
	# @param		str text				(required) The text to format.
	# @param		int textLen				(required) The length of the text in visible characters.
	#										NOTE: We need this value as our text data might contain color codes and
	#										calculating the real character length of this text data is quite expensive.
	# @param		int halign				(required) Horizontal alignment
	# @param		int textTransform		(required) Text transformation
	# @param		int width				(required) Width in number of characters
	# @param		int marginLeft			(required) Left margin in number of characters
	# @param		int marginRight			(required) Right margin in number of characters
	#
	def __hformatCellText(self, text:str, textLen:int, halign:int, textTransform:int, width:int, marginLeft:int, marginRight:int) -> str:
		if textTransform == SimpleTableConstants.CASE_LOWER:
			text = text.lower()
		elif textTransform == SimpleTableConstants.CASE_UPPER:
			text = Console.colorSensitiveToUpper(text)
			#text = text.upper()

		if halign in [ None, SimpleTableConstants.HALIGN_LEFT ]:
			text = text + " " * (width - textLen)
		elif halign == SimpleTableConstants.HALIGN_CENTER:
			spc = " " * ((width - textLen) // 2 + 1)
			text = spc + text + spc
			text = text[:width]
		elif halign == SimpleTableConstants.HALIGN_RIGHT:
			text = " " * (width - textLen) + text
		else:
			raise Exception()

		if marginLeft:
			text = " " * marginLeft + text
		if marginRight:
			text += " " * marginRight

		return text
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	def addRow(self, *args) -> SimpleTableRow:
		r = SimpleTableRow(self)
		self.__rows.append(r)
		if args:
			r.addCells(*args)
		return r
	#

	def __len__(self):
		return len(self.__rows)
	#

	def column(self, nColumn:int) -> SimpleTableColumn:
		d = self.__columns_cached.get(nColumn)
		if d is None:
			d = SimpleTableColumn(self, nColumn, self.__rows)
			self.__columns_cached[nColumn] = d
		return d
	#

	def row(self, nRow:int) -> SimpleTableRow:
		if (nRow >= len(self.__rows)) or (nRow < 0):
			return None
		return self.__rows[nRow]
	#

	#
	# Print the table.
	#
	def print(self, prefix:str = "", gapChar = " ", vLineChar = "|", hLineChar = "-", crossChar = "|", printFunction = None, useColors:bool = True):
		if printFunction is None:
			printFunction = print

		outBuffer = []
		self.__printToBuffer(outBuffer, prefix, gapChar, vLineChar, hLineChar, crossChar, useColors)

		for line in outBuffer:
			printFunction(line)
	#

	#
	# Print the table.
	#
	def printToLines(self, prefix:str = "", gapChar = " ", vLineChar = "|", hLineChar = "-", crossChar = "|", useColors:bool = True) -> list:
		outBuffer = []
		self.__printToBuffer(outBuffer, prefix, gapChar, vLineChar, hLineChar, crossChar, useColors)
		return outBuffer
	#

	def printToTextFile(self, filePath:str, prefix:str = "", gapChar = " ", vLineChar = "|", hLineChar = "-", crossChar = "|", useColors:bool = True):
		with open(filePath, "w") as f:
			f.write("\n".join(self.printToLines(prefix, gapChar, vLineChar, hLineChar, crossChar, useColors)))
			f.write("\n")
	#

	def raw(self) -> list:
		ret = []

		for row in self.__rows:
			rowCells = []
			for nColumn in range(0, self.numberOfColumns):
				column = self.column(nColumn)
				halign, color, textTransform, text, textLen = self.__getCellData(row, column, row[nColumn])
				rowCells.append(self.__hformatCellText(text, textLen, None, textTransform, 0, 0, 0))
			ret.append(rowCells)

		return ret
	#

	def addEmptyRow(self, bAddOnlyIfLastRowNotEmpty:bool = True) -> SimpleTableRow:
		if bAddOnlyIfLastRowNotEmpty:
			if len(self.__rows):
				if self.__rows[-1]:
					return self.addRow()
			return None
		else:
			return self.addRow()
	#

	def removeColumn(self, nColumn:int):
		assert isinstance(nColumn, int)
		assert 0 <= nColumn < self.numberOfColumns

		self.__columns_cached.clear()

		for row in self.__rows:
			self._getColumnsList(len(row)).remove(row)
		for row in self.__rows:
			row._removeColumn(nColumn)
		for row in self.__rows:
			self._getColumnsList(len(row)).append(row)
	#

#




