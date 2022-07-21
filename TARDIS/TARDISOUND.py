import pygame
#file setup
path = 'sounds/'
sound_files = ["TARDIS-Take-off.mp3", "TARDIS-Land.mp3", "TARDIS-Ambient.mp3"]

#pygame setup
pygame.mixer.init()

#pygame.play
def play(string, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(path + string)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
def playNo(string, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(path + string)
    pygame.mixer.music.play()

def isPlaying():
    if pygame.mixer.music.get_busy() == True:
        return "True"
    else:
        return "False"

def stop():
    pygame.mixer.music.stop()
