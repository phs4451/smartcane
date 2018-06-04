import time
from time import strftime


def convert(inputName):
 
 data = open(inputName, "r")

 for line in data:
   gpgga = line.split(',')
   if gpgga[0] == '$GPGGA':
       if gpgga[2] != '':
            lat_val = str(gpgga[2]) + str(gpgga[3])
            long_val = str(gpgga[4]) + str(gpgga[5])
       else:
           return 1
   else:
     return 1 

      
 return lat_val,long_val
 

