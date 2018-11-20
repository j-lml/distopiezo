import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set GPIO as output
GPIO.setup(12 ,GPIO.OUT)
GPIO.setup(16 ,GPIO.OUT)
GPIO.setup(20 ,GPIO.OUT)
GPIO.setup(21 ,GPIO.OUT)


state = 0;
while(1):
	if state == 0:	
		GPIO.output(12 ,1);
		GPIO.output(16,0);
		GPIO.output(20,0);
		GPIO.output(21,0);
		state = 1;
	elif state == 1:	
		GPIO.output(12 ,0);
		GPIO.output(16,1);
		GPIO.output(20,0);
		GPIO.output(21,0);
		state = 2;
	elif state == 2:	
		GPIO.output(12 ,0);
		GPIO.output(16,0);
		GPIO.output(20,1);
		GPIO.output(21,0);
		state = 3;
	elif state == 3:	
		GPIO.output(12 ,0);
		GPIO.output(16,0);
		GPIO.output(20,0);
		GPIO.output(21,1);
		state = 0;
	time.sleep(0.05)
