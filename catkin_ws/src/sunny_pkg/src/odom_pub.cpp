#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include<geometry_msgs/PoseWithCovarianceStamped.h>

void sub_cb(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& );

float x = 0.0;
float y = 0.0;
float z = 0.0;
float th = 0.0;
double cov[36];
double eye[36]={1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1};
geometry_msgs::PoseWithCovarianceStamped pos_sub;

int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;

  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("amcl_odom", 50);
  ros::Subscriber pose_sub = n.subscribe("/amcl_pose",1000,sub_cb);
//ros::Subscriber pose_sub = n.subscribe("poseupdate",1000,sub_cb);
  tf::TransformBroadcaster odom_broadcaster;

  
  double vx = 0.0;
  double vy = -0.0;
  double vth = 0.0;

  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(8.0);
  while(n.ok()){

    ros::spinOnce();               // check for incoming messages
    current_time = ros::Time::now();

    //compute odometry in a typical way given the velocities of the robot
    /*double dt = (current_time - last_time).toSec();
    double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
    double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
    double delta_th = vth * dt;

    pos_sub.pose.pose.position.x += delta_x;
    pos_sub.pose.pose.position.y += delta_y;
    pos_sub.pose.pose.orientation.w += delta_th;
*/
    //since all odometry is 6DOF we'll need a quaternion created from yaw
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(pos_sub.pose.pose.orientation.w);

    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "map";

    odom_trans.transform.translation.x =  pos_sub.pose.pose.position.x;
    odom_trans.transform.translation.y =  pos_sub.pose.pose.position.y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);

    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = current_time;
    odom.header.frame_id = "odom";

    //set the position
    odom.pose.pose.position.x =  pos_sub.pose.pose.position.x;
    odom.pose.pose.position.y =  pos_sub.pose.pose.position.y;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = odom_quat;
    odom.pose.covariance = pos_sub.pose.covariance;
	odom.pose.covariance[28] = 1;
	odom.pose.covariance[21] = 1;
	odom.pose.covariance[14] = 1;
      
    //set the velocity
    //odom.child_frame_id = "map";
    //odom.twist.twist.linear.x = vx;
    //odom.twist.twist.linear.y = vy;
    //odom.twist.twist.angular.z = vth;
    //odom.twist.covariance = pos_sub.pose.covariance;
	//odom.twist.covariance[28] = 1;
	//odom.twist.covariance[21] = 1;
	//odom.twist.covariance[14] = 1;

    //publish the message
    odom_pub.publish(odom);

    last_time = current_time;
    r.sleep();
  }
}


void sub_cb(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg ){
   	pos_sub.pose.pose.position.x=msg->pose.pose.position.x;
 	pos_sub.pose.pose.position.y=msg->pose.pose.position.y;
	pos_sub.pose.pose.orientation.w=msg->pose.pose.orientation.w;
	th=pos_sub.pose.pose.orientation.w;
	pos_sub.pose.covariance=msg->pose.covariance; 
         ROS_INFO("x=%f,y=%f",x,y);
}
