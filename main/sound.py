import os
import pygame
os.system('pacmd set-default-sink 1')



def start():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/start.mp3')
    pygame.mixer.music.play()
    pygame.quit()
    
def camera():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/camera.wav')
    pygame.mixer.music.play()
    pygame.quit()
    
def finish():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/finish.mp3')
    pygame.mixer.music.play()
    pygame.quit()
    
def mms():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/mms.mp3')
    pygame.mixer.music.play()
    pygame.quit()

def caution():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/caution.wav')
    pygame.mixer.music.play()
    pygame.quit()
    
def click():
    pygame.mixer.init()
    pygame.mixer.music.load('voicefile/click.wav')
    pygame.mixer.music.play()
    pygame.quit()
