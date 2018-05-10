import os

dirname = '/home/pi/Desktop/smartcane/blackbox/record'

def dir_exist():
	if not os.exists(dirname):
		os.makedirs(dirname)
def getDirSize(dirname):
	size = 0
	files = os.listdir(dirname)
	file_size_list = []
	for file in files:
		filename = os.path.join(dirname,file)
		if os.path.isfile(filename):
			temp = os.path.getsize(filename)
			size += temp
 			file_size_list.append([filename,size])
	return size
