import time
from time import strftime


def convert(inputName):
 
 data = open(inputName, "r")

 for line in data:
   gpgga = line.split(',')
   if gpgga[0] == '$GPGGA':
     lat_val = str(gpgga[2]) + str(gpgga[3])
     long_val = str(gpgga[4]) + str(gpgga[5])
   else:
     return 1 

      
 return "33.12N","128.11E"
 
'''
     strtrkpt = "<trkpt lat=\"" + str(lat_val) + "\" lon=\"" + str(long_val) + "\"> <time>" + format_time(gpgga[1]) + "</time> </trkpt>\n"
     file.write(strtrkpt)
        
 file.write("</trkseg>\n</trk>\n</gpx>\n")
 file.close()
'''
