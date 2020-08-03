cmake_minimum_required(VERSION 2.8.3)
project(catkinize_this)
find_package(catkin REQUIRED COMPONENTS rospy)
catkin_package()

catkin_install_python(PROGRAMS scripts/catkinize_this.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
