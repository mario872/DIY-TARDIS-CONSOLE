from RPi import GPIO
from time import sleep

clk = 32
dt = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

def get_updated_state():
	clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
 	       if dtState != clkState:
	               counter += 1
               else:
 	              counter -= 1
                      return counter
                clkLastState = clkState
                sleep(0.01)
