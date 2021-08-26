from time import sleep
import pydirectinput


def pressKey(k):
    pydirectinput.keyDown(k)


def releaseKey(k):
    pydirectinput.keyUp(k)


def left():
    """ Turn left """
    pressKey("a")
    releaseKey("a")
    


def right():
    """ Turn right """
    pressKey("d")
    releaseKey("d")
    


def release_all():
    """ Release all keys """
    releaseKey("w")
    releaseKey("a")
    releaseKey("d")

def click(x, y):
    pydirectinput.click(x=x, y=y)
    
if __name__ == "__main__":
    sleep(3)
    right()

    