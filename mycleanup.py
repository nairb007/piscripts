#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
  
GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
GPIO.setup(11, GPIO.IN)   
GPIO.setup(7, GPIO.IN)   
GPIO.setup(8, GPIO.IN)   
GPIO.cleanup()  


