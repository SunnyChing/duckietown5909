/************************************************************************************************
 *  Program: 	ar_pillar_drive_ino_car.cpp							*	
 *  Author:	Ewing Kang
 *  Date:   	2015/12/30
 *  Contact: 	f039281310@yahoo.com.tw
 *  Licese:	BSD (see below)
 *  Note:
 *	This ROS program is mainly act as a templete for the final project of the course 
 * "Introduction to Computers" in the IBDPE of National Cheng Kung University, Taiwan. 
 * 	The program can determine the target between several AR tags and publish the driving 
 * command for Arduino Car. According to the current situation, there should be two Arduino car
 * driving status: the tracking mode which the car will drive toward the AR tags, and searching 
 * mode which the car should rotate itself and point the camera at different direction to enable
 * search.
 * 	Custom bundle file with ar_track_alvar can detect multiple "AR tag pillars" at the same 
 * time. An array in the program is used to record the detection and the information about each 
 * tag. Status array can mark individual tag destination as visited and look for unvisited tag.
 ************************************************************************************************
 	Software License Agreement (BSD License)

	 Copyright (c) 2012, Hsin-Yi Kang
	 All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are permitted 
 provided that the following conditions are met:
	
  * Redistributions of source code must retain the above copyright notice, this list of conditions
    and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or other materials provided
    with the distribution.
  * Neither the name of the Hsin-Yi Kang nor the names of its contributors may be used to endorse
    or promote products derived from this software without specific prior written permission.
	
 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR 
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
 FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
 CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
 WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
 WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	 author: Hsin-Yi Kang
 ***************************************************************************************************/
#include <ros/ros.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <ar_track_alvar_msgs/AlvarMarker.h>
#include <ar_track_alvar_msgs/AlvarMarkers.h>
#include <math.h>
#include <stdint.h>
#include <iostream>
using namespace std;
#define PI 3.14159265358979323846
#define LINEAR_TARGET 50			// 20cm
#define LINEAR_GAIN_P 700/100			// relationship between distance error and motor speed
#define ANGULAR_GAIN_P 1400			// relationship between angle error and motor speed
#define TAG_SEQ_COUNT 1			// how many AR tags we're looking for
#define TAG_SEQ_START 60			// tag ID starting number
#define TAG_SEQ_INTERVAL 2			// 60, 62, 64, .....
#define ACTIVATE_RANGE 30			// The range that a pillar is seen visited 30 cm
#define DISP_RATE_DIV 10	
		// the display rate divider, 1/10 rate of main loop

// global veriables

geometry_msgs::PoseStamped pose_ar[TAG_SEQ_COUNT];	// database of AR pose

// functions

void arinfoCallback(const ar_track_alvar_msgs::AlvarMarkers::ConstPtr& ar_info);	// subscriber callback

int main(int argc, char** argv){
  ros::init(argc, argv, "ar_pub");
  ros::NodeHandle node;

  ros::Subscriber ar_info_sub = node.subscribe("ar_pose_marker", 1000, arinfoCallback);		// subscribe to AR info
  ros::Publisher ino_drive_pub = node.advertise<geometry_msgs::Twist>("ino_drive", 1000);	// publishing Ino Car info
  ros::spinOnce();			// notify the ROS we're running

  // car driving related variables
  geometry_msgs::Twist ino_drive;
  double distance_cm, distance_err_cm, right_offset_cm, z_angle_err;
  ino_drive.linear.y = 0;	// we only need forward and z rotation
  ino_drive.linear.z = 0;
  ino_drive.angular.x = 0;
  ino_drive.angular.y = 0;

  int display_loop_i = 0;	// display rate controller

  // strat ROS node
  ros::Rate rate(10.0);
  while (node.ok()){
  
    
	

	// distance to the target AR tag
    distance_cm = pose_ar[0].pose.position.z * 100;
    right_offset_cm = pose_ar[0].pose.position.x * 100;


	/*
        cout << "AR target : " ;
        cout << "distance " << distance_cm;
        cout << ", offset " << right_offset_cm;
        cout << std::endl;*/
    


    /********** Inocar controlling **********/
    					
      distance_err_cm = LINEAR_TARGET - distance_cm;
      ino_drive.linear.x = -(-distance_err_cm * LINEAR_GAIN_P)+1500 ;  	// ranging +-50cm will have speed contorl mapping
      z_angle_err = atan2( right_offset_cm, distance_cm);
      ino_drive.angular.z =-z_angle_err*ANGULAR_GAIN_P +1500 ;
    

	// Ino car control display
    if( display_loop_i >= DISP_RATE_DIV ) {
      cout << "Ino car command: x " << ino_drive.linear.x;
      cout << ", rotation " << ino_drive.angular.z;
      cout << endl;
//	cout<<z_angle_err;
    }

    ino_drive_pub.publish(ino_drive);				// publishing the driving information


    /********** loop handlings **********/
    display_loop_i %= DISP_RATE_DIV;
    display_loop_i++;

    ros::spinOnce();
    rate.sleep();
  

  }	// end of while(node.ok())



 
  
  return 0;
};




void arinfoCallback(const ar_track_alvar_msgs::AlvarMarkers::ConstPtr& ar_info) {

  if(ar_info->markers.size()==1) {
   
    pose_ar[0] = ar_info->markers[0].pose;
   }
}

