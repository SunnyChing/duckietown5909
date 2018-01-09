//
//  CarCtl.h
//  
//
//  Created by ching on 2016/10/13.
//
//

#ifndef carctl_h
#define carctl_h

#include <stdio.h>
#include "ros/ros.h"
#include <geometry_msgs/PointStamped.h>
#include <time.h>
#include <nav_msgs/Path.h>

#endif /*carctl_h */


class L1Controller
{
public:
    L1Controller();
    void posecb(const geometry_msgs::PoseStamped::ConstPtr &pose);
    void pathcb(const nav_msgs::Path::ConstPtr& path);

private:
    ros::NodeHandle n;
    ros::Subscriber sub_pose, sub_path;
    ros::Publisher pub_;
    geometry_msgs::PoseWithCovarianceStamped pose_now, pose_last;
    ros::Time current_time, last_time ;
    nav_msgs::Path path;

    double roll_now, pitch_now, yaw_now;
    double roll_last, pitch_last, yaw_last;


};
