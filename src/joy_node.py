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

def TriggerDeadSpot(input):
    # triggers are 0..1 rather than -1..1 so convert
    input = (input * 2) - 1
    if -0.15 <= input <= 0.15:
        return 0
    else:
        return input

pub = rospy.Publisher('joy', Joy, queue_size=5)
rospy.init_node('joy_node', anonymous=True)

if __name__ == '__main__':
    try:
        # Get a joystick
        with ControllerResource() as joystick:
            print("Joystick connected.")
            run_loop = True
            r = rospy.Rate(20)

            # Loop until disconnected
            while not rospy.is_shutdown():
                # Create message
                axes = [0,0,0,0,0,0,0]
                buttons = [0,0,0,0,0,0,0,0,0]
                joy_msg = Joy(None, axes, buttons)
                
                #  Left Stick
                joy_msg.axes[0] = joystick.lx
                joy_msg.axes[1] = joystick.ly * -1

                # Right Stick
                joy_msg.axes[3] = joystick.rx
                joy_msg.axes[4] = joystick.ry

                # Rotation 
                joy_msg.axes[2] = TriggerDeadSpot(joystick.lt)

                right_trigger = TriggerDeadSpot(joystick.rt)
                # print(right_trigger)
                joy_msg.axes[5] = right_trigger

                # Encoder
                # joy_msg.axes[6] = joystick.lt

                # buttons = [s1, s2, s3_down, s4_up, s5, encoder, trigger, left_top, right_top]
                joy_msg.buttons[0] = CheckNone(joystick.square) 
                joy_msg.buttons[1] = CheckNone(joystick.triangle) 
                joy_msg.buttons[2] = CheckNone(joystick.ddown)
                joy_msg.buttons[3] = CheckNone(joystick.dup)
                joy_msg.buttons[4] = CheckNone(joystick.circle)
                joy_msg.buttons[5] = CheckNone(joystick.select)
                joy_msg.buttons[6] = CheckNone(joystick.cross)
                joy_msg.buttons[7] = CheckNone(joystick.ls)
                joy_msg.buttons[8] = CheckNone(joystick.rs)
                
#                rospy.loginfo(joy_msg)
                pub.publish(joy_msg)
#                print("Sending message")

                r.sleep()
                
            print("Exiting, controller disconnected.")

    except rospy.ROSInterruptException:
        pass
