import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set GPIO as output
GPIO.setup(6  ,GPIO.OUT)
GPIO.setup(13 ,GPIO.OUT)
GPIO.setup(19 ,GPIO.OUT)
GPIO.setup(26 ,GPIO.OUT)

state = 0;
while(1):
	if state == 0:	
		GPIO.output(6 ,1);
		GPIO.output(13,0);
		GPIO.output(19,0);
		GPIO.output(26,0);
		state = 1;
	elif state == 1:	
		GPIO.output(6 ,0);
		GPIO.output(13,1);
		GPIO.output(19,0);
		GPIO.output(26,0);
		state = 2;
	elif state == 2:	
		GPIO.output(6 ,0);
		GPIO.output(13,0);
		GPIO.output(19,1);
		GPIO.output(26,0);
		state = 3;
	elif state == 3:	
		GPIO.output(6 ,0);
		GPIO.output(13,0);
		GPIO.output(19,0);
		GPIO.output(26,1);
		state = 0;
	time.sleep(0.05)
