import logging
import threading
import time
import os
import atexit

stop_threads = False

def thread_function(event_obj:threading.Event, stop):
    while True:
        print("Thread started, waiting for event")
        flag = event_obj.wait()
        print("Yeeeeee")
        if stop():
            break

def thread_trigger(event_obj:threading.Event, stop):
    while True:
        time.sleep(1)
        event_obj.set()
        event_obj.clear()
        if stop():
            break

def exit_handler():
    print("stopping threads")
    global stop_threads 
    stop_threads = True
    

# having difficulty stopping threads right now
if __name__ == "__main__":
    event_obj = threading.Event()
    terminate_thread = threading.Event()
    trigger = threading.Event()
    terminate_thread.set() 
    stop_threads = False
    x = threading.Thread(target=thread_function, args=[event_obj, lambda: stop_threads])
    y = threading.Thread(target=thread_trigger, args=[event_obj, lambda: stop_threads])
    atexit.register(exit_handler, trigger)
    x.start()
    y.start()
    num = 0
    while True: 
        print(f"Waiting {num}")
        num += 1
        time.sleep(1)
        if (num == 5):
            break
    