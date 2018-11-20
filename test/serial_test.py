import serial
import time

#create serial device
dev = serial.Serial('/dev/ttyUSB0',9600)

time.sleep(2)

while(1):
	#Arduino will be sending data continuosly, so to get
	#the last data all the buffer must be cleared
	dev.flushInput()
	rawString = dev.readline()
	print(rawString)

dev.close()
