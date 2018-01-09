#include <tf/transform_datatypes.h>
#include "ros/ros.h"
#include <cmath>
#include <geometry_msgs/PointStamped.h>
#include "geometry_msgs/PoseWithCovarianceStamped.h"
#include <time.h>
#include <nav_msgs/Path.h>
#include <std_msgs/Float32MultiArray.h>


#define Lf  3
#define L 0.25
#define lf 0.1
#define Vcmd 1
#define CONTROL_LOOP_FREQ 20

class L1controller{

public:
L1controller(){
    //publish topic
    pub_ =n.advertise<std_msgs::Float32MultiArray>("vel_cmd",1000);

    //subscribe topic
    sub_pose = n.subscribe("/robot_ekf_pose/odom_combined",1000,&L1controller::posecb,this);
    sub_path = n.subscribe("/move_base/TrajectoryPlannerROS/global_plan",1000,&L1controller::pathcb,this);
   //sub_vel = n.subscribe("",1000,&L1controller::velcb,this);
    current_time = ros::Time::now();
    last_time = ros::Time::now();

    timer = n.createTimer(ros::Duration((float)1/CONTROL_LOOP_FREQ),&L1controller::loop_control,this);
     ros::Rate rate(50.0);
}

void posecb(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr &pose){

    current_time = ros::Time::now();

     pose_now = *pose;

     double x_now = pose_now.pose.pose.orientation.x;
     double y_now = pose_now.pose.pose.orientation.y;
     double z_now = pose_now.pose.pose.orientation.z;
     double w_now = pose_now.pose.pose.orientation.w;


     tf::Quaternion q_now(x_now, y_now, z_now, w_now);
     tf::Matrix3x3 quat_now(q_now);
     quat_now.getRPY(roll_now, pitch_now, yaw_now);


     double x_last = pose_last.pose.pose.orientation.x;
     double y_last = pose_last.pose.pose.orientation.y;
     double z_last = pose_last.pose.pose.orientation.z;
     double w_last = pose_last.pose.pose.orientation.w;


     tf::Quaternion q_last(x_last, y_last, z_last, w_last);
     tf::Matrix3x3 quat_last(q_last);
     quat_last.getRPY(roll_now, pitch_now, yaw_now);




     last_time = ros::Time::now();
     pose_last = pose_now;

     //ROS_INFO(" position_x = %f\tposition_y = %f\tposition _theta = %f\n", );
     //ROS_INFO("veloctiy_x = %f\tveloctiy_y = %f\n", v_x, v_y);

}
void pathcb(const nav_msgs::Path::ConstPtr &waypoint){

        path = *waypoint;

        double car_x = pose_now.pose.pose.position.x;
        double car_y = pose_now.pose.pose.position.y;
        double car_theta = yaw_now;


        double dist, goal_x, goal_y;
        double MIN_DIFF =5;

        //find the waypoint on th path with Lf
        for(int i=0;i<path.poses.size();i++){

            double path_x = path.poses[i].pose.position.x;
            double path_y = path.poses[i].pose.position.y;
            dist =sqrt(pow((car_x - path_x),2)+pow ((car_y - path_y),2));

                if(abs(dist-Lf)< MIN_DIFF){
                    goal_x=path_x;
                    goal_y=path_y;
                    MIN_DIFF=dist;
                   find_flag++;
                }
                 
         }

        if(find_flag==path.poses.size()){
            ctl_flag=1;
            find_flag=0;
        }
       // ROS_INFO("point found x=%f y=%f ",goal_x,goal_y);

        //eta
        eta=atan2(goal_y-car_y, goal_x-car_x);

        ROS_INFO("eta:\t%f",eta);
}
void loop_control(const ros::TimerEvent& event){

    std_msgs::Float32MultiArray msg;
    if(ctl_flag==1){
            ctl_flag=0;
            steering = -atan(L*sin(eta) / (Lf/2 +lf*cos(eta)));
             ROS_INFO("sterring:/t%f",steering);

    }
    msg.data.push_back(steering);
    pub_.publish(msg);
}




private:
    ros::NodeHandle n;
    ros::Subscriber sub_pose, sub_path;
    ros::Publisher pub_;
    geometry_msgs::PoseWithCovarianceStamped pose_now, pose_last;
    ros::Time current_time, last_time ;
    nav_msgs::Path path;
    ros::Timer timer;

    double roll_now, pitch_now, yaw_now;
    double roll_last, pitch_last, yaw_last;
    double eta, steering;
    int ctl_flag;
    int find_flag;





};
int main(int argc, char **argv)
{
  //Initi ROS
  ros::init(argc, argv, "posectl");

  //Create an object of class SubscribeAndPublish that will take care of everything
  L1controller l1ctrl;

  ros::spin();

  return 0;
}
  
