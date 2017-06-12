#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/scripts/door.log',
                    filemode='a')
  
GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
SleepTimeL = 12 
GPIO.setup(8, GPIO.OUT)   
GPIO.output(8, GPIO.HIGH)  
  
# main loop  
  
try:  
  GPIO.output(8, GPIO.LOW)  
  time.sleep(SleepTimeL);
  GPIO.output(8, GPIO.HIGH)
  logging.info('Door unlocked')
  
# End program cleanly with keyboard  
except KeyboardInterrupt:  
  print " Quit"  
  
GPIO.cleanup()
