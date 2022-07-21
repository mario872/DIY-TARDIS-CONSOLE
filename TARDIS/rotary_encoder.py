from RPi import GPIO
from time import sleep

clk = 32
dt = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clkLastState = GPIO.input(clk)
counter = 0
oldCounter = counter

def get_updated_state():
    global counter
    global clkLastState
    
    global oldCounter

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
            oldCounter = counter
            return counter 
        elif dtState == clkState:
            counter -= 1
            oldCounter = counter
            return counter
        else:
            return counter
    clkLastState = clkState
    
counter = 0    
for x in range(10):
    sleep(1)
    print(get_updated_state())
