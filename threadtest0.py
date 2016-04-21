#thread example
import threading
import queue
import time
import random

import receiveblinks as client
from SetPin import SetPin

Q1=queue.Queue(100)  #100 limits number of inputs from foo that can be Queued.

def mainThread():
    h=threading.Thread(target=receiver,name="HIGHER")
    # note that "goo" is started by "for I in goo()" in function "hoo"
    # goo reads queued items from foo and yields them to hoo
    f=threading.Thread(target=reader,name="LOWER")

    print("STARTING")
    h.start()
    f.start()
    f.join()
    h.join()
    print("DONE")

def reader():
    message = list()
    ct = 0
    new = True
    for I in goo():
        if I and new:
            print("New message received! Processing...")
            new = False
        message.append(I);

    new = True
    ct += 1
    start = 0
    end = len(message)
    for char, i in enumerate(message):
        if char == '.':
            start = i
            break

    for char, i in enumerate(reversed(message)):
        if char == '.':
            end = i
            break

    print(client.process(''.join(message[start:end+1])))

def goo():
    # "gets values from Q1 queue; foo puts values onto Q1 queue"
    while True:
        g = Q1.get()
        if g != "/":
            yield g
        else:
            break

def receiver(): #receives from physical layer
    blinks = 1000
    duration = .075
    count = 0
    with SetPin(16, 'GPIO_23', direction='RX') as RXpin:
        RXpin.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for i in range(blinks):
            if RXpin.read_pin():
                count = 0
                Q1.put('.')
            else:
                count += 1
                Q1.put('*')
                
            if count == 20:
                Q1.put('/')
                return
            time.sleep(duration)

if __name__ == "__main__":
    mainThread()
