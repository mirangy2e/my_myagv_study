from pymycobot import MechArm
import time

mc = MechArm("/dev/ttyACM#",115200)
init_pos = [0.17, -33.39, -12.56, -0.61, 43.94, 0.43]
while True:
    mc.send_angles(init_pos,50)
    time.sleep(1)
    # print(mc.get_angles())
    mc.send_angle(4,40,50)
    time.sleep(0.1)
    mc.send_angle(6,40,50)
    time.sleep(1)
    mc.send_angles(init_pos,50)
    time.sleep(1)
    mc.send_angle(4,-40,50)
    time.sleep(0.1)
    mc.send_angle(6,-40,50)
    time.sleep(1)
    mc.send_angle(1,40,50)
    time.sleep(1)
    mc.send_angles([-90.7, 28.91, -163.3, 1.66, -47.81, 2.02],50)
    time.sleep(2)
    mc.send_angle(1,90,50)
    time.sleep(3)
    mc.send_angle(3,0,50)
    time.sleep(0.1)
    mc.send_angle(5,55,50)
    time.sleep(2)
    mc.send_angles([0.52, -10.37, -5.97, -1.14, 33.83, 1.75],50)
    time.sleep(1)
    mc.send_angle(2,-73.38,50)
    time.sleep(0.1)
    mc.send_angle(3,40,50)
    time.sleep(0.1)
    mc.send_angle(4,0,50)
    time.sleep(0.1)
    mc.send_angle(5,65,50)
    time.sleep(0.1)