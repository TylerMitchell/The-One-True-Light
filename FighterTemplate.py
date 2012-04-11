import os
import sys
import random
import math
import pygame
from pygame.locals import *
import core
import states
import input
import gui
import enginefonts

# moves                  { (move left), (move right), (jump), (Hard Punch), (Soft Punch), (Hard Kick), (Soft Hick), (Block), (Fireball), (Uppercut), (Roundhouse), (crouch), }
# input delay            { (0)        , (0)         , (2)   , (15)        , (7)         , (20)       ,  (10)      , (0)    , (30)      , (25)      , (30)        , (0)} AKA Frame Penalty
# Damage (based on 1000) { (0)        , (0)         , (0)   , (85)        , (60)        , (100)      ,  (75)      , (0)    , (120)     , (100)      , (120)      , (0)}
# states { (Stunned), (Normal) }
class Vector():
	def __init__():
		pass
class Fighter():
	def __init__(self, isAI, inp):
		self.hitPoints = 1000
		self.isAI = isAI
		self.input = inp
		self.input.regKeyEvent( self.moveRight, K_RIGHT, self)
		self.input.regKeyEvent( self.moveLeft, K_LEFT, self)
		self.image = pygame.Surface( (32, 64) )
		self.image.fill( (0, 255, 0) )
		self.dx = 0
		self.dy = 0
		self.posx = core.screen.get_width()/2
		self.posy = core.screen.get_height()-100
	def hardPunch(self):
		pass
	def softPunch(self):
		pass
	def hardKick(self):
		pass
	def softKick(self):
		pass
	def fireball(self):
		pass
	def uppercut(self):
		pass
	def roundhouse(self):
		pass
	def crouch(self):
		pass
	def jump(self):
		pass
	def block(self):
		pass
	def moveRight(self, obj):
		print "WTF"
		self.dx = 4
	def moveLeft(self, obj):
		self.dx = -4
	def updatePosition(self):
		self.posx += self.dx
		self.posy += self.dy
	def draw(self):
		core.screen.blit( self.image, (self.posx, self.posy) )
class Tiler():
	pass
class Tile():
	pass
class SuperSprite(pygame.sprite.Sprite):
	def __init__(self):
		pass
class GameScreen():
	def __init__(self):
		self.input = input.Input()
		self.player1 = Fighter( 0, self.input )
		self.player2 = Fighter( 1, self.input )
	def gameScreen(self, stateManager, state):
		self.input.handleEvents( pygame.event.get(), stateManager )
		self.player1.updatePosition()
		self.drawScreen()
		core.game.renderFrame()
	def drawScreen(self):
		core.screen.fill( (0,0,0) )
		self.player1.draw()
class MainMenu(): #define a class that will control a state
	def __init__(self):
		self.input = input.Input()
		self.quit = gui.Button( 50, 150, 100, 50, "quit", self.input )
		self.start = gui.Button( 50, 50, 100, 50, "start", self.input )
		self.start.assignHandler( self.clickStart, core.LEFTMOUSEBUTTON )
		self.quit.assignHandler( self.clickQuit, core.LEFTMOUSEBUTTON )
	def mainMenu(self, stateManager, state):
		self.input.handleEvents( pygame.event.get(), stateManager )
		self.drawScreen()
		core.game.renderFrame()
	def clickStart( self, object, mousePosition ):
		gameScreen = GameScreen()
		core.game.newState( gameScreen.gameScreen )
	def clickQuit( self, object, mousePosition ):
		sys.exit( 1 )
	def drawScreen(self): # this eventually needs to be turned into a render subsystem
		core.screen.fill( (0,0,0) )
		self.quit.draw()
		self.start.draw()
def main():
	core.engineInit()
	menu = MainMenu()
	mainState = core.State(menu.mainMenu)
	core.game.stateManager.push(mainState)#don't forget to push the main state onto the stack
	totalseconds = pygame.time.get_ticks() # confusing implementation of framerate control, make prettier
	while True:
		currenttime = pygame.time.get_ticks()
		if currenttime - totalseconds > 17:
			totalseconds = currenttime
			core.game.doState()
if __name__ == "__main__": main()