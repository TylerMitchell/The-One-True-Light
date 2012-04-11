import os
import sys
import random
import math
import pygame
from pygame.locals import *
import core
import states
def pauseGame(stateManager, state):
	print "currently paused"
	loopIf = True
	while loopIf:
		events = pygame.event.get()
		for event in events:
			if event.type == KEYDOWN:
				if event.key == K_p:
					stateManager.pop()
					loopIf = False