#-------------------------------------------------- 
# Author: Brandon Newbright
# 
# Description: Basic Python implementation of 
# 	hexagonal grid system, for game development.
#--------------------------------------------------

import math

# Class to construct hexagonal units and store their coordinates
class Hex(object):

	# In the case of axial coordinates, s has a pre-definition
	def __init__(self, q, r, s = -q - r):
		assert (q + r + s == 0)
		self.q, self.r, self.s = q, r, s

	# Define equality parameters between two objects
	def __eq__(self, other):
		return self.q == other.q and self.r == other.r and self.s == other.s

	def __ne__(self, other):
		return !(self == other)

# Class to house mathematic functions on and between Hex() objects
class HexOps:

	# Basic functions for coordinate arithmetic
	def add(self, a, b):
		return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

	def subtract(self, a, b):
		return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

	def multiply(self, a, n):
		return Hex(a.q * n, a.r * n, a.s * n)

	# Finds the "length", in hexagonal units, from the origin Hex(0, 0, 0) to the Hex 'a'
	def length(self, a):
		return int((abs(a.q) + abs(a.r) + abs(a.s)) / 2)

	# Finds the distance between two Hex() objects 'a' and 'b'
	def distance(self, a, b):
		return length(subtract(a, b))

	# List to reference the six sides of a Hex() object to its neighbors and its coordinates' discrepancy to that of its neighbors
	hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]

	# References one of the six sides 'd' of a Hex() to its neighbors and the distance to that neighbor
	def direction(self, d):
		assert (0 <= d and d < 6)
		return hex_directions[d]

	# Gets the coordinates of the Hex() 'a' in direction 'd'  
	def neighbor(self, a, d):
		return add(a, direction(d))

	# Rounds the coordinates of a "fractional" Hex() 'a' into integers
	def hex_round(self, a):
		q = int(round(a.q))
		r = int(round(a.r))
		s = int(round(a.s))
		q_diff = abs(q - a.q)
		r_diff = abs(r - a.r)
		s_diff = abs(s - a.s)
		if q_diff > r_diff and q_diff > s_diff:
			q = -r - s
		else:
			if r_diff > s_diff:
				r = -q - s
			else:
				s = -q - r
		return Hex(q, r, s)

	# Linearly interpolates between two hexagons 'a' and 'b', where 't' is the the geometric sum (1.0/N) * i for 0 < i < N
	def hex_lerp(self, a, b, t):
		return Hex(a.q + (b.q - a.q) * t, a.r + (b.r - a.r) * t, a.s + (b.s - a.s) * t)

	# Uses linear interpolation to draw a line between the hexagons 'a' and 'b'
	def hex_linedraw(self, a, b):
		N = hex_distance(a, b)
		results = []
		step = 1.0 / max(N, 1)
		for i in range(0, N + 1):
			results.append(hex_round(hex_lerp(a, b, step * i)))
		return results

# Helper class to define the hexagonal grid's orientation
class Orientation(object):

	# Values are stored as a 2x2 forward matrix 'j', a 2x2 inverse matrix 'k', and the starting angle 'l' (in multiples of 60 degrees)
	def __init__(self, j0 = None, j1 = None, j2 = None, j3 = None, k0 = None, k1 = None, k2 = None, k3 = None, l = None):
		self.j0, self.j1, self.j2, self.j3 = j0, j1, j2, j3
		self.k0, self.k1, self.k2, self.k3 = k0, k1, k2, k3
		self.l = l

	# Builds oen of two "pre-defined" Orientation() objects: "point-top" and "flat-top". 
	def build_from_type(self, type_name):
		if type_name == "point":
			return Orientation(sqrt(3.0), sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
		if type_name == "flat":
			return Orientation(3.0 / 2.0, 0.0, sqrt(3.0) / 2.0, sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, sqrt(3.0) / 3.0, 0.0)

# Minimal class to store two-dimensional point coordinates
class Point(object):

	# Stores a pair of Cartesian coordinates. Pretty straighforward.
	def __init__(self, x, y):
		self.x, self.y = x, y

# Class to establish the layout of the hexagonal grid on-screen
class Layout(object):

	# Values are an Orientation() 'orientation', a Point() 'size', and a Point() 'origin'
	def __init__(self, orientation, size, origin):
		self.orientation = orientation
		self.size = size
		self.origin = origin

	# Finds the pixel representation of a given hexagon
	def hex_to_pixel(self, hexagon):
		x = (self.orientation.f0 * hexagon.q + self.orientation.f1 * hexagon.r) * self.size.x
		y = (self.orientation.f2 * hexagon.q + self.orientation.f3 * hexagon.r) * self.size.y
		return Point(x + self.origin.x, y + self.origin.y)

	# Finds the hexagon at a given pixel
	def pixel_to_hex(self, point):
		pt = Point((point.x - self.origin.x) / self.size.x, (point.y - self.origin.y) / self.size.y)
		q = self.orientation.b0 * pt.x + self.orientation.b1 * pt.y
		r = self.orientation.b2 * pt.x + self.orientation.b3 * pt.y
		return Hex(q, r, -q - r)

	# Finds the vector location of a hexagon's corner at "corner" degrees, relative to the hexagon's center
	def hex_corner_offset(self, corner):
		angle = 2.0 * math.pi * (corner + self.orientation.l) / 6
		return Point(self.size.x * cos(angle), self.size.y * sin(angle))

	# Finds the vector locations of all six corners of a hexagon
	def polygon_corners(self, hexagon):
		corners = []
		center = self.hex_to_pixel(hexagon)
		for i in range(0, 6):
			offset = hex_corner_offset(i)
			corners.append(Point(center.x + offset.x, center.y + offset.y))
		return corners