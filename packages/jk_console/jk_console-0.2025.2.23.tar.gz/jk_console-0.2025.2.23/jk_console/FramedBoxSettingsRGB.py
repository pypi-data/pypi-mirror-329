

from .IntRGB import IntRGB




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





