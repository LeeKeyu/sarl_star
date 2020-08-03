cmake_minimum_required(VERSION 2.8.3)
project(roswiki_node)
find_package(catkin REQUIRED COMPONENTS)
catkin_package()
catkin_install_python(PROGRAMS scripts/roswiki
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

