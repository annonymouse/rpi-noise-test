#!/usr/bin/env python

import argparse, subprocess
import RPi.GPIO as GPIO
from time import sleep

def _resp(port, programs):
    pids = dict()
    def callback(gpio):
        if gpio != port:
            return
        state = GPIO.input(gpio)
        if state == 1:
            # Stop doing things
            print "Changed to 1"
            for prog in programs:
                if pids and prog in pids:
                    pid = pids[prog]
                    pid.poll()
                    if not pid.returncode:
                        pid.kill()
                    else:
                        print "{0} not running {1}".format(prog, pid.returncode)
                else:
                    print "{0} hasn't been started, we can't stop it"
        else:
            # Start doing things
            print "Changed to 0"
            for prog in programs:
                if prog in pids:
                    pid = pids[prog]
                    pid.poll()
                    if pid.returncode:
                        pid= subprocess.Popen(prog)
                    else:
                        print "program is still running - we can't restart"

    if 0 == GPIO.input(port):
        print "port shorted"
        for p in programs:
            pids[p] = subprocess.Popen(p)
    else:
        print "not shorted"

        GPIO.add_event_detect(port, GPIO.BOTH,
            callback=callback, bouncetime=100)

    while True:
        sleep(5)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            help="Will run a list of programs when the port pin is pulled down")
    # For now only allow pin 26
    parser.add_argument("port", type=int, choices=(26),
            help="GPIO port to detect a short on")
    parser.add_argument("program", help="Program to execute when gpio fires",
            nargs="+")
    args = parser.parse_args()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.port, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    _resp(args.port, args.program)

