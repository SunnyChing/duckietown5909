//*************************************************************
//
//This code load a path data from .txt and then saves it in thepath topic.
//And then, according the path to impelment L1 contorl.
//
//
//*************************************************************************





#include <tf/transform_datatypes.h>
#include "ros/ros.h"
#include <geometry_msgs/PoseStamped.h>
#include "geometry_msgs/PoseWithCovarianceStamped.h"
#include <geometry_msgs/PointStamped.h>
#include <time.h>
#include <nav_msgs/OccupancyGrid.h>
#include <nav_msgs/Path.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float64.h>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#define Lf  0.2
#define L 0.16
#define CONTROL_LOOP_FREQ 10
#define PI 3.141592
#define kv 0.24		//kv 	<--->	kv^2
#define kv1 1		//kv1 	<---> 	kv1^2
#define kv2 3.5		//kv2 	<---> 	kv2^2
#define kw 0.22		//kw	<--->	kw^2
#define kw1 1		//kw1	<--->	kw1^2
#define kw2 1.1		//kw2	<--->	kw2^2
#define dT 0.1 //frequency = 10 (Hz)
/********************************************************************
*																	*
*								class								*
*																	*

********************************************************************/

void get_tragectory(bool);
nav_msgs::Path mypathl, mypathr;

int main(int argc, char **argv)
{
  //Initi ROS
  ros::init(argc, argv, "readPath");
  ros::NodeHandle n;
  bool haspath= false;
  get_tragectory(!haspath);
 ros::Publisher chatter_pub = n.advertise<nav_msgs::Path>("mytrack", 1000);
 ros::Publisher chatter_pub1 = n.advertise<nav_msgs::Path>("chatter_r", 1000);
 while (ros::ok())
  {
  
    chatter_pub.publish(mypathl);
    chatter_pub1.publish(mypathr);
    ros::spinOnce();

   
  }


  return 0;
}
  
void get_tragectory(bool b){
  double temx,temy,tempphi;
  std::string headline;
  mypathl.header.frame_id="gzbbot/odom1";
  mypathr.header.frame_id="world";
  std::vector<geometry_msgs::PoseStamped> plan, plan1;
  geometry_msgs::PoseStamped tempose;

    std::ifstream myfile,myfile1;
    ROS_INFO("already open");
    myfile.open("/home/room5909/duckietown/catkin_ws/src/barc/track1.txt",std::ios::in);
    if(myfile.is_open()){
            ROS_INFO("openl");
            getline(myfile,headline);

            while (myfile>>temx>>temy){
              tempose.pose.position.x=temx;
              tempose.pose.position.y=temy;
              plan.push_back(tempose);
          }
    }else ROS_INFO("unable to openl");
mypathl.poses=plan;

/*myfile1.open("/home/room5909/Desktop/basement_r.txt",std::ios::in);
    if(myfile1.is_open()){
            ROS_INFO("openr");
            getline(myfile1,headline);

            while (myfile1>>temx>>temy){
              tempose.pose.position.x=temx;
              tempose.pose.position.y=temy;
              plan1.push_back(tempose);
          }
    }else ROS_INFO("unable to openr");

mypathr.poses=plan1;*/
}

