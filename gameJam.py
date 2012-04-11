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
import vector
# THE ONE TRUE LIGHT!!!
# play swat animation on collision ---- setup but not QUITE working
# display background tiles.

class Candle():
	def __init__(self, images, window):
		self.windowTuple = window # (leftx rightx, depth)
		self.posx = random.randint( self.windowTuple[0], self.windowTuple[1]  - 48 )
		self.posy = self.windowTuple[2] - 75
		self.isLit = True
		self.images = images # lit, unlit
	def draw(self):
		if self.isLit:
			core.screen.blit( self.images[0], ( self.posx, self.posy ) )
		else:
			core.screen.blit( self.images[1], ( self.posx, self.posy ) )
class MapTile():
	def __init__(self, image):
		self.image = image
class Wind():
	def __init__(self, image):
		self.posx = core.screen.get_width()/2
		self.posy = core.screen.get_height()/2
		self.dx   = 0
		self.dy   = 0
		self.vec  = vector.Vector(self.dx, self.dy)
		self.speed = 1
		self.variance = 3
		self.image = image
		self.rect = self.image.get_rect()
		self.startUp()
	def draw(self):
		core.screen.blit( self.image, ( self.posx, self.posy ) )
	def startUp(self):
		screenSide = random.randint(1,4) # 1. top 2. bottom 3. left 4. right
		#if screenSide   == 1: #top
		#	self.posx = random.randint( 50, core.screen.get_width()- 114 )
		#elif screenSide == 2: #bottom
		#	self.posy = core.screen.get_height() - 48
		#	self.posx = random.randint( 50, core.screen.get_width()- 114 )
		#elif screenSide == 3: #left
		#	self.posy = random.randint( 50, core.screen.get_height()- 98 )
		#elif screenSide == 4: #right
		#	self.posx = core.screen.get_width() - 64
		#	self.posy = random.randint( 50, core.screen.get_height()- 98 )
		self.rect.move_ip( self.posx, self.posy )
		self.initialDirection( screenSide )
	def initialDirection( self, screenSide ):
		negvar = -1*self.variance
		#if screenSide == 1: #top
		#	self.dx = random.randint(negvar, self.variance)
		#	self.dy = random.randint(0, self.variance)
		#elif screenSide == 2: #bottom
		#	self.dx = random.randint(negvar, self.variance)
		#	self.dy = random.randint(negvar, 0)
		#elif screenSide == 3: #left
		#	self.dx = random.randint(0, self.variance)
		#	self.dy = random.randint(negvar, self.variance)
		#elif screenSide == 4: #right
		#	self.dx = random.randint(negvar, 0)
		#	self.dy = random.randint(negvar, self.variance)
		self.dx = random.randint( negvar, self.variance )
		self.dy = random.randint( negvar, self.variance )
		self.vec = vector.Vector( self.dx, self.dy )
	def changeDirection(self, angle, vec):
		self.dx = vec.dx
		self.dy = vec.dy
	def move(self):
		self.posx += round(self.dx*self.speed)
		self.posy += round(self.dy*self.speed)
		self.rect.move_ip( round(self.dx*self.speed), round(self.dy*self.speed) )
	def collideHand(self, hand):
		if hand.rect.colliderect( self.rect ):
			return True
		return False
	def collideCandle(self, candle):
		cpx = candle.posx + 10
		cpy = candle.posy + 8
		wpx = self.rect.centerx-20
		wpy = self.rect.centery-15
		if math.sqrt( ( cpx - (wpx + 32) )**2 + ( cpy - (wpy + 24) )**2 ) < 12:
			return True
		if math.sqrt( ( cpx - (wpx + 32) )**2 + ( cpy - (wpy - 24) )**2 ) < 12:
			return True
		if math.sqrt( ( cpx - (wpx - 32) )**2 + ( cpy - (wpy + 24) )**2 ) < 12:
			return True
		if math.sqrt( ( cpx - (wpx - 32) )**2 + ( cpy - (wpy - 24) )**2 ) < 12:
			return True
		if math.sqrt( ( cpx - (wpx - 32) )**2 + ( cpy - (wpy - 24) )**2 ) < 12:
			return True
		return False
	def isInScreen(self): #if wind goes offscreen, check if all candles are out, if not then level fail
		if self.posx < core.screen.get_width() and self.posx > -64:
			if self.posy < core.screen.get_height() and self.posy > -48:
				return True
		return False
class Hand():
	def __init__(self, images, inp, firstHand = True):
		self.images = images # the hand image should follow the mouse around the screen
		self.tempImage = self.images[0]
		self.rect = self.images[0].get_rect()
		self.animCount = 0
		self.posx = 0 
		self.posy = 0
		self.angle = 0
		self.rotation = 0
		self.doAnimate = False
		self.input = inp
		self.vec = vector.Vector( -1, 2 )
		self.tempVec = vector.Vector( 0, 1 )
		pygame.mouse.set_visible(False)
		self.input.regKeyEvent( self.setRotate ,K_z , self, 1, 0) # callback, key, object
		self.input.regKeyEvent( self.setRotate ,K_x , self, -1, 0) # callback, key, object
		self.input.motionListen( self.followMouse )
		self.rotate()
	def followMouse(self, mousePos):
		oldx = self.posx
		oldy = self.posy
		self.posx = mousePos[0] - 37
		self.posy = mousePos[1] - 36
		self.rect.move_ip( self.posx - oldx, self.posy - oldy )
	def setRotate( self, obj, value ):
		self.rotation = value
	def rotate( self ):
		if self.rotation > 0 or self.rotation < 0:
			self.angle += self.rotation
			if self.doAnimate:
				pass
			else:
				self.tempImage = pygame.transform.rotate( self.images[0], self.angle )
			self.rect = self.images[0].get_rect()
			self.rect.move_ip( self.posx, self.posy )
			self.tempVec = self.vec.rotate(self.angle)
	def animate(self): #rotate each sprite properly, display sequence 1,2,3 5frames per image
		self.doAnimate = True
		self.animCount += 1
		if self.animCount < 6:
			self.tempImage = pygame.transform.rotate( self.images[1], self.angle )
		if self.animCount < 11:
			self.tempImage = pygame.transform.rotate( self.images[2], self.angle )
		if self.animCount < 16:
			self.tempImage = pygame.transform.rotate( self.images[3], self.angle )
		if self.animCount == 16:
			self.animCount = 0
			self.doAnimate = False
	def draw(self):
		if self.doAnimate:
			self.animate()
		core.screen.blit( self.tempImage, ( self.posx, self.posy ) )
class Window():
	def __init__(self, px, py, image):
		self.posx = px
		self.posy = py
		self.image = image
	def draw(self):
		core.screen.blit( self.image, (self.posx, self.posy) )
