import os

camera = "/home/pi/Desktop/smartcane/blackbox/flag_camera.txt"
vibrate = "/home/pi/Desktop/smartcane/blackbox/flag_vibrate.txt"
def initFlag(flagfile):
    if os.path.exists(flagfile):
        os.remove(flagfile)        
    f = open(flagfile,"w")
    f.write(str(1))
    f.close()

def setFlag(flag,filename):
    if os.path.exists(filename):
        try:
            f = open(filename,"w")
            f.write(str(flag))
            f.close()
        except:
            print("setflag failed")
    else:
        print("no flag file exists")

def getFlag(filename):
    if os.path.exists(filename):
        try:
            f = open(filename,"r")
            flag = f.readline()
            return flag
        except:
            print("getflag failed")
    else:
        print("no flag file exists")
