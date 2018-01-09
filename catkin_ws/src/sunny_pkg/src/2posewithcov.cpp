#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>
#include<geometry_msgs/PoseStamped.h>


void sub_cb(const geometry_msgs::PoseStamped::ConstPtr& );


geometry_msgs::PoseWithCovarianceStamped pos_pub;


int main(int argc, char** argv){
  ros::init(argc, argv, "posestamped2posewithCov_publisher");

  ros::NodeHandle n;

  ros::Publisher pose_pub = n.advertise<geometry_msgs::PoseWithCovarianceStamped>("", 1);
  ros::Subscriber pose_sub = n.subscribe("",1,sub_cb);

 
  
  

  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  
  while(n.ok()){
   pose_pub.publish(pos_pub);
    ros::spinOnce();               // check for incoming messages
   
    
  }
}


void sub_cb(const geometry_msgs::PoseStamped::ConstPtr& msg ){
   	
	pos_pub.header=msg->header;
        pos_pub.pose.pose.position.x=msg->pose.position.x;
 	pos_pub.pose.pose.position.y=msg->pose.position.y;
	pos_pub.pose.pose.orientation=msg->pose.orientation;
	
}
