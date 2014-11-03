#!/usr/bin/env python

import argparse, subprocess, os
import RPi.GPIO as GPIO
from time import sleep

def _resp(port, programs):
    pids = dict()
    def kill():
        print "kill"
        GPIO.remove_event_detect(port)
        GPIO.add_event_detect(port, GPIO.FALLING, callback=lambda _x: start(),
                bouncetime=500)
        for prog in programs:
            if prog in pids:
                pids[prog].poll()
                if not pids[prog].returncode:
                    pids[prog].kill()
                else:
                    print "{0} not running {1}".format(prog, pids[prog].returncode)
            else:
                print "{0} hasn't been started, we can't stop it"
    def start():
        print "start"
        GPIO.remove_event_detect(port)
        GPIO.add_event_detect(port, GPIO.RISING, callback=lambda _x: kill(),
                bouncetime=500)
        for prog in programs:
            if prog in pids:
                pids[prog].poll()
                if pids[prog].returncode:
                    pids[prog]= subprocess.Popen(prog)
                else:
                    print "program is still running - we can't restart"
            else:
                pids[prog] = subprocess.Popen(prog)

    state = GPIO.input(port)
    if state == 1:
        # Stop doing things
        print "Not shorted"
        kill()
    else:
        print "Shorted"
        start()
    while True:
        sleep(5)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # For now only allow pin 26
    parser.add_argument("port", type=int, choices=[26],
            help="GPIO port to detect a short on")
    parser.add_argument("program", help="Program to execute when gpio fires",
            nargs="+")
    args = parser.parse_args()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    _resp(args.port, args.program)

