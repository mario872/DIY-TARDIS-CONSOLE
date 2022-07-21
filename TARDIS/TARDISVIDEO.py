import vlc

path = ("video/")

def video(string):
    player = vlc.MediaPlayer(path + string)\
    player.set_fulscreen(True)
    player.play()

# def stopVideo():
#     player.stop()