import roslib; roslib.load_manifest('easy_markers')

from easy_markers.generator import MarkerGenerator
from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import InteractiveMarkerControl

TYPEDATA = {
    'rotate_x': [1,1,0,0, InteractiveMarkerControl.ROTATE_AXIS],
    'move_x'  : [1,1,0,0, InteractiveMarkerControl.MOVE_AXIS],
    'rotate_z': [1,0,1,0, InteractiveMarkerControl.ROTATE_AXIS],
    'move_z'  : [1,0,1,0, InteractiveMarkerControl.MOVE_AXIS],
    'rotate_y': [1,0,0,1, InteractiveMarkerControl.ROTATE_AXIS],
    'move_y'  : [1,0,0,1, InteractiveMarkerControl.MOVE_AXIS]
}

def default_callback(feedback):
    print feedback

class InteractiveGenerator:
    def __init__(self, name="interactive_markers"):
        self.server = InteractiveMarkerServer(name)
        self.mg = MarkerGenerator()
        self.mg.type = 1
        self.mg.scale = [.25]*3
        self.c = 0
        self.markers = {}



    def makeMarker( self, callback=None, marker=None, pose=[0,0,0], controls=[], 
                    fixed=False, name=None, frame="/map", description="", imode=0, rot=[0,0,0,1]):

        if marker is None:
            marker = self.mg.marker()

        if callback is None:
            callback = default_callback

        if name is None:
            name = "control%d"%self.c
            self.c += 1

        int_marker = InteractiveMarker()
        int_marker.header.frame_id = frame
        int_marker.pose.position.x = pose[0]
        int_marker.pose.position.y = pose[1]
        int_marker.pose.position.z = pose[2]
        int_marker.pose.orientation.x = rot[0]
        int_marker.pose.orientation.y = rot[1]
        int_marker.pose.orientation.z = rot[2]
        int_marker.pose.orientation.w = rot[3]
        int_marker.scale = 1
        int_marker.name = name
        int_marker.description = description

        control = InteractiveMarkerControl()
        control.always_visible = True
        control.interaction_mode = imode
        control.markers.append( marker )
        int_marker.controls.append(control)

        for control_name in controls:
            data = TYPEDATA[control_name]
            control = InteractiveMarkerControl()
            control.orientation.w = data[0]
            control.orientation.x = data[1]
            control.orientation.y = data[2]
            control.orientation.z = data[3]
            control.name = control_name
            control.interaction_mode = data[4]
            if fixed:
                control.orientation_mode = InteractiveMarkerControl.FIXED
            int_marker.controls.append(control)

        self.server.insert(int_marker, callback)
        self.markers[name] = int_marker
        self.server.applyChanges()
