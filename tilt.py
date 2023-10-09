# coding=utf-8

import RPi.GPIO as GPIO
import datetime
import time


def my_callback(v):
    if v == GPIO.HIGH:
        print('\n ▲ at ' + str(datetime.datetime.now()))
    else:
        print('\n▼  at ' + str(datetime.datetime.now()))


CHANNEL = 22


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time.sleep(0.25)  # let the pin settle
    current = GPIO.input(CHANNEL)
    my_callback(current)
    while True:
        last = current
        GPIO.wait_for_edge(CHANNEL, GPIO.BOTH)
        current = GPIO.input(CHANNEL)
        # print('\nM:'+ str(current) + ' at ' + str(datetime.datetime.now()))
        if current != last:
            # if we got a new value wait to see if it sticks (debounce)
            now = time.time()
            end = now + 1  # end wait in 1000 millis
            timeoutMs = int((end - now) * 1000)
            while True:
                channel = GPIO.wait_for_edge(CHANNEL, GPIO.BOTH, timeout=timeoutMs)
                if channel is None:
                    timeoutMs = 0
                else:
                    current = GPIO.input(CHANNEL)
                    # print('\nW:'+ str(current) + ' at ' + str(datetime.datetime.now()))
                    if current == last:
                        # We flip-flopped start over at the main loop
                        break
                    # we got the same result as before (it's binary)
                    timeoutMs = int((end - time.time()) * 1000)

                if timeoutMs <= 0:
                    my_callback(current)
                    break
            # End wait loop
finally:
    GPIO.cleanup()

