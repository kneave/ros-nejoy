#!/usr/bin/env python3
from time import sleep

import rospy
from sensor_msgs.msg import Joy

from approxeng.input.selectbinder import ControllerResource

# The joystick returns "time held" for each button, we just need a 0 or 1
def CheckNone(input):
    if(input == None):
        return 0
    else:
        return 1

pub = rospy.Publisher('joy', Joy, queue_size=10)
rospy.init_node('joy_node', anonymous=True)

if __name__ == '__main__':
    try:
        # Get a joystick
        with ControllerResource() as joystick:
            # Loop until disconnected
            while joystick.connected:
                # Create message
                axes = [0,0,0,0,0,0,0]
                buttons = [0,0,0,0,0,0,0,0,0]
                joy_msg = Joy(None, axes, buttons)
                
                #  Left Stick
                joy_msg.axes[0] = joystick.lx
                joy_msg.axes[1] = joystick.ly

                # Right Stick
                joy_msg.axes[2] = joystick.rx
                joy_msg.axes[3] = joystick.ry

                # Rotation 
                joy_msg.axes[4] = joystick.lt
                joy_msg.axes[5] = joystick.rt

                # Encoder
#               joy_msg.axes[6] = joystick.ty

                # buttons = [s1, s2, s3_down, s4_up, s5, encoder, trigger, left_top, right_top]
                joy_msg.buttons[0] = CheckNone(joystick.cross) 
                joy_msg.buttons[1] = CheckNone(joystick.circle) 
                joy_msg.buttons[2] = CheckNone(joystick.ddown)
                joy_msg.buttons[3] = CheckNone(joystick.dup)
                joy_msg.buttons[4] = CheckNone(joystick.square)
                joy_msg.buttons[5] = CheckNone(joystick.select)
                joy_msg.buttons[6] = CheckNone(joystick.triangle)
                joy_msg.buttons[7] = CheckNone(joystick.ls)
                joy_msg.buttons[8] = CheckNone(joystick.rs)
                
                rospy.loginfo(joy_msg)
                pub.publish(joy_msg)

                sleep(0.05)
            
            print("Exiting, controller disconnected.")

    except rospy.ROSInterruptException:
        pass
