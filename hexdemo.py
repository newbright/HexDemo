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

# Minimal class to store two-dimensional point coordinates
class Point(object):

	# Stores a pair of Cartesian coordinates. Pretty straighforward.
	def __init__(self, x, y):
		self.x, self.y = x, y

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

# Class to establish the layout of the hexagonal grid on-screen
class Layout(object):

	# Values are an Orientation() 'orientation', a Point() 'size', and a Point() 'origin'
	def __init__(self, orientation, size, origin):
		self.orientation = orientation
		self.size = size
		self.origin = origin
