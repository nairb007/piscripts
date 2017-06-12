#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/scripts/watering.log',
                    filemode='a')
  
GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
  
GPIO.setup(7, GPIO.OUT)   
GPIO.output(7, GPIO.HIGH)  
  
# main loop  
  
try:  
  GPIO.output(7, GPIO.LOW)  
  print "Relay Turned On"  
  logging.info('Watering turned on!')
  #GPIO.cleanup()  
  print "Good bye!"  
  
# End program cleanly with keyboard  
except KeyboardInterrupt:  
  print " Quit"  
  
  # Reset GPIO settings  
# GPIO.cleanup()  
