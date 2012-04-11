import core
import math

class Vector():
	def __init__(self, dx, dy, notInit = 1):
		self.dx = dx
		self.dy = dy
		if notInit :
			self.initAngle = self.angleFromInitial()
	def angleFromInitial(self):
		dotP = self.dotProduct( core.initVector )
		mag1 = self.magnetude( self )
		mag2 = self.magnetude( core.initVector )
		div = mag1*mag2
		if div:
			return math.cos(dotP/div)
		else:
			return 0
	def findAngle( self, vec2 ):
		print self.dx , " ", self.dy, " ", vec2.dx, " ", vec2.dy
		dotP = self.dotProduct( vec2 )
		mag1 = self.magnetude( self )
		mag2 = self.magnetude( vec2 )
		div = mag1*mag2
		if div:
			return math.cos(dotP/div)
		else:
			return 0
	def dotProduct( self, vec):
		newx = self.dx*vec.dx
		newy = self.dy*vec.dy
		return (newx + newy)
	def magnetude( self, vec ):
		return math.sqrt( self.dx**2 + self.dy**2 )
	def rotate( self, angle ):
		radians = (math.pi / 180) * angle
		tdy = self.dy
		tdx = self.dx
		retx = tdx * math.cos( radians ) - tdy * math.sin( radians )
		rety = tdx * math.sin( radians ) + tdy * math.cos( radians )
		#self.dy *= -1
		return Vector(retx,rety)
	def flip( self ):
		self.dx *= -1
		self.dy *= -1