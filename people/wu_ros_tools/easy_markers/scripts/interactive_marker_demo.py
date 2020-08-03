#!/usr/bin/python

import rospy
from easy_markers.interactive import InteractiveGenerator

def callback(feedback):
    print feedback

if __name__=='__main__':
    rospy.init_node('itest')

    ig = InteractiveGenerator()
    ig.makeMarker(controls=["move_x", "rotate_x"])
    ig.makeMarker(controls=["move_y", "rotate_y"], pose=[1,0,0], description="X")
    rospy.spin()
