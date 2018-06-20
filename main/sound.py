import os
import pygame
#os.system('pacmd set-default-sink 2')

mixer = pygame.mixer
mixer.init()

def start():
    mixer.music.load('voicefile/start.mp3')
    mixer.music.play()   
    
def camera():
    mixer.music.load('voicefile/camera.mp3')
    mixer.music.play()
    
def finish():
    mixer.music.load('voicefile/finish.mp3')
    mixer.music.play()
    
def mms():    
    mixer.music.load('voicefile/mms.mp3')
    mixer.music.play()

def caution():
    mixer.music.load('voicefile/caution.wav')
    mixer.music.play()
    
def click():
    mixer.music.load('voicefile/click.wav')
    mixer.music.play()
