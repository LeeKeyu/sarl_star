cmake_minimum_required(VERSION 2.8.3)
project(manifest_cleaner)
find_package(catkin REQUIRED COMPONENTS rospy)
catkin_package()
catkin_install_python(PROGRAMS scripts/stats.py
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
