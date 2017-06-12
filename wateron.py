#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
  
GPIO.setmode(GPIO.BCM)  
  
# Reset to a normal state  
  
GPIO.setup(7, GPIO.OUT)   
GPIO.output(7, GPIO.HIGH)  
  
# main loop  
  
try:  
  GPIO.output(7, GPIO.LOW)  
  print "Relay Turned On"  
  #GPIO.cleanup()  
  print "Good bye!"  
  
# End program cleanly with keyboard  
except KeyboardInterrupt:  
  print " Quit"  
  
  # Reset GPIO settings  
# GPIO.cleanup()  