class GameScreen():
	def __init__(self):
		self.input = input.Input()
		self.candles = []
		self.handImages = []
		self.windows = []
		self.level = 1
		self.numCandles = 1
		self.isInstr = True
		self.score = 0
		msg = "Level: " + str(self.level) + " Score: " + str(self.score)
		self.font = enginefonts.SuperFont( msg, 25, core.screen )
		self.loadSprites()
		self.wind = self.generateWind()
		self.hand = self.generateHand()
		self.bgimg = pygame.image.load( "Sprites\gamebg.png" )
		self.failbg = pygame.image.load( "Sprites\lightsout.png" )
		self.instructions = pygame.image.load("Sprites\instructions.png")
		self.generateWindows()
		self.generateCandles()
	def loadSprites(self):
		self.handImages.append( pygame.image.load( "Sprites\goodhand1.png" ) )
		self.handImages.append( pygame.image.load( "Sprites\goodhand2.png" ) )
		self.handImages.append( pygame.image.load( "Sprites\goodhand3.png" ) )
		self.handImages.append( pygame.image.load( "Sprites\goodhand4.png" ) )
	def gameScreen(self, stateManager, state):
		self.input.regKeyEvent( self.showInstructions, K_s, self, 1, 0)# callback key object downval upval 
		while self.isInstr:
			self.input.handleEvents( pygame.event.get(), stateManager )
			core.screen.blit( self.instructions, (0,0) )
			core.game.renderFrame()
		self.stateManager = stateManager
		self.input.handleEvents( pygame.event.get(), stateManager )
		self.gameLogic()
		self.drawScreen()
		core.game.renderFrame()
	def showInstructions(self, obj, downVal):
		self.isInstr = False
		self.input.unregKeyEvent( K_s)
	def generateWind(self):
		return Wind( pygame.image.load("Sprites\wind.png") )
	def generateCandles(self):
		candleImages = []
		candleImages.append( pygame.image.load("Sprites\candle1.png") )
		candleImages.append( pygame.image.load("Sprites\candle2.png") )
		for i in range( self.numCandles ):
			rnd = random.randint( 0, len(self.windows)-1 )
			target = self.windows[rnd]
			self.candles.append( Candle( candleImages, (target.posx, target.posx+94, target.posy+114) ) ) # upadate this if more sprites are added to self.images
	def generateWindows(self):
		window = pygame.image.load( "Sprites\window.png" ) # 16, 10
		spacing = (26, 20)
		for j in range(5):
			self.windows.append( Window( spacing[0]*(j+1) + 95*j, spacing[1], window ) )
			self.windows.append( Window( spacing[0]*(j+1) + 95*j, spacing[1] + 125, window ) )
			self.windows.append( Window( spacing[0]*(j+1) + 95*j, spacing[1] + 250, window ) )
	def generateHand(self):
		return Hand( self.handImages, self.input, False )
	def levelUp(self):
		for i in range(len(self.candles)):
			self.candles.pop()
		self.level += 1
		self.numCandles += 2
		self.generateCandles()
		self.generateWind()
	def checkCandles(self):
		for candle in self.candles: # return False if there is a lit candle, True otherwise
			if candle.isLit:
				return False
		return True
	def testCollisions(self):
		#print len(self.candles)
		for candle in self.candles:
			if self.wind.collideCandle( candle ) and candle.isLit:
				candle.isLit = False
				if self.checkCandles():
					self.levelUp()
		if self.wind.collideHand( self.hand ) and not self.hand.doAnimate:
			self.hand.animate()
			self.wind.changeDirection( self.hand.angle, self.hand.tempVec )
		#print self.hand.rect , " " , self.wind.rect
	def levelFail(self):
		msg =  " the followers of The Serpent Flame have won!!!"
		deadFont = enginefonts.SuperFont( msg, 30, self.failbg, core.screen.get_width()/10, (core.screen.get_height()/10)*7 )
		deadFont.draw()
		quit = gui.Button( 150, 400, 100, 50, "", self.input, "quit.png" )
		start = gui.Button( 350, 400, 100, 50, "", self.input, "play.png" )
		start.assignHandler( self.clickStart, core.LEFTMOUSEBUTTON )
		quit.assignHandler( self.clickQuit, core.LEFTMOUSEBUTTON )
		self.loopif = True
		while self.loopif:
			core.screen.blit( self.failbg, ( 0, 0 ) )
			start.draw()
			quit.draw()
			self.hand.draw()
			core.game.renderFrame()
			self.input.handleEvents( pygame.event.get(), self.stateManager )
	def clickStart( self, object, mousePosition ):
		self.loopif = False
		self.stateManager.pop()
		gameScreen = GameScreen()
		core.game.newState( gameScreen.gameScreen )
	def clickQuit( self, object, mousePosition ):
		sys.exit( 1 )
	def checkSuccess(self):
		for candle in self.candles:
			if candle.isLit:
				self.levelFail()
	def gameLogic(self): # check if wind collides with hand, check if wind collides with candles, check if all candles are out, chek if wind is in screen
		self.wind.move()
		self.hand.rotate()
		if self.wind.isInScreen():
			self.testCollisions()
		else:
			self.checkSuccess()
	def drawBackground(self):
		core.screen.blit( self.bgimg, (0,0) )
	def drawScreen(self):
		core.screen.fill( (0,0,0) )
		self.drawBackground()
		for window in self.windows:
			window.draw()
		self.wind.draw()
		self.font.draw()
		#hackysac = pygame.Surface( (40, 40) )
		#hackysac.fill( (0,0,255) )
		#core.screen.blit(hackysac, (self.wind.rect.centerx-20, self.wind.rect.centery-15) )
		for candle in self.candles:
			candle.draw()
			#hackysac = pygame.Surface( (20, 20) )
			#hackysac.fill( (0,0,255) )
			#core.screen.blit(hackysac, (candle.posx+10, candle.posy+8) )
		self.hand.draw()
