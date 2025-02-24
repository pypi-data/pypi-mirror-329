

__slots__ = (
	"parseCSS_toARGB",
	"parseCSS_to3Ints",
)


import typing
import re






_HEXVALS = "0123456789abcdef"
_P1 = re.compile(r"^#([0-9a-f][0-9a-f])([0-9a-f][0-9a-f])([0-9a-f][0-9a-f])$")
_P2 = re.compile(r"^#([0-9a-f])([0-9a-f])([0-9a-f])$")
_P3 = re.compile(r"^rgb\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$")







def parseCSS_toARGB(cssStr:str) -> int:
	assert isinstance(cssStr, str)

	cssStr = cssStr.lower()
	m = _P1.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = (_HEXVALS.index(sr[0]) << 4) + _HEXVALS.index(sr[1])
		g = (_HEXVALS.index(sg[0]) << 4) + _HEXVALS.index(sg[1])
		b = (_HEXVALS.index(sb[0]) << 4) + _HEXVALS.index(sb[1])
		return 0xff000000 | ((((r << 8) + g) << 8) + b)
	m = _P2.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = _HEXVALS.index(sr)
		g = _HEXVALS.index(sg)
		b = _HEXVALS.index(sb)
		return 0xff000000 | ((((((((((r << 4) + r) << 4) + g) << 4) + g) << 4) + b) << 4) + b)
	m = _P3.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = int(sr)
		if r > 255:
			raise Exception("Invalid red component in: " + repr(cssStr))
		g = int(sg)
		if g > 255:
			raise Exception("Invalid green component in: " + repr(cssStr))
		b = int(sb)
		if b > 255:
			raise Exception("Invalid blue component in: " + repr(cssStr))
		return 0xff000000 | ((((r << 8) + g) << 8) + b)
	raise Exception("Not a CSS color string: " + repr(cssStr))
#



def parseCSS_to3Ints(cssStr:str) -> typing.Tuple[int,int,int]:
	assert isinstance(cssStr, str)

	cssStr = cssStr.lower()
	m = _P1.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = (_HEXVALS.index(sr[0]) << 4) + _HEXVALS.index(sr[1])
		g = (_HEXVALS.index(sg[0]) << 4) + _HEXVALS.index(sg[1])
		b = (_HEXVALS.index(sb[0]) << 4) + _HEXVALS.index(sb[1])
		return (r, g, b)
	m = _P2.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = _HEXVALS.index(sr)
		g = _HEXVALS.index(sg)
		b = _HEXVALS.index(sb)
		return ((r << 4) + r, (g << 4) + g, (b << 4) + b)
	m = _P3.match(cssStr)
	if m:
		sr = m.group(1)
		sg = m.group(2)
		sb = m.group(3)
		r = int(sr)
		if r > 255:
			raise Exception("Invalid red component in: " + repr(cssStr))
		g = int(sg)
		if g > 255:
			raise Exception("Invalid green component in: " + repr(cssStr))
		b = int(sb)
		if b > 255:
			raise Exception("Invalid blue component in: " + repr(cssStr))
		return (r, g, b)
	raise Exception("Not a CSS color string: " + repr(cssStr))
#


