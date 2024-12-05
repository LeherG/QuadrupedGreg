import pygame
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

# GPIO.output(pinNum, GPIO.HIGH)

## setting the pins

pin1 = 0 #represents most significant
pin2 = 5
pin3 = 6
pin4 = 13 #rightmost least significant
print("-------------------------------------")


## commands
commands = {
	"sit": 13,
	"stand": 1,
	"walk": 2,
	"walk_back":3,
	"walk_fast":4,
	"dance":5,
	"dance2":6,
	"turn_l":7,
	"turn_r":8,
	"walk_turn_left":9,
	"walk_turn_right":12,
	"sidestep":10,
	"walkq":11
}

signalPins = [26, 19]

## signal pins
for pin in signalPins:
	GPIO.setup(pin, GPIO.OUT)

def setSignals(setting):
	for i in signalPins:
		GPIO.output(i, setting)

setSignals(0)

## command pins
commandPins = [pin1, pin2, pin3, pin4]

for pin in commandPins:
	GPIO.setup(pin, GPIO.OUT)

lastcommand = "default"

def setPins(commandNum):
	global lastcommand

	setSignals(1)
	cmd = "default"

	for key, value in commands.items():
		if value == commandNum:
			cmd = key

	# print("cmd: " + cmd)
	# print("lastcommand: " + lastcommand)

	# if cmd == lastcommand:
	# 	print(f"	last command was also {cmd}")

	# else:
	binList = list(map(int, list(bin(commandNum)[2:])))

	while len(binList) < 4:
		binList.insert(0,0)

	for i in range(len(commandPins)):
		GPIO.output(commandPins[i], binList[i])
	
	print("command num: " + str(commandNum))
	print("set pins to: " + str(binList))
	print("command: " + cmd)

	print("-------------------------------------")

	time.sleep(0.7)
	setSignals(0)

	lastcommand = cmd


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
	0: { # TLLR
		-1: "walk_turn_left", # Top left joystick pushed left
		1: "walk_turn_right" # Top left joystick pushed right
	},
	1: { # TLFB
		-1: "walk", # Top left joystick pushed forward - yes, counterintuitive
		1: "walk_back" # Top left joystick pushed back
	},
	3: { # BRLR
		-1: "turn_l", # Back right joystick pushed left
		1: "turn_r" # Back right joystick pushed right
	},
	4: { # BRFB
		-1: "walk", # Back right joystick pushed forward - yes, counterintuitive
		1: "stand" # Back right joystick pushed back
	}
}


pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

print(joystick_count)

if joystick_count > 0:
	joystick=pygame.joystick.Joystick(0)

running = True
axisold = 0
valueold = 0
standorsit = "sit"

while running:
	for event in pygame.event.get():
		setSignals(1) # tells arduino to start receiving
		if event.type == pygame.JOYBUTTONDOWN: # buttons
			# print(f"Button {event.button} pressed")
			button = event.button
			if button == buttons["A"]:
				setPins(commands["sit"])
				standorsit = "sit"
			elif button == buttons["B"]:
				setPins(commands["stand"])
				standorsit = "stand"
			elif button == buttons["X"]:
				setPins(commands["dance"])
			elif button == buttons["Y"]:
				setPins(commands["dance2"])

		if event.type == pygame.JOYAXISMOTION: # joystick
			# print(f"Axis {event.axis} moved to {event.value}")
			axis = event.axis
			value = event.value


			if value > 0.9:
				value = 1
			elif value < -0.9:
				value = -1
			elif value < 0.2 and value > -0.2:
				value = 0

			if value == 1 or value == -1:
				setPins(commands[axisNumbers[axis][value]])

			elif value == 0:
				setPins(commands[standorsit])
			
			axisold = axis
			valueold = value


		if event.type == pygame.JOYHATMOTION: # the four button thing
			print(f"Axis {event.value}")
			value = event.value
#		print(event)
		setSignals(0) # tells arduino to stop receiving new commands
