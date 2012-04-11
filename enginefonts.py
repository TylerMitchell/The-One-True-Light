import os
import sys
import random
import math
import pygame
from pygame.locals import *
import core
import states
class SuperFont():
	def __init__(self, msg, s, surf, x = 0, y = 0, col = (0,255,0), styl = None):
		self.font = pygame.font.Font(styl, s) 
		self.surface = surf
		self.style = styl
		self.size = s
		self.color = col
		self.msgfont = self.font.render( msg , 1, col)
		self.msgpos = self.msgfont.get_rect( topleft = (x, y) )
	def draw(self):
		self.surface.blit( self.msgfont, self.msgpos )
	def resize(self, s):
		self.size = s
		self.font = pygame.font.Font(self.style, s)
		self.msgfont = self.font.render( msg , 1, self.color )
	def setStyle(self, styl):
		self.style = styl
		self.font = pygame.font.Font(styl, self.size)
		self.msgfont = self.font.render( msg , 1, self.color )
	def setColor(self, col):
		self.color = col
		self.msgfont = self.font.render( msg , 1, col )
	def move(self, dx, dy):
		self.msgpos.move( dx, dy )