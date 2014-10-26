#!/usr/bin/env python

import RPIO, subprocess

def _resp(port, programs):
    RPIO.setmode(RPIO.BOARD)
    RPIO.setup(port, RPIO.IN)
    pids = dict()
    if 0 == RPIO.input(port):
        for p in programs:
            pids[p] = subprocess.popen(p)

    def callback(gpio, state):
        if gpio != port:
            return
        if state == 1:
            # Stop doing things
            print "Changed to 1"
            for prog in programs:
                if pids && prog in pids:
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
                if sub && prog in pids:
                    pid = pids[prog]
                    pid.poll()
                    if pid.returncode:
                        pid= subprocess.popen(prog)
                    else:
                        print "program is still running - we can't restart"
    RPIO.add_interrupt_callback(port, callback, pull_up_down=RPIO.PUD_UP)
    RPIO.wait_for_interrupts()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", help="Program to execute when gpio fires",
            nargs="+")
    args = parser.parse_args()
    _resp(26, args.program)

