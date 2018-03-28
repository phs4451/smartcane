import tts
import obstacleDetect
import button
import time
from multiprocessing import Process

def main2():
    while(True):
        print("listening...")
        count= button.getButton()
        if count== 1:
            print("once")
        elif count== 2:
            print("twice")
            #obstacleDetect.main()
            t.terminate()
        elif count>=3:
            print("long press")
        time.sleep(1)

  
#t = multiprocessing.Process(target = obstacleDetect.main(),args=(1,100000))
t1 = Process(target = main2)
t = Process(target = obstacleDetect.main)
t.start()
t1.start()
t.join()
t1.join()


