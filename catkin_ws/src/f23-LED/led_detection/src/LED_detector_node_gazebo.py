#!/usr/bin/env python
import rospy
import time
from led_detection.LEDDetector import LEDDetector
from std_msgs.msg import Byte, String
from duckietown_msgs.msg import Vector2D, LEDDetection, LEDDetectionArray, LEDDetectionDebugInfo, BoolStamped, GazeboLED,AprilTagsWithInfos, SignalsDetection
from duckietown_utils.bag_logs import numpy_from_ros_compressed
import numpy as np

class LEDDetectorNode(object):
    def __init__(self):
        self.active = True # [INTERACTIVE MODE] Won't be overwritten if FSM isn't running, node always active 
        self.trigger = False
        self.node_state = 0
        self.data = []
        self.tags_id_seen=[]
        self.subself = False
        self.node_name = rospy.get_name()
        self.veh_name = rospy.get_namespace().strip("/")
        rospy.loginfo('[%s] Vehicle: %s'%(self.node_name, self.veh_name))
        if not self.veh_name:
            # fall back on private param passed thru rosrun
            # syntax is: rosrun <pkg> <node> _veh:=<bot-id>
            if rospy.has_param('~veh'):
                self.veh_name = rospy.get_param('~veh')
        rospy.loginfo('[%s] Vehicle: %s'%(self.node_name, self.veh_name))

        self.protocol = rospy.get_param("~LED_protocol")
        self.label = rospy.get_param("~location_config") # should be a list
        self.continuous = rospy.get_param('~continuous', True) # Detect continuously as long as active


        self.lightGo = self.protocol['signals']['traffic_light_go']['frequency']
        self.lightStop = self.protocol['signals']['traffic_light_stop']['frequency']
        self.carSignalA = self.protocol['signals']['CAR_SIGNAL_A']['frequency']
        self.carSignalB = self.protocol['signals']['CAR_SIGNAL_B']['frequency']
        self.carSignalC = self.protocol['signals']['CAR_SIGNAL_C']['frequency']                                                               # [INTERACTIVE MODE] set to False for manual trigger
        self.frequencies = self.protocol['frequencies'].values()
        param_car_dict = rospy.get_param("~cars",{})
        self.cross_dict={'right':{'12','23','34','41'},
		  'front':{'13','31','24','42'},
		  'left':{'14','43','32','21'},
		  }
        self.intersection = []
        self.cross = ''
        #initialize the standard output message
        self.front = SignalsDetection.NO_CAR
        self.right = SignalsDetection.NO_CAR
        self.left = SignalsDetection.NO_CAR
        self.traffic_light_state = SignalsDetection.NO_TRAFFIC_LIGHT
        #self.sub_topic_tag = rospy.Subscriber("~tag", AprilTagsWithInfos, self.cbTag, queue_size=1)
        self.sub_trig = rospy.Subscriber("%s%s/trigger"%(self.veh_name,self.node_name),Byte, self.trigger_callback)
        self.sub_switch = rospy.Subscriber("%s%s/switch"%(self.veh_name,self.node_name),BoolStamped,self.cbSwitch)
        self.pub_detections = rospy.Publisher("~raw_led_detection", LEDDetectionArray, queue_size = 1)
        self.led_detecteds= LEDDetectionArray()
        ##Subscribe fake led signals
        self.sub_list = list()
        for car_name, car_dict in param_car_dict.items():
            #print car_name
            car_name = car_dict["name"]
            topic_name = car_dict["topic"]
            self.sub_list.append(rospy.Subscriber("%s/%s"%(car_name,topic_name), GazeboLED, self.cbEvent))
            #print "%s/%s"%(car_name,topic_name)
        self.cycle_timer = rospy.Timer(rospy.Duration.from_sec(0.3), self.cycleTimer)



    def cbSwitch(self, switch_msg): # active/inactive switch from FSM
        self.active = switch_msg.data
        if(self.active):
            self.trigger = True
            #self.sub_self = False

    def cbEvent(self, msg):
        #print msg.id
        led_detected = LEDDetection()

        #print type(msg.color)
        if msg.car == self.veh_name  and self.subself == False :
            self.intersection = msg.intersection        
            self.cross = msg.cross
            self.sub_self = True
        elif msg.car == self.veh_name  and self.subself == True:
            return
        else:
            #print(self.cross )
            if self.intersection == 'trafficLight' and msg.intersection == 'trafficLight' and msg.car == 'trafficLight':
                if (str(self.cross) + str(msg.cross)) in self.cross_dict['front']:
                    #print 'tl'
                    led_detected.color = 'g'
                    led_detected.frequency = self.lightGo
                    led_detected.pixels_normalized.y = self.label['top']-0.1
                    self.led_detecteds.detections.append(led_detected)
                                
            elif msg.intersection == self.intersection and msg.car != 'trafficLight' :          
                if (self.cross + msg.cross) in self.cross_dict['front']:
                    #print 'oveh'
                    led_detected.color = self.protocol['signals'][str(msg.color)]['color']
                    led_detected.frequency = self.protocol['signals'][str(msg.color)]['frequency']
                    led_detected.pixels_normalized.y = self.label['top']+0.1
                    led_detected.pixels_normalized.x = self.label['right']-0.1
                    self.led_detecteds.detections.append(led_detected)

                elif (self.cross + msg.cross) in self.cross_dict['right']:
                    #print 'rveh'
                    led_detected.color =  self.protocol['signals'][str(msg.color)]['color']
                    led_detected.frequency = self.protocol['signals'][str(msg.color)]['frequency']
                    led_detected.pixels_normalized.y = self.label['top']+0.1
                    led_detected.pixels_normalized.x = self.label['right']+0.1
                    self.led_detecteds.detections.append(led_detected)

            
    def trigger_callback(self, msg):
        self.trigger = True

   
    def send_state(self, msg):
        msg.state = self.node_state
        self.pub_debug.publish(msg) 
 

#    def cbTag(self, tag_msgs):
#        #if self.trigger =True:
#        self.tags_id_seen=[]
#       for taginfo in tag_msgs.infos:
#            #rospy.loginfo("[%s] taginfo." %(taginfo))
#            self.tags_id_seen.append(str(taginfo.id))
#        if len([x for x in self.tags_id_seen if x in self.intersection_dict['trafficLight'] ])!= 0:
#            #print self.tags_id_seen,self.intersection_dict['trafficLight']
#            self.intersection = 'trafficLight'
#        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign1'] ])!= 0:
#            self.intersection = 'stopSign1'
#        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign2'] ])!= 0:
#            self.intersection = 'stopSign2'  
#        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign3'] ])!= 0:
#            self.intersection = 'stopSign3'  
#        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign4'] ])!= 0:
#            self.intersection = 'stopSign4'
#        else:
#            self.intersection = ''
#        #print self.intersection


    def cycleTimer(self,event):
        
        if(self.active):
        	self.pub_detections.publish(self.led_detecteds)
        	del self.led_detecteds.detections[:]
        else:
               del self.led_detecteds.detections[:]
        
if __name__ == '__main__':
    rospy.init_node('LED_detector_node',anonymous=False)
    node = LEDDetectorNode()
    rospy.spin()

