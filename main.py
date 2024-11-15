import pygame
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# GPIO.output(pinNum, GPIO.HIGH)

## setting the pins
pin1 = 0 #represents leftmost digit
pin2 = 5
pin3 = 6
pin4 = 13 #rightmost digit

signalPins = [25, 19]

## signal pins
for pin in signalPins:
	GPIO.setup(pin, GPIO.OUT)

def setSignals(setting):
	for i in signalPins:
		GPIO.output(i, setting)

## command pins
commandPins = [pin1, pin2, pin3, pin4]
commandPinStatus = [0] * len(commandPins)

for pin in commandPins:
	GPIO.setup(pin, GPIO.OUT)

def setPins(commandNum):
	binList = list(map(int, list(bin(commandNum)[2:])))
	for i in range(len(commandPins)):
		GPIO.output(commandPins[i], binList[i])

 ## commands
commands = {
	"sit": 0,
	"stand": 1,
	"walk": 2,
	"walk_back":3,
	"walk_fast":4,
	"dance":5,
	"dance2":6
}

## mapping
buttons = {
	"A":0,
	"B":1,
	"X":2,
	"Y":3,
	"LB":4,
	"RB":5,
	"Back":6,
	"Start":7,
	"Metal Ball":8
}

axisLabels = {
	"TLLR": 0, # top left joystick, left/right
	"TLFB": 1, # top left joystick, front/back
	"BRLR": 2, # bottom right joystick, left/right
	"BRFB": 3 # bottom right joystick, front/back
}

axisNumbers = {
	0: {
		-1: "placeholder (command for what to do when TLLR is pushed left)",
		1: "placeholder (command for what to do when TLLR is pushed right)"
	},
	1: {
		-1: "stand", # "placeholder (command for what to do when TLFB is pushed forward - yes, counterintuitive)",
		1: "sit" # "placeholder (command for what to do when TLLR is pushed back)"
	},
	2: {
		-1: "placeholder (command for what to do when BRLR is pushed left)",
		1: "placeholder (command for what to do when BRLR is pushed right)"
	},
	3: {
		-1: "walk", # "placeholder (command for what to do when BRFB is pushed forward - yes, counterintuitive)",
		1: "placeholder (command for what to do when BRLR is pushed back)"
	}
}

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

print(joystick_count)

if joystick_count > 0:
	joystick=pygame.joystick.Joystick(0)

running = True

# with open("test.txt", "w") as file:
# 	file.write("Hello world!")

while running:
	for event in pygame.event.get():
		setSignals(1) # tells arduino to start receiving
		if event.type == pygame.JOYBUTTONDOWN:
			# print(f"Button {event.button} pressed")
			button = event.button
			if button == buttons["A"]:
				setPins(commands["stand"])
			elif button == buttons["B"]:
				setPins(commands["sit"])
			elif button == buttons["X"]:
				setPins(commands["dance"])
			elif button == buttons["Y"]:
				setPins(commands["dance2"])

		if event.type == pygame.JOYAXISMOTION: # joystick
			# print(f"Axis {event.axis} moved to {event.value}")
			axis = event.axis
			value = event.value

			if value == 1 or value == -1:
				setPins(commands[axisNumbers[axis][value]])


		if event.type == pygame.JOYHATMOTION: # the four button thing
			# print(f"Axis {event.value}")
			value = event.value
#		print(event)
		setSignals(0) # tells arduino to stop receiving new commands
