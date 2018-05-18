import os

flag_name = "/home/pi/Desktop/smartcane/blackbox/flag.txt"

def initFlag(filename=flag_name):
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename,"w")
    f.write(str(1))
    f.close()

def setFlag(flag,filename=flag_name):
    if os.path.exists(filename):
        try:
            f = open(filename,"a")
            f.write(str(flag))
            f.close()
        except:
            print("setflag failed")
    else:
        print("no flag file exists")

def getFlag(filename=flag_name):
    if os.path.exists(filename):
        try:
            f = open(flag_name,"r")
            flag = f.readline()
            return flag
        except:
            print("getflag failed")
    else:
        print("no flag file exists")
