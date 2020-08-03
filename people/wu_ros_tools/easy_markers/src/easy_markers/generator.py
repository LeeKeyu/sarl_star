import roslib; roslib.load_manifest('easy_markers')
import tf
import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, Quaternion

def get_point(position, scale=1.0):
    pt = Point()
    if position is None:
        pt.x = 0.0
        pt.y = 0.0
        pt.z = 0.0
    elif('x' in dir(position)):
        pt.x = position.x
        pt.y = position.y
        pt.z = position.z
    else:
        pt.x = position[0]
        pt.y = position[1]
        pt.z = position[2]

    pt.x /= scale
    pt.y /= scale
    pt.z /= scale

    return pt
    
def get_quat(orientation):
    quat = Quaternion()
    if orientation is None:
        quat.x = 0.0
        quat.y = 0.0
        quat.z = 0.0
        quat.w = 1.0
    elif('x' in dir(orientation)):
        quat.w = orientation.w
        quat.x = orientation.x
        quat.y = orientation.y
        quat.z = orientation.z
    elif len(orientation)==4:
        quat.x = orientation[0]
        quat.y = orientation[1]
        quat.z = orientation[2]
        quat.w = orientation[3]
    else:
        q2 = tf.transformations.quaternion_from_euler(orientation[0],orientation[1],orientation[2])
        quat.x = q2[0]
        quat.y = q2[1]
        quat.z = q2[2]
        quat.w = q2[3]
    return quat
        

class MarkerGenerator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.counter = 0
        self.frame_id = ''
        self.ns = 'marker'
        self.type = 0
        self.action = Marker.ADD
        self.scale = [1.0] *3
        self.color = [1.0] * 4
        self.points = []
        self.colors = []
        self.text = ''       
        self.lifetime = 0.0

    def marker(self, position=None, orientation=None, points=None, colors=None, scale=1.0):
        mark = Marker()
        mark.header.stamp = rospy.Time.now()
        mark.header.frame_id = self.frame_id
        mark.ns = self.ns
        mark.type = self.type
        mark.id = self.counter
        mark.action = self.action
        mark.scale.x = self.scale[0]
        mark.scale.y = self.scale[1]
        mark.scale.z = self.scale[2]
        mark.color.r = self.color[0]
        mark.color.g = self.color[1]
        mark.color.b = self.color[2]
        mark.color.a = self.color[3]
        mark.lifetime = rospy.Duration(self.lifetime)

        if points is not None:
            mark.points = []
            for point in points:
                mark.points.append(get_point(point, scale))
        if colors is not None:
            mark.colors = colors

        if position is not None or orientation is not None:
            mark.pose.position = get_point(position, scale)
            mark.pose.orientation = get_quat(orientation)

           

        self.counter+=1
        return mark
