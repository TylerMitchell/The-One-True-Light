import os
import sys
import random
import math
import pygame
from pygame.locals import *
import core
import states
import enginefonts
class Button():
	def __init__(self, locx, locy, w, h, text, inp, image = 0):
		if image:
			self.image = pygame.image.load(image)
		else:
			self.image = pygame.Surface( (w,h) )
			self.color = (255,0,0)
			self.image.fill( self.color )
		self.label = text
		self.rect = pygame.Rect( (locx, locy), (w, h) )
		self.posx = self.rect.topleft[0]
		self.posy = self.rect.topleft[1]
		self.font = enginefonts.SuperFont( text, 30, self.image )
		self.font.draw()
		self.input = inp
		self.inputRegistry = []
	def setColor(self, col):
		self.color = col
		self.image.fill( self.color )
	def setLabel(self, text):
		self.label = text
	def setPos(self, x, y):
		self.rect = self.rect.move( x - self.posx, y - self.posy )
		self.posx = x
		self.posy = y
	def draw(self):
		core.screen.blit( self.image, (self.posx, self.posy) )
	def assignHandler(self, callback, whichButton):
		self.inputRegistry.append( self.input.regMouseEvent( callback, whichButton, self.rect.topleft, self.rect.bottomright, self) )