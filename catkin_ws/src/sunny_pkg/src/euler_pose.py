#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

roll = pitch = yaw = 0.0
euler_pose=Odometry()
def get_rotation (msg):
    global roll, pitch, yaw, euler_pose
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    euler_pose.pose.pose.orientation.w=yaw
    euler_pose.pose.pose.position.x=msg.pose.pose.position.x
    euler_pose.pose.pose.position.y=msg.pose.pose.position.y
    euler_pose.twist.twist.linear.x=msg.twist.twist.linear.x
    euler_pose.header.frame_id='gzbbot/odom1'
    
    #print yaw

    
    
def state_transform():
    sub = rospy.Subscriber ('odom', Odometry, get_rotation)
    euler_state = rospy.Publisher('euler_odom', Odometry, queue_size= 1)
    rospy.init_node('quaternion_to_euler')
    r = rospy.Rate(15)
    while not rospy.is_shutdown():    
        
        euler_state.publish(euler_pose)    
        r.sleep()

if __name__ == '__main__':
    try:
       state_transform()
    except rospy.ROSInterruptException:
        pass
