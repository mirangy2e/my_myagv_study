from pymycobot.myagv import MyAgv
import time

MA = MyAgv('/dev/ttyAMA2',115200)

#RED
MA.set_led(1,255,0,0)
time.sleep(2)

#OFF
MA.set_led(1,0,0,0)
time.sleep(2)

#Blynk RED
MA.set_led(2,255,0,0)
time.sleep(2)
# turn off 
MA.set_led(1,255,0,0)
time.sleep(2)
