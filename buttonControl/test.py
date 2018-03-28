import jh2 as gpzp

while(True):
	count= gpzp.getButton()
	if count== 1:
		print("once")
	elif count== 2:
		print("twice")
	elif count>=3:
		print("long press")


