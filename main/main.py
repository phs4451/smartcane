import tts
import obstacleDetect2
import button
import time
from multiprocessing import Process

def main2():
    while(True):
        print("Button2 listening...")
        count= button.getButton2()
        if count== 1:
            print("Button2 once")
        elif count== 2:
            print("Button2 twice")
            #obstacleDetect.main()
            t.terminate()
        elif count>=3:
            print("Button2 long press")
        time.sleep(1)

def main():
    while(True):
        print("Button1 listening...")
        count= button.getButton()
        if count== 1:
            print("Button1 once")
        elif count== 2:
            print("Button1 twice")
            #obstacleDetect.main()
            t.terminate()
        elif count>=3:
            print("Button1 long press")
        time.sleep(1)

obsDet = obstacleDetect2.obstacleDetect(20,21,12)
#t = multiprocessing.Process(target = obstacleDetect.main(),args=(1,100000))
t2 = Process(target = obsDet.main)
t1 = Process(target = main2)
#t = Process(target = obstacleDetect.main)

t = Process(target = main)
t.start(); t1.start(); t2.start()
t.join(); t1.join(); t2.start()

