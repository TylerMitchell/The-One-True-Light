import os
import sys
import random
import math
import pygame
from pygame.locals import *
import states
import input
import gui
import enginefonts
import vector
class State():
	def __init__(self, callback):
		self.stateCallback = callback
class StateManager():
	def __init__(self):
		self.stateStack = []
	def push(self, state):
		self.stateStack.append(state)
	def pop(self):
		return self.stateStack.pop()
	def popAll(self):
		pass
	def doState(self):
		temp = self.stateStack[len(self.stateStack)-1 ]
		temp.stateCallback(self, temp)
class Game():
	def __init__(self):
		pauseState = State( states.pauseGame )
		self.stateManager = StateManager()
	def doState(self):
		self.stateManager.doState()
	def drawScreen(self): # this eventually needs to be turned into a render subsystem
		pass
	def newState(self, callback):
		self.stateManager.push( State(callback) )
	def lastState(self):
		self.stateManager.pop()
	def renderFrame(self):
		pygame.display.flip()
def engineInit( gameName, sizeX, sizeY, isResizeable = 0 ): #changed during Game Jam
	pygame.init()
	global LEFTMOUSEBUTTON
	global RIGHTMOUSEBUTTON
	global screen
	global initVector
	initVector = vector.Vector( 1, 0, 0 )
	LEFTMOUSEBUTTON = 0
	RIGHTMOUSEBUTTON = 1
	if isResizeable:
		screen = pygame.display.set_mode( ( sizeX, sizeY ), RESIZABLE)
	else:
		screen = pygame.display.set_mode( ( sizeX, sizeY ) )
	pygame.display.set_caption( gameName)
	global game
	game = Game()