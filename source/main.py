#!/usr/bin/env python3          
                                
import signal                   
import sys
import RPi.GPIO as GPIO
import camera
import saving

BUTTON_GPIO = 23

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def pir_callback(channel):
    print("Car Detected!")
    print("Opening Camera...")
    camera.get_plate()
    print("Session Ended!")
    # sleep
    print("Waiting for car...\n")

def initialize():
    camera.init_camera()
    saving.create_containers()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, 
            callback=pir_callback, bouncetime=500)
    print("Interrupt OK!")
    print("Waiting for car...\n")
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
    

if __name__ == '__main__':
    print("Begin")
    initialize()

