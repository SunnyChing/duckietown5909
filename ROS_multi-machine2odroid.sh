#!/bin/sh
# Set up the ROS multi-machine connection
export ROS_MASTER_URI=http://192.168.0.100:11311
export ROS_HOSTNAME=`hostname -I`
export ROS_IP=`hostname -I`

echo "Connected to ROS master hold by Odroid"
