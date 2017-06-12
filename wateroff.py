#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/var/log/watering.log',
                    filemode='a')

GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
logging.info('Watering turned off!')
GPIO.setup(7, GPIO.OUT)   
GPIO.output(7, GPIO.HIGH)  
  
# Reset GPIO settings  
GPIO.cleanup()  
