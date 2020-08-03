import roslib; roslib.load_manifest('joy_listener')
import rospy
from sensor_msgs.msg import Joy

class JoyListener(dict):
    def __init__(self, wait_time=1.0, joy_topic='/joy'):
        self.wait_time = wait_time
        self.sub = rospy.Subscriber(joy_topic, Joy, self.joy_cb, queue_size=1)
        self.last_time = rospy.Time(0)
        self.axes_cb = None

    def joy_cb(self, msg):
        buttons = msg.buttons
        now = rospy.Time.now() 
        if (now- self.last_time ).to_sec() < self.wait_time:
            return

        for button, function in self.iteritems():
            if buttons[button]:
                self.last_time = now
                function()
                break      

        if self.axes_cb:
            self.axes_cb(msg.axes)

PS3_BUTTONS = ['select', 'left_joy', 'right_joy', 'start', 'up', 'right', 'down', 'left', 'l2', 'r2', 'l1', 'r1', 'triangle', 'circle', 'x', 'square', 'ps3']
def PS3(name):
    return PS3_BUTTONS.index(name)


WII_BUTTONS = ['1', '2', 'a', 'b', '+', '-', 'left', 'right', 'up', 'down', 'home']

def WII(name):
    return WII_BUTTONS.index(name)
