# Import the required module for text 
# to speech conversion
from gtts import gTTS

import os

from playsound import playsound

# This module is imported so that we can 
# play the converted audio

# Language in which you want to convert
languageused = 'en'
#Path to files...
path = '/home/pi/TARDIS/'


def google(input_string, slowish):
    if not os.path.isfile(str(path) + str(input_string) + ".mp3"):
        # Passing the text and language to the engine.
        myobj = gTTS(text=input_string, lang=languageused, slow=slowish)
      
        # Saving the converted audio in a mp3 file named
        # speech 
        myobj.save(str(input_string) + ".mp3")
      
        # Playing the converted file
        playsound(str(path) + str(input_string) + ".mp3")
    else:
        # Playing the converted file
        playsound(str(path) + str(input_string) + ".mp3")
