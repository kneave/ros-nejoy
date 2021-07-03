#!/usr/bin/env python3
from time import sleep

import rospy
from sensor_msgs.msg import BatteryState

from pijuice import PiJuice # Import pijuice module
pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

pub = rospy.Publisher('power', BatteryState, queue_size=10)
rospy.init_node('controller_power_node', anonymous=True)

if __name__ == '__main__':
    try:
        # Loop until disconnected
        while True:
            try:
                # Create message
                msg = BatteryState()

                status = pijuice.status.GetStatus() # Read PiJuice status.
                chargeLevel = pijuice.status.GetChargeLevel()
                current = pijuice.status.GetBatteryCurrent()
                voltage = pijuice.status.GetBatteryVoltage()
                
                msg.voltage = voltage["data"] / 1000
                msg.current = current["data"] * -1
                msg.charge = chargeLevel["data"] / 100

                # uint8 POWER_SUPPLY_STATUS_UNKNOWN = 0
                # uint8 POWER_SUPPLY_STATUS_CHARGING = 1
                # uint8 POWER_SUPPLY_STATUS_DISCHARGING = 2
                # uint8 POWER_SUPPLY_STATUS_NOT_CHARGING = 3
                # uint8 POWER_SUPPLY_STATUS_FULL = 4

                isCharging = status["data"]["battery"] != "NORMAL"
                isCharged = True if msg.charge > 0.95 else False

                if(isCharged):
                    powerStatus = 4
                elif(isCharging):
                    powerStatus = 1
                else:
                    powerStatus = 2
                
                msg.power_supply_status = powerStatus

                msg.location = "Controller"
                rospy.loginfo(msg)
                pub.publish(msg)
            except:
                pass

            sleep(1)
        
        print("Exiting, controller disconnected.")

    except rospy.ROSInterruptException:
        pass