class MainMenu():
	def __init__(self):
		self.input = input.Input()
		self.quit = gui.Button( 50, 360, 100, 50, "", self.input, "quit.png" )
		self.start = gui.Button( 50, 150, 100, 50, "", self.input, "play.png" )
		self.options = gui.Button( 50, 290, 100, 50, "", self.input, "options.png" )
		self.credits = gui.Button( 50, 220, 100, 50, "", self.input, "credits.png" )
		self.start.assignHandler( self.clickStart, core.LEFTMOUSEBUTTON )
		self.quit.assignHandler( self.clickQuit, core.LEFTMOUSEBUTTON )
		self.credits.assignHandler( self.clickCredits, core.LEFTMOUSEBUTTON )
		self.options.assignHandler( self.clickOptions, core.LEFTMOUSEBUTTON )
		self.bgimg = pygame.image.load( "menubg.png" )
		self.bgimg = pygame.transform.scale( self.bgimg, (640, 480) )
	def mainMenu(self, stateManager, state):
		self.stateManager = stateManager
		self.state = state
		self.input.handleEvents( pygame.event.get(), stateManager )
		self.drawScreen()
		core.game.renderFrame()
	def clickStart( self, object, mousePosition ):
		gameScreen = GameScreen()
		core.game.newState( gameScreen.gameScreen )
	def clickQuit( self, object, mousePosition ):
		sys.exit( 1 )
	def clickCredits( self, object, mousePosition ):
		core.screen.fill( (0,0,0) )
		programmer = "Programmer: Tyler"
		nick = "Artists: Nick, CMac, Kevin, PMac" # credit nick with music
		font1 = enginefonts.SuperFont( programmer, 30, core.screen, 50, 150)
		font2 = enginefonts.SuperFont( nick, 30, core.screen, 50, 250)
		font3 = enginefonts.SuperFont( "Press the \"b\" key to return to the menu", 30, core.screen, 50, 350)
		self.drawBackground()
		font1.draw()
		font2.draw()
		font3.draw()
		while True:
			self.input.handleEvents( pygame.event.get(), self.stateManager )
			self.input.regKeyEvent( self.backToMenu, K_b, self, K_b, 0)
			core.game.renderFrame()
	def backToMenu(self, object, downVal):
		self.input.unregKeyEvent( downVal )
		self.mainMenu( self.stateManager, self.state )
	def clickOptions( self, object, mousePosition ):
		font1 = enginefonts.SuperFont( "The Are NO OPTIONS!!!", 50, core.screen, 50, 150)
		font2 = enginefonts.SuperFont( "Press the \"b\" key to return to the menu", 30, core.screen, 50, 250)
		self.drawBackground()
		font1.draw()
		font2.draw()
		while True:
			self.input.handleEvents( pygame.event.get(), self.stateManager )
			self.input.regKeyEvent( self.backToMenu, K_b, self, K_b, 0)
			core.game.renderFrame()
	def drawBackground(self):
		core.screen.blit( self.bgimg, (0,0) )
	def drawScreen(self): # this eventually needs to be turned into a render subsystem
		core.screen.fill( (0,0,0) )
		self.drawBackground()
		self.quit.draw()
		self.start.draw()
		self.options.draw()
		self.credits.draw()
def playMovie(): #woot woot
	image = pygame.image.load( "grouplogo.jpg" )
	image = pygame.transform.scale( image, (400, 400) )
	core.screen.blit( image, (120, 40) )
	core.game.renderFrame()
	pygame.time.wait(1000)
	pygame.mixer.quit()
	movie = pygame.movie.Movie( "candlemovie.mpg" )
	movie.set_display( core.screen )
	movie.play()
	while movie.get_busy():
		pass
def main():
	core.engineInit( "THE ONE TRUE LIGHT!!!", 640, 480)
	playMovie()
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
