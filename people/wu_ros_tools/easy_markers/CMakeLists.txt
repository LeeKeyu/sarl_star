cmake_minimum_required(VERSION 2.8.3)
project(easy_markers)
find_package(catkin REQUIRED COMPONENTS 
                interactive_markers
                roslib
                geometry_msgs
                visualization_msgs
                tf
                rospy)
catkin_python_setup()
catkin_package(CATKIN_DEPENDS geometry_msgs visualization_msgs)

catkin_install_python(PROGRAMS scripts/interactive_marker_demo.py scripts/std_marker_demo.py
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

