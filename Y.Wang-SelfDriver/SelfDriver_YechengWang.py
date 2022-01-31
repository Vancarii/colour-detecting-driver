# ~ Yecheng Wang
# ~ Self Driver Pixel Collision Assignment
# ~ May 5th 2020

import math, random, sys
import pygame
from pygame.locals import *
from PIL import Image

# initialise display
pygame.init()
W, H = 800, 600
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Self Driver")
FPS = 120
Black = (0,0,0)
White = (255, 255, 255)

class car:
	def __init__(self):
		self.x = 120
		self.y = 300
		self.speed = 1
		self.direction = 0
		self.image = pygame.image.load('Car.png')
		rect = self.image.get_rect()
	
	def move(self, NextCoordinates):
		self.x = NextCoordinates[0]
		self.y = NextCoordinates[-1]
		rotated = pygame.transform.rotate(self.image, self.direction)
		rect = rotated.get_rect()
		rect.center = (self.x, self.y)
		screen.blit(rotated, rect)

	def turn(self, Coordinates, NextCoordinates):
		# ~ this function lets the car rotate in the direction it is going
		# ~ NextCoordinates is a few coordinates in front 
		# ~ Find distance between the next coordinate and the current
		# ~ find the angle and put it into the direction of the car
		Coordinates_x = Coordinates[0]
		Coordinates_y = Coordinates[-1]
		NextCoordinates_x = NextCoordinates[0]
		NextCoordinates_y = NextCoordinates[-1]
		distance_x = NextCoordinates_x - Coordinates_x
		distance_y = NextCoordinates_y - Coordinates_y
		
		if distance_x == 0:
			if NextCoordinates_y > Coordinates_y:
				self.direction = 0
			elif NextCoordinates_y < Coordinates_y:
				self.direction = 180
		elif distance_y == 0:
			if NextCoordinates_x > Coordinates_x:
				self.direction = 90
			elif NextCoordinates_x < Coordinates_x:
				self.direction = 270
		else:
			angle = (math.degrees(math.atan(distance_y / distance_x)))
			if distance_x > 0:
				self.direction = 90 - angle
			elif distance_x < 0:
				self.direction = - (90 + angle)

# ~ This function takes the CollisionMap image and makes the black parts transparent
# ~ so that in the get_outline function, it can mask the inner white area
# ~ The new image with a transparent background is then stored in NewMap
def getnewmap(CollisionMap):
    datas = CollisionMap.getdata()
    NewMapData = []
    for item in datas:
	    if item[0] == 0 and item[1] == 0 and item[2] == 0:
		    NewMapData.append((0, 0, 0, 0))
	    elif item[0] != 255 and item[1] != 255 and item[2] != 255:
		    NewMapData.append((0, 0, 0, 0))
	    else:
		    NewMapData.append(item)
    CollisionMap.putdata(NewMapData)
    CollisionMap.save("NewMap.png", "PNG")
    
# ~ This function takes the Newmap created above and finds the coordinates of the outline 
# ~ This way we have a list of coordinates for the car to follow
def get_outline(NewMap, color=(255,255,255), threshold=127):
    NewMap_mask = pygame.mask.from_surface(NewMap)
    outline_map = pygame.Surface(NewMap.get_size()).convert_alpha()
    outline_map.fill((0,0,0,0))
    for point in NewMap_mask.outline():
	    outline_map.set_at(point,color)
	    Coordinates.append(point)	    
    return outline_map
  
track = pygame.image.load('trackBG.jpg')
CollisionMap = Image.open('CollisionMap2.jpg')
CollisionMap = CollisionMap.convert("RGBA") 
 
getnewmap(CollisionMap)
NewMap = pygame.image.load('NewMap.png')
    
Car = car()

Coordinates = []

mask_location = get_outline(NewMap)
NewMap_rect = NewMap.get_rect()
mask_location_rect = mask_location.get_rect()

NextCoordinates = Coordinates[0]

i=0
gap = 35

# ~ Text Prompt
font = pygame.font.Font('freesansbold.ttf', 18) 
Prompt1 = font.render('Press the UP arrow key to increase the speed of the car', True, Black) 
Prompt1_rect = Prompt1.get_rect()  
Prompt1_rect.center = (410, H // 2) 

Prompt2 = font.render('Press the DOWN arrow key to decrease the speed of the car', True, Black)
Prompt2_rect = Prompt2.get_rect()
Prompt2_rect.center = (410, 320)


# main loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == K_UP:
			Car.speed += 1
		elif event.type == KEYDOWN and event.key == K_DOWN:
			if Car.speed > 1:
				Car.speed -= 1
	
	# ~ This is to loop the list of coordinates 
	# ~ So that the car can keep making laps around the track
	# ~ Since the NextCoordinates are in front in the current coordinates,
	# ~ we need to ensure the loop doesn't go out of range
	j = len(Coordinates) - i
	if i <= len(Coordinates):
		if j <= gap:
			
			NextCoordinates = Coordinates[gap-j-1]
			if i == len(Coordinates):
				i = 0
		else:
			NextCoordinates = Coordinates[i+gap]
	else:
		i = 0
	    
	screen.blit(mask_location, mask_location_rect)
	screen.blit(track,(0,0))
	screen.blit(Prompt1, Prompt1_rect)
	screen.blit(Prompt2, Prompt2_rect)
	
	Car.move(NextCoordinates)
	Car.turn(Coordinates[i], NextCoordinates)
	
	i += Car.speed
	pygame.display.update()
	CLOCK.tick(FPS)
