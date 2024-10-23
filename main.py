import pygame
import os

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

print(joystick_count)

if joystick_count > 0:
	joystick=pygame.joystick.Joystick(0)

running = False

with open("test.txt", "w") as file:
	file.write("Hello world!")

while running:
	for event in pygame.event.get():
		if event.type == pygame.JOYBUTTONDOWN:
			print(f"Button {event.button} pressed")
		if event.type == pygame.JOYAXISMOTION:
			print(f"Axis {event.axis} moved to {event.value}")
		if event.type == pygame.JOYHATMOTION:
			print(f"Axis {event.value}")
#		print(event)
