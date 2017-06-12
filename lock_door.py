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
SleepTimeL = 10 
GPIO.setup(11, GPIO.OUT)   
GPIO.output(11, GPIO.HIGH)  
  
# main loop  
  
try:  
  GPIO.output(11, GPIO.LOW)  
  print "Relay Turned On"  
  logging.info('Door locked')
  #GPIO.cleanup()  
  print "Good bye!"  
  time.sleep(SleepTimeL);
  GPIO.output(11, GPIO.HIGH)
  
# End program cleanly with keyboard  
except KeyboardInterrupt:  
  print " Quit"  
  
  # Reset GPIO settings  
GPIO.cleanup()  


