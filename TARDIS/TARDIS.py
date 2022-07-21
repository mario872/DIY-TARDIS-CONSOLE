import sys
import RPi.GPIO as GPIO

from flask import Flask, render_template, redirect, request

sys.path.insert(0, '/home/pi/TARDIS/handles/assistant-sdk-python/google-assistant-sdk/googlesamples/assistant/grpc')

#from genericpushtotalk import *

GPIO.setmode(GPIO.BCM)

handbrakePin = 27 #This is where we placed the NO wire from the Limit Switch
GPIO.setup(handbrakePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

onButtonPin = 17 #Where we placed the wire from our on/off button
GPIO.setup(onButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonLEDPin = 22 #Where we placed the LED for the button
GPIO.setup(buttonLEDPin, GPIO.OUT)

startPin = 19 #Broadcast to the PICO to start lights
GPIO.setup(startPin, GPIO.OUT)

rotaryButtonPin = 26
GPIO.setup(rotaryButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

handlesLED = 20
GPIO.setup(handlesLED, GPIO.OUT)

handlesPin  = 16
GPIO.setup(handlesPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

keysPin = 18
GPIO.setup(keysPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

keyboardPin = 21
GPIO.setup(keyboardPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Import other things
import time
import threading
import random

#Import Sound, Keyboard and Speaking Modules
import TARDISOUND as TS
import TARDISKEYBOARD as TK
import TARDISPEAK as TSPEAK

from encoder import Encoder #www.github.com/nstansby/rpi-rotary-encoder-python
import I2C_LCD_driver #www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
import keyboard
import glowbit

matrix = glowbit.matrix4x4(pin=12, brightness = 25, rateLimitFPS = 10)

LCD = I2C_LCD_driver.lcd()
rotary = Encoder(23, 24)

def LCD_Display(string):
    LCD.lcd_clear()
    LCD.lcd_display_string(string, 1)

def LCD_Clear():
    LCD.lcd_clear()

volume = .75 #This is like setting the volume to 100%

MusicThreadON = "False"
SoundThreadON = "False"
GPIOThreadON = "False"
keyboardThreadON = "False"
vortexON = "False"

webGo = "False"

music_files_location = ["All Star.mp3", "An Idiot with a Box.mp3", "Bohemian Rhapsody.mp3", "Cereal Killa.mp3", "Dance Magic Dance.mp3", "DW Theme.mp3", "Doctor Who Theme Remix Extended.mp3", "Father and Son.mp3", "I'm So.mp3", "I'm Still Standing.mp3", "I am the Doctor.mp3", "Never Gonna Give You Up.mp3", "New Shirt.mp3", "Starman Lightyear.mp3"]
music_files = ["All Star Smas...", "An Idiot with...", "Bohemian Rhap...", "Cereal Killa....", "Dance Magic D...", "DW Theme 2005...", "DW Theme Remi... ", "Father and So...", "I'm So Andrew...", "I'm Still Sta...", "I am the Doct...", "Never Gonna G...", "New Shirt Pon...", "Starman Light..."]

max_music = len(music_files) -1
min_music = 0

whereTo = ""

sound_files = ["TARDIS-Take-off.mp3", "TARDIS-Land.mp3", "TARDIS-Ambient.mp3"]
video_files = ["Gallifreyan-Text.mp4"]   
def keyboardKeys(Null):
    global whereTo
    global keyboardThreadON
    keyboardThreadON = "True"
    while True:
        whereTo = TK.returnKeypress()
        time.sleep(.1)
def playMusic(Null):
    if TS.isPlaying() == "True": #If music is playing then it will stop the sound.
        TS.stop()
        print("Paused.")
        return
    else: #Start playing the music we select with the rotary encoder below in music()
        TS.playNo(music_files_location[rotary.value], volume)
        #print("Music Track is: " + str(music_files_location[rotary.value]))

                
GPIO.add_event_detect(rotaryButtonPin, GPIO.FALLING, callback=playMusic, bouncetime=200)

def music(Null):
    while True:
        global MusicThreadON
        global whereTo
        global max_music
        global min_music
        MusicThreadON = "True"
        MusicRotaryThreadON = "False"
        keyboardTesting = "False"
        #MusicRotaryThread.start()
        listPress = [keyboard.read_key()]
        oldestination = ""
        while True:
            if GPIO.input(onButtonPin) == 0:
                if keyboardTesting == "True": #GPIO.input(keyboardPin) == 0:
                        destination = whereTo
                        if destination == oldestination:
                            pass
                        else:
                            LCD_Display(destination, line=2)
                            oldestination = destination
                else:
                    if TS.isPlaying() == "False":
                        if rotary.getValue() > max_music:
                            rotary.value = min_music
                        elif rotary.getValue() < min_music:
                            rotary.value = max_music
                
                        #print("Music Track is:" + str(rotary.value))                        
                        LCD_Display(music_files[rotary.value])
            else:
                LCD_Clear()

def vortex(Null):
    global vortexON
    vortexON = "True"
    while True:
        while True:
            if GPIO.input(onButtonPin) == 0:
                if webGo == "True":
                    matrix.circularRainbow()

                    if GPIO.input(onButtonPin) == 1 or webGo == "False":
                        matrix.pixelsFill(matrix.black()) # Make display black
                        matrix.pixelsShow()
                        break
                elif GPIO.input(handbrakePin) == 1:
                    matrix.circularRainbow()
            
                    if GPIO.input(onButtonPin) == 1:
                        matrix.pixelsFill(matrix.black()) # Make display black
                        matrix.pixelsShow()
                        break


matrix.pixelsShow()

def TSSound(Null): 
    global SoundThreadON
    global webGo
    
    SoundThreadON = "True"
    
    while True:
        if GPIO.input(onButtonPin) == 0:   
            if webGo == "True":
                if TS.isPlaying() == "False":
                    GPIO.output(startPin, GPIO.HIGH) #Tell pico to do strip lights
                    TS.playNo(sound_files[0], volume) #Play dematerialisation sounds!
                    for i in range(50):
                        if GPIO.input(onButtonPin) == 1 or webGo == "False":
                            TS.stop()
                            webGo = "False"
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    TS.playNo(sound_files[2], volume) #Start ambience sounds
                    for i in range(10, random.randint(20,120)):
                        if GPIO.input(onButtonPin) == 1 or webGo == "False":
                            TS.stop()
                            webGo = "False"
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    TS.stop() #When we've waited for that time, stop the ambient sounds.
                            
                    TS.playNo(sound_files[1], volume) #Play materialisation sound.
                    for i in range(46):
                        if GPIO.input(onButtonPin) == 1 or webGo == "False":
                            TS.stop()
                            webGo = "False"
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    webGo = "False"
                    GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                else:
                    GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                    pass
                    webGo = "False"
                webGo = "False"
            elif GPIO.input(handbrakePin) == 1:
                if TS.isPlaying() == "False":
                    GPIO.output(startPin, GPIO.HIGH) #Tell pico to do strip lights
                    TS.playNo(sound_files[0], volume) #Play dematerialisation sounds!
                    for i in range(50):
                        if GPIO.input(onButtonPin) == 1:
                            TS.stop()
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    TS.playNo(sound_files[2], volume) #Start ambience sounds
                    for i in range(10, random.randint(20,120)):
                        if GPIO.input(onButtonPin) == 1:
                            TS.stop()
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    TS.stop() #When we've waited for that time, stop the ambient sounds.
                            
                    TS.playNo(sound_files[1], volume) #Play materialisation sound.
                    for i in range(46):
                        if GPIO.input(onButtonPin) == 1:
                            TS.stop()
                            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                            break
                        time.sleep(.5)
                    webGo = "False"
                    GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                else:
                    GPIO.output(startPin, GPIO.LOW) #Tell pico to stop the strip lights
                    pass


def web(null):
    global GPIOThreadON
    GPIOThreadON = "True"
    
    while True:

        
        if GPIO.input(onButtonPin) == 0: #If we did hit the On/Off button
            GPIO.output(buttonLEDPin, GPIO.HIGH)
            if MusicThreadON == "False":
                MusicThread.start()                                                                                                                                                                                                                                                                                                                                                                  

            if SoundThreadON == "False":
                TSSoundThread.start()
            if keyboardThreadON == "False":
                KeyboardThread.start()
            if vortexON == "False":
                vortexThread.start()


                

        else:
            GPIO.output(startPin, GPIO.LOW) #Tell pico to stop strip lights
            GPIO.output(buttonLEDPin, GPIO.LOW)    
    
MusicThread = threading.Thread(target=music, args=(1,), daemon=True)
TSSoundThread = threading.Thread(target=TSSound, args=(1,), daemon=True)
GPIOThread = threading.Thread(target=web, args=(1,), daemon=True)
KeyboardThread = threading.Thread(target=keyboardKeys, args=(1,), daemon=True)
vortexThread = threading.Thread(target=vortex, args=(1,), daemon=True)

if GPIOThreadON == "False":
    GPIOThread.start()
    
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go')
def go():
    global webGo
    TSPEAK.google("Initialising Time Space Dematerialisation Procedures.", False)
    webGo = "True"
    return redirect('/')
@app.route('/no')
def no():
    global webGo
    TS.stop()
    webGo = "False"
    TSPEAK.google("Ow! Bang, Bange, Crash!", False)
    print("Stop the engines River!")
    return redirect('/')
@app.route('/playPause')
def playPause():
    playMusic(0)
    return redirect('/')

#@app.route('/terminal', methods =["GET","POST"])
#def terminal():
 #   if request.method == "POST":
        #get input from user
   #     command = request.form.get("command")
    #    globals()[command]
     #   return redirect('/terminal')
    #TSPEAK.google("My name is Handles, but my terminal doesn't work yet.", False)
  #  return render_template('terminal.html')
try:
    if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')
except KeyboardInterrupt:  
    GPIO.cleanup() #Clean up all of our GPIO
