import os
import sys
import random
import math
import pygame
from pygame.locals import *
import core
import states
class MouseCallback():
	def __init__(self, cb, minX, maxX, minY, maxY, obj):
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		self.callback = cb
		self.object = obj
class Input():
	def __init__(self):
		self.lookup = []
		self.mouseLeftButton = []
		self.mouseRightButton = []
		self.listenMotion = False
		#self.motionCallback = 0
	def regKeyEvent(self, callback, key, obj, downVal, upVal):
		self.lookup.append( ( key, callback, obj, downVal, upVal ) )
	def unregKeyEvent(self, key):
		for event in self.lookup:
			if event[0] == key:
				self.lookup.remove( event )
	def motionListen( self, callback ):
		self.listenMotion = True
		self.motionCallback = callback
	def regMouseEvent(self, callb, buttonType, topLeft, bottomRight, obj):
		if buttonType == 0:
			callback = MouseCallback( callb, topLeft[0], bottomRight[0], topLeft[1], bottomRight[1], obj )
			self.mouseLeftButton.append( callback )
			return len(self.mouseLeftButton)-1
		if buttonType == 1:
			callback = MouseCallback( callb, topLeft[0], bottomRight[0], topLeft[1], bottomRight[1], obj )
			self.mouseRightButton.append( callback )
			return len(self.mouseRightButton)-1
	def unregMouseEvent(self, callb):
		pass
	def searchLeftMouse(self, mousePosition):
		for mouseAction in self.mouseLeftButton:
			if mouseAction.minX <= mousePosition[0] and mousePosition[0] <= mouseAction.maxX:
				if mouseAction.minY <= mousePosition[1] and mousePosition[1] <= mouseAction.maxY:
					mouseAction.callback( mouseAction.object, mousePosition )
	def searchRightMouse(self, mousePosition):
		for mouseAction in self.mouseRightButton:
			if mouseAction.minX <= mousePosition[0] and mousePosition[0] <= mouseAction.maxX:
				if mouseAction.minY <= mousePosition[1] and mousePosition[1] <= mouseAction.maxY:
					mouseAction.callback( mouseAction.object, mousePosition )
	def handleEvents(self, events, stateManager):
		for event in events:
			if event.type == QUIT:
				sys.exit( 1 )
			if event.type == VIDEORESIZE:
				core.screen = pygame.display.set_mode(event.size, RESIZABLE)
			if event.type == KEYDOWN:
				if event.key == K_p:
					stateManager.push( core.State( states.pauseGame ) )
				for iter in self.lookup:
					if event.key == iter[0]:
						iter[1](iter[2], iter[3])
			if event.type == KEYUP:
				for iter in self.lookup:
					if event.key == iter[0]:
						iter[1](iter[2], iter[4])
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.searchLeftMouse( event.pos )
				if event.button == 3:
					self.searchRightMouse( event.pos )
			if self.listenMotion:
				if event.type == MOUSEMOTION:
					self.motionCallback( event.pos )