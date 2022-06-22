cmake_minimum_required(VERSION 3.0.2)
project(ne-joystick)

find_package(catkin REQUIRED COMPONENTS
  joy
  roscpp
  rospy
  std_msgs
  rosredboard
)

generate_messages(
  DEPENDENCIES
  rosredboard
)

catkin_package(
  #INCLUDE_DIRS include
  #LIBRARIES ne-joystick
  CATKIN_DEPENDS joy roscpp rospy std_msgs rosredboard
  DEPENDS rosredboard
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
