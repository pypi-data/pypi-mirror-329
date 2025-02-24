


class RGBColorMapper(object):

	def __init__(self):
		# for rendering to the console: these maps hold int->str pairs assigning the string representations of colors to their integer representations
		self.__colMapBG = {}
		self.__colMapFG = {}
	#

	#
	# During rendering to the console color values are mapped from int to str.
	# This cache can grow as it is not cleared automatically. If you use a large variety of colors
	# you might want to clear this cache from time to time.
	#
	def clear(self):
		self.__colMapBG.clear()
		self.__colMapFG.clear()
	#

	#
	# Convert the rgb color values to a string. The result is cached.
	#
	def get(self, bgRGB:int, fgRGB:int):
		s = ""
		if bgRGB is not None:
			colStr = self.__colMapBG.get(bgRGB)
			if colStr is None:
				colStr = "\033[48;2;" + str((bgRGB >> 16) & 0xff) + ";" + str((bgRGB >> 8) & 0xff) + ";" + str(bgRGB & 0xff) + "m"
				self.__colMapBG[bgRGB] = colStr
			s += colStr
		if fgRGB is not None:
			colStr = self.__colMapFG.get(fgRGB)
			if colStr is None:
				colStr = "\033[38;2;" + str((fgRGB >> 16) & 0xff) + ";" + str((fgRGB >> 8) & 0xff) + ";" + str(fgRGB & 0xff) + "m"
				self.__colMapFG[fgRGB] = colStr
			s += colStr
		return s
	#

	#
	# Convert the rgb color values to a string. The result is cached.
	#
	def __call__(self, bgRGB:int, fgRGB:int):
		s = ""
		if bgRGB is not None:
			colStr = self.__colMapBG.get(bgRGB)
			if colStr is None:
				colStr = "\033[48;2;" + str((bgRGB >> 16) & 0xff) + ";" + str((bgRGB >> 8) & 0xff) + ";" + str(bgRGB & 0xff) + "m"
				self.__colMapBG[bgRGB] = colStr
			s += colStr
		if fgRGB is not None:
			colStr = self.__colMapFG.get(fgRGB)
			if colStr is None:
				colStr = "\033[38;2;" + str((fgRGB >> 16) & 0xff) + ";" + str((fgRGB >> 8) & 0xff) + ";" + str(fgRGB & 0xff) + "m"
				self.__colMapFG[fgRGB] = colStr
			s += colStr
		return s
	#

#












