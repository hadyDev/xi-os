import picoease as raw
from time import sleep_ms

read = raw.read
write = raw.write
init = raw.init

er0 = 0

def halt():
    global er0
    global pc
    print("halt")
    raw.pwrite(13, 8)
    er0 = raw.pread(4)


def resume():
    print("resume")
    print(er0)
    raw.run(0 | ((er0 >> 8) & 255), 256 | (er0 & 255))
    raw.pwrite(13, 0)
    raw.run(65167, 65039)


def connect():
    raw.connect()
    halt()
