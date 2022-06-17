#Import the GPIO
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

handbrakePin = 13 #This is where we placed the NO wire from the Limit Switch
GPIO.setup(handbrakePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

onButtonPin = 11 #Where we placed the wire from our on/off button
GPIO.setup(onButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonLEDPin = 15 #Where we placed the LED for the button
GPIO.setup(buttonLEDPin, GPIO.OUT)

startPin = 12 #Broadcast to the PICO to start lights
GPIO.setup(startPin, GPIO.OUT)

#Import other things
import time
import threading
import random

#Import Sound and Video Modules
import TARDISOUND as TS
#import TARDISVIDEO as TV

volume = 1 #This is like setting the volume to 100%

sound_files = ["TARDIS-Take-off.mp3", "TARDIS-Land.mp3", "TARDIS-Ambient.mp3"]
video_files = ["Gallifreyan-Text.mp4"]

while True:
    
    if GPIO.input(onButtonPin) == 0: #If we did hit the On/Off button
        GPIO.output(buttonLEDPin, GPIO.HIGH)

        if GPIO.input(handbrakePin) == 0: #If we have not clicked it do the normal stuff.
            continue
            
        else: #We have clicked the throttle, start the dematerialisation!
            
            GPIO.output(startPin, GPIO.HIGH) #Tell pico to do strip lights
            
            
            TS.play(sound_files[0], volume) #Play dematerialisation sounds!
            
            TS.playNo(sound_files[2], volume) #Start ambience sounds
            time.sleep(random.randint(10, 60)) #Wait a while while the ambience is playing
            TS.stop() #When we've waited for that time, stop the ambient sounds.
            
            TS.play(sound_files[1], volume) #Play materialisation sound.
            
            
            GPIO.output(startPin, GPIO.LOW) #Tell PICO to stop lights
            
    else:
            GPIO.output(buttonLEDPin, GPIO.LOW)
    
GPIO.cleanup() #Clean up all of our GPIO