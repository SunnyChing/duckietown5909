#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Header
from geometry_msgs.msg import Point, Pose
from visualization_msgs.msg import Marker

import numpy as np

class Parkspace():
    def __init__(self):
        self.park_pub = rospy.Publisher("park_space", Marker, queue_size =1 )
        rospy.loginfo("park node initialized")
        self.marker = Marker()
        self.marker.header.frame_id = "/world"
        self.marker.header.stamp = rospy.Time.now()
        self.marker.ns = "/gzbbot"
        self.marker.id = 0
        self.marker.type = 1	# cube
        self.marker.action = 0
        self.marker.pose.position.x = 0
        self.marker.pose.position.y = 1.7
        self.marker.pose.position.z = 0.0
        self.marker.pose.orientation.w = 1.0
        self.marker.scale.x = 0.2
        self.marker.scale.y = 0.2
        self.marker.scale.z = 0.01
        self.marker.color.r = 0.0
        self.marker.color.g = 0.0
        self.marker.color.b = 1.0	# blue
        self.marker.color.a = 0.5
	

        while not rospy.is_shutdown():

            self.park_pub.publish(self.marker)




if __name__=="__main__":
    rospy.init_node("parkingspace")
    Parkspace()
    rospy.spin()

