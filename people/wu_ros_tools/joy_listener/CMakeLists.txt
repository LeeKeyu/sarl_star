cmake_minimum_required(VERSION 2.8.3)
project(joy_listener)
find_package(catkin REQUIRED COMPONENTS 
                roslib
                sensor_msgs
                rospy)
catkin_python_setup()
catkin_package(CATKIN_DEPENDS sensor_msgs rospy)

