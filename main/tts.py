# -*- coding: utf-8 -*- 

import os
import sys
import urllib.request
import ssl
import pygame

ssl._create_default_https_context = ssl._create_unverified_context

client_id = "q0EvMJnxWgi_mML7oocc"
client_secret = "FHas8W2HNi"

def playSound(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    pygame.quit()
    
def tts_Clova(filename='tts.mp3',text='no text input'):
    encText = urllib.parse.quote(text)
    data = "speaker=jinho&speed=0&text=" + encText;
    url = "https://openapi.naver.com/v1/voice/tts.bin"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    
    if(rescode==200):
        print("TTS mp3")
        response_body = response.read()
        with open(filename, 'wb') as f:
            f.write(response_body)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.quit()
        os.remove(filename)
        
    else:
        print("Error Code:" + rescode)
