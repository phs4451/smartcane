# -*- coding: utf-8 -*-
import gspeech
import time
import string
import tts
import os

def main():
    i=0
    os.system("mplayer voicefile/enterstt.mp3")
    gsp = gspeech.Gspeech()
    while True:
        stt = gsp.getText()

        if stt is None:
            break
        print(stt)
        time.sleep(0.01)
        
        if(len(stt)==13):
            sms_file = open('/home/pi/Desktop/smartcane/main/sms.py','r+')
            lines = sms_file.readlines()
            sms_file.close()
            sms_file = open('/home/pi/Desktop/smartcane/main/sms.py','w+')
            Text = "      params['to'] = '{}'\n"
            replaceText = Text.format(stt)
            print(lines[44])
            print(replaceText)
            lines[44] = replaceText
            lines[51] = replaceText

            for line in lines:
                sms_file.write(lines[i])
                i+=1       
            
            gsp.pauseMic()
            sms_file.close()
            ttsText = stt + ' 로 설정되었습니다 '
            tts.tts_Clova(text = ttsText)
            
            break
        else:
            gsp.pauseMic()
            os.system("mplayer voicefile/wrong.mp3")
            break
        
        if ('종료' in stt):
            break


if __name__ == '__main__':
    main()
