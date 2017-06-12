#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  

GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
GPIO.setup(7, GPIO.OUT)   
GPIO.output(7, GPIO.HIGH)  
  
# Reset GPIO settings  
GPIO.cleanup()  
