

import typing

from .impl._parseCSS import parseCSS_toARGB







class IntRGB(object):

	#
	# Parse CSS codes as used by web technologies
	#
	@staticmethod
	def parseCSS(css:str):
		return parseCSS_toARGB(css)
	#

	@staticmethod
	def toCSS(rgb:int) -> str:
		assert isinstance(rgb, int)

		r = (rgb // 65536) % 256
		g = (rgb // 256) % 256
		b = rgb % 256
		return "#%0x%0x%0x" % (r, g, b)
	#

	@staticmethod
	def fade(rgbA:int, rgbB:int, f:typing.Union[float,int] = 0.5) -> int:
		assert isinstance(rgbA, int)
		assert isinstance(rgbB, int)
		assert isinstance(f, (float,int))

		rA = (rgbA // 65536) % 256
		gA = (rgbA // 256) % 256
		bA = rgbA % 256

		rB = (rgbB // 65536) % 256
		gB = (rgbB // 256) % 256
		bB = rgbB % 256

		if f < 0:
			f = 0
		if f > 1:
			f = 1
		fm1 = 1 - f

		r = round(rA*f + rB*fm1)
		g = round(gA*f + gB*fm1)
		b = round(bA*f + bB*fm1)

		return r * 65536 + g * 256 + b
	#

	@staticmethod
	def rgb256(r:int, g:int, b:int):
		assert isinstance(r, int)
		assert isinstance(g, int)
		assert isinstance(b, int)

		if not isinstance(r, int) or (r < 0) or (r > 255):
			raise Exception("Red value must be a valid integer value! (Value specified: " + str(r) + ")")
		if not isinstance(g, int) or (g < 0) or (g > 255):
			raise Exception("Red value must be a valid integer value! (Value specified: " + str(g) + ")")
		if not isinstance(b, int) or (b < 0) or (b > 255):
			raise Exception("Red value must be a valid integer value! (Value specified: " + str(b) + ")")
		return 0xff000000 | ((((r << 8) + g) << 8) + b)
	#

	@staticmethod
	def rgb1(r:float, g:float, b:float):
		if not isinstance(g, (int, float)) or (r < 0) or (r > 1):
			raise Exception("Red value must be a valid float value in the range [0..1]! (Value specified: " + str(r) + ")")
		if not isinstance(g, (int, float)) or (g < 0) or (g > 1):
			raise Exception("Green value must be a valid float value in the range [0..1]! (Value specified: " + str(g) + ")")
		if not isinstance(g, (int, float)) or (b < 0) or (b > 1):
			raise Exception("Blue value must be a valid float value in the range [0..1]! (Value specified: " + str(b) + ")")
		return 0xff000000 | ((((int(r * 255) << 8) + int(g * 255)) << 8) + int(b * 255))
	#

	@staticmethod
	def hsl1(h:float, s:float, l:float):
		if not isinstance(h, (int, float)) or (h < 0) or (h > 1):
			raise Exception("Hue value must be a valid float value in the range [0..1]! (h is " + str(h) + ")")
		if not isinstance(s, (int, float)) or (s < 0) or (s > 1):
			raise Exception("Saturation value must be a valid float value in the range [0..1]! (s is " + str(s) + ")")
		if not isinstance(l, (int, float)) or (l < 0) or (l > 1):
			raise Exception("Luminance value must be a valid float value in the range [0..1]! (l is " + str(l) + ")")

		if s == 0:
			s = 0.0001
		q = l * (1 + s) if l < 0.5 else l + s - l * s
		p = 2 * l - q
		r = IntRGB._hue2rgb(p, q, h + 1/3)
		g = IntRGB._hue2rgb(p, q, h)
		b = IntRGB._hue2rgb(p, q, h - 1/3)
		return 0xff000000 | (((int(r * 255) << 8) + int(g * 255)) << 8) + int(b * 255)
	#

	@staticmethod
	def _hue2rgb(p, q, t):
		if t < 0:
			t += 1
		if t > 1:
			t -= 1
		if t < 1/6:
			return p + (q - p) * 6 * t
		if t < 1/2:
			return q
		if t < 2/3:
			return p + (q - p) * (2/3 - t) * 6
		return p
	#

#



IntRGB.BLACK = IntRGB.parseCSS("#000000")
IntRGB.DARK_GRAY = IntRGB.parseCSS("#404040")
IntRGB.GRAY = IntRGB.parseCSS("#808080")
IntRGB.LIGHT_GRAY = IntRGB.parseCSS("#c0c0c0")
IntRGB.WHITE = IntRGB.parseCSS("#ffffff")

IntRGB.LIGHT_RED = IntRGB.parseCSS("#ff8080")
IntRGB.RED = IntRGB.parseCSS("#ff0000")
IntRGB.DARK_RED = IntRGB.parseCSS("#800000")

IntRGB.LIGHT_GREEN = IntRGB.parseCSS("#80ff80")
IntRGB.GREEN = IntRGB.parseCSS("#00ff00")
IntRGB.DARK_GREEN = IntRGB.parseCSS("#008000")

IntRGB.LIGHT_BLUE = IntRGB.parseCSS("#8080ff")
IntRGB.BLUE = IntRGB.parseCSS("#0000ff")
IntRGB.DARK_BLUE = IntRGB.parseCSS("#000080")

IntRGB.LIGHT_YELLOW = IntRGB.parseCSS("#ffff80")
IntRGB.YELLOW = IntRGB.parseCSS("#ffff00")
IntRGB.DARK_YELLOW = IntRGB.parseCSS("#808000")

IntRGB.LIGHT_VIOLET = IntRGB.parseCSS("#ff80ff")
IntRGB.VIOLET = IntRGB.parseCSS("#ff00ff")
IntRGB.DARK_VIOLET = IntRGB.parseCSS("#800080")

IntRGB.LIGHT_CYAN = IntRGB.parseCSS("#80ffff")
IntRGB.CYAN = IntRGB.parseCSS("#00ffff")
IntRGB.DARK_CYAN = IntRGB.parseCSS("#008080")

IntRGB.LIGHT_ORANGE = IntRGB.parseCSS("#ffc080")
IntRGB.ORANGE = IntRGB.parseCSS("#ff8000")
IntRGB.DARK_ORANGE = IntRGB.parseCSS("#804000")

IntRGB.LIGHT_BROWN = IntRGB.parseCSS("#c06000")
IntRGB.BROWN = IntRGB.parseCSS("#804000")
IntRGB.DARK_BROWN = IntRGB.parseCSS("#502800")

#IntRGB.NAVY = IntRGB.DARK_BLUE
#IntRGB.AQUA = IntRGB.CYAN
#IntRGB.TEAL = IntRGB.DARK_CYAN
#IntRGB.LIME = IntRGB.GREEN
#IntRGB.FUCHSIA = IntRGB.VIOLET
#IntRGB.PURPLE = IntRGB.DARK_VIOLET
#IntRGB.OLIVE = IntRGB.DARK_YELLOW
#IntRGB.SILVER = IntRGB.LIGHT_GRAY



