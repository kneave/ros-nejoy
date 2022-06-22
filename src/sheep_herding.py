#!/usr/bin/env python3
import rospy
from rosredboard.msg import Expander
from evdev import InputDevice, categorize, ecodes

rospy.init_node('sheep_herding_node', anonymous=True)
pub = rospy.Publisher('/redboard/expander', Expander, queue_size=10, latch=False)

dev = InputDevice('/dev/input/event0')
print(dev)

# Key Codes
# values: up: 0, down: 1, held: 2
#
# Key	    Code
# Q	        16
# W	        17
# E	        18
# R	        19
# A	        30
# S	        31
# D	        32
# F	        33
# Z	        44
# X	        45
# Space	    57
# N	        49
# M	        50
# K	        37
# L	        38
# O	        24
# P	        25

left_arm_rest = [0.17, -0.57, 0.14, 0.60, 0.02, 0.00, 0.00, 0.00]

def DoAction(event):
    global pub

    if event.value == 1:
        msg = Expander()

        # any value of 999 will be ignored by the expander node
        # so assume we don't want to move anything
        msg.servo0  = 999
        msg.servo1  = 999
        msg.servo2  = 999
        msg.servo3  = 999
        msg.servo4  = 999
        msg.servo5  = 999
        msg.servo6  = 999
        msg.servo7  = 999
        msg.servo8  = 999
        msg.servo9  = 999
        msg.servo10 = 999
        msg.servo11 = 999
        msg.servo12 = 999
        msg.servo13 = 999
        msg.servo14 = 999
        msg.servo15 = 999    

        if event.code == 16:    #   Q
            print("left arm above sheep")
            msg.servo0 = -0.01 
            msg.servo1 =  0.29
            msg.servo2 =  0.12
            msg.servo3 = -0.05
            msg.servo4 =  0.22
            msg.servo5 = -0.34
            msg.servo7 = -1.00

        if event.code == 17:
            print("left arm around sheep")
            # msg.servo0 = -0.01 
            # msg.servo1 =  0.29
            # msg.servo2 =  0.12
            # msg.servo3 = -0.05
            msg.servo4 = -0.77
            msg.servo5 =  0.80
            # msg.servo7 = -1.00

        if event.code == 18:
            print("left arm grip sheep")
            # msg.servo0 = -0.01 
            # msg.servo1 =  0.29
            # msg.servo2 =  0.12
            # msg.servo3 = -0.05
            # msg.servo4 = -0.77
            # msg.servo5 =  0.80
            msg.servo7 = -0.20

        if event.code == 19:
            print("left arm lift sheep")
            # -0.01, 0.38, 0.12, 0.76, -0.77, 0.80
            # msg.servo0 = -0.01 
            msg.servo1 =  0.38
            # msg.servo2 =  0.12
            msg.servo3 =  0.76
            # msg.servo4 = -0.77
            # msg.servo5 =  0.80
            # msg.servo7 = -0.20

        if event.code == 30:
            print("right arm above sheep")
        if event.code == 31:
            print("right arm around sheep")
        if event.code == 32:
            print("right open")
            msg.servo15 = -1.0
        if event.code == 33:
            print("right close")
            msg.servo15 = -0.4
        if event.code == 57:
            print("resting positions")
                            
        pub.publish(msg)

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        DoAction(event)

