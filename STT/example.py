# -*- coding: utf-8 -*-
import gspeech
import time
def main():
    gsp = gspeech.Gspeech()
    while True:
    
        stt = gsp.getText()
        if stt is None:
            break
        print(stt)
        time.sleep(0.01)
        if ('HI' in stt):
            break


if __name__ == '__main__':
    main()
