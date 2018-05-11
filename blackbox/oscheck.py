import os

dirname = '/home/pi/Desktop/smartcane/blackbox/record'
max_size = pow(2,30)

def dir_exist():
	if not os.exists(dirname):
		os.makedirs(dirname)
def getDirSize(dirname):
	size = 0
	files = os.listdir(dirname)
	file_size_list = []
	file_time_list = []

	for file in files:
		filename = os.path.join(dirname,file)
		file_time = int(file.split('.mp4')[0],base=10)

		if os.path.isfile(filename):
			temp = os.path.getsize(filename)
			size += temp
			file_size_list.append([file_time,size])
			file_time_list.append(file_time)
	
	if size > max_size:
		old_file = min(file_time_list)
		file_name =os.path.join(dirname,str(old_file)+'.mp4')
		os.remove(file_name)

