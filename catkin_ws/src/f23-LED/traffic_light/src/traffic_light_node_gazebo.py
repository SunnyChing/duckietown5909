#!/usr/bin/env python
import rospy
from rgb_led import *
import sys
import time
from std_msgs.msg import Float32, Int8
from duckietown_msgs.msg import Vector2D, LEDDetection, LEDDetectionArray, GazeboLED
#from rgb_led import RGB_LED
from visualization_msgs.msg import Marker

class TrafficLight(object):
    def __init__(self):       
        self.node_name = rospy.get_name()
        self.cycle = None
        self.protocol =self.setupParameter("~LED_protocol",[]) #should be a list of tuples
        self.greenlight_freq = 10#self.protocol['signals']['traffic_light_go']['frequency']
        #self.redlight_freq = self.protocol['signals']['traffic_light_stop']['frequency']

        self.traffic_light_list = self.setupParameter("~traffic_light_list",[0,2,3,1]); #order of lights
        self.greenlight_duration = self.setupParameter("~greenlight_duration",3) #in seconds
        self.allred_duration = self.setupParameter("~allred_duration",2) #in seconds

       # self.redlight_t = 1.0/self.redlight_freq
        self.greenlight_t = 1.0/self.greenlight_freq
        self.green_on=False
        self.green_i = 0;
        self.green = self.traffic_light_list[self.green_i]
        self.green_color = 'g'#[0,1,0] #Hardcoded but should be parameter
        self.yellow_color = 'y'#[1,0.65,0] #Hardcoded but should be parameter
        self.redlightlist = self.traffic_light_list[:self.green_i] + self.traffic_light_list[(self.green_i+1):];
        self.traffic_light_state = {0:False,1:False,2:False,3:False} #All LEDs are off
        self.yellowlightlist = []
        self.traffic_cycle = rospy.Timer(rospy.Duration((self.greenlight_duration+self.allred_duration)),self.switchGreen)
        #self.redLED_cycle = rospy.Timer(rospy.Duration(0.5*self.redlight_t),self.freqred)
        self.greenLED_cycle = rospy.Timer(rospy.Duration(0.5*self.greenlight_t),self.freqgreen)
        # Publish fake traffic light signal
        self.pub_traffic_light = rospy.Publisher("~raw_led_trafficlight",GazeboLED,queue_size=1)
        self.visual_pub = rospy.Publisher("~light", Marker, queue_size =1 )

    def switchGreen(self,event):
        self.yellowlightlist=[]
        self.green_i = (self.green_i+1)%4 #Move to next light in list
        self.green = self.traffic_light_list[self.green_i]
        self.green_color = 'g'#[0,1,0]
        self.green_on=True
        self.redlightlist = self.traffic_light_list[:self.green_i] + self.traffic_light_list[(self.green_i+1):];
        rospy.sleep(self.greenlight_duration) #Keep the green light on
        self.green_on = False #Turn off the green light
        self.yellowlightlist = [self.green]
        rospy.sleep(self.allred_duration)
        self.redlightlist = self.traffic_light_list[0:]

    def freqred(self,event):
        for light in self.redlightlist:
            if self.traffic_light_state[light]==True:
                self.led.setRGB(light,[0,0,0])
                self.traffic_light_state[light]=False
            else:
                self.led.setRGB(light,[1,0,0])
                self.traffic_light_state[light]=True
        for light in self.yellowlightlist:
            if self.traffic_light_state[light]==True:
                self.led.setRGB(light,[0,0,0])
                self.traffic_light_state[light]=False
            else:
                self.led.setRGB(light,[1,1,0])
                self.traffic_light_state[light]=True

    def freqgreen(self,event):
        light = GazeboLED()
        #light.color = ['r','r','r','r']  #id : 49 51 52 53
        if self.green_on==False: #Exit if lights should all be red
	 return
        #light.color[self.green] = 'g'
        light.cross = str(self.green+1)
        light.intersection = 'trafficLight'
        light.car = 'trafficLight'
        print  light.cross, light.car
        self.pub_traffic_light.publish(light)
        self.visualize(self.green+1)

    def setupParameter(self,param_name,default_value):
        value = rospy.get_param(param_name,default_value)
        rospy.set_param(param_name,value) #Write to parameter server for transparancy
        rospy.loginfo("[%s] %s = %s " %(self.node_name,param_name,value))
        return value

    def visualize(self, cross):
        dx =0
        dy =0
        if cross ==1:
	 dx = -0.4
	 dy = 0
        elif cross ==2:
	 dx = 0
	 dy = -0.4
        elif cross == 3:
	 dx = 0.4
	 dy = 0
        elif cross == 4:
	 dx = 0
	 dy = 0.4
 
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "/"
        marker.id = 0
        marker.type = 2	# cube
        marker.action = 0
        marker.pose.position.x = 0.595*2.5 +dx
        marker.pose.position.y = 0.595*4.5 +dy
        marker.pose.position.z = 0.7
        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0	# blue
        marker.color.a = 1
        self.visual_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node('traffic_light',anonymous=False)
    node = TrafficLight()
    rospy.spin()
   # finally:
   #     for i in range(0,3):
    #            self.led.setRGB(i,[0,0,0])

