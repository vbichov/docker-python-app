import threading, requests

import signal
import sys
running = True
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        global running
        running = False
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('To exit press Ctrl+C')

def worker():
    global running
    while running:
      requests.get("http://localhost:5000/work")
threads = []
for x in range(0, 3):
    t = threading.Thread(target=worker, args=())
    threads.append(t)
    t.start()
signal.pause()   
