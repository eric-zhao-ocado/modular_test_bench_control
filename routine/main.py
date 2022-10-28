from .automated_routine import routine
from threading import Timer
def hello():
    print("hello, world")



if __name__ == '__main__':
    t = Timer(30.0, hello)
    t.start()  # after 30 seconds, "hello, world" will be printed
    # while True:
    #     routine = input('"Manual" or "Automated" routine?')
    #     if routine == 'Manual':
    #         automated_routine()
    #     elif routine == 'Automated':

    