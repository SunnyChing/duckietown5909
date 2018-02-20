#!/usr/bin/env python
import rospy
from rgb_led import *
import sys
import time
from std_msgs.msg import Float32, Int8, String
from duckietown_msgs.msg import BoolStamped, GazeboLED,AprilTagsWithInfos
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
class LEDEmitter(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        #self.pub_state = rospy.Publisher("~current_led_state",Float32,queue_size=1)
        self.sub_pattern = rospy.Subscriber("~change_color_pattern", String, self.changePattern)
        self.pub_pattern = rospy.Publisher("~emit_color_pattern",GazeboLED,queue_size=1)
        self.sub_switch = rospy.Subscriber("~switch",BoolStamped,self.cbSwitch)
        self.sub_topic_tag = rospy.Subscriber("~tag", AprilTagsWithInfos, self.cbTag, queue_size=1)
        self.sub_odom = rospy.Subscriber("odom", Odometry, self.cbOdom, queue_size=1)
        self.pub_state = rospy.Publisher("cstate", Marker, queue_size=1)
        self.cycle = None
        self.pattern = GazeboLED()
        self.is_on = False
        self.active = False

        self.protocol = rospy.get_param("~LED_protocol") #should be a list of tuples
        self.tags_id_seen=[] 
  
        self.cycle_timer = rospy.Timer(rospy.Duration.from_sec(.1), self.cycleTimer)
        self.current_pattern_name = None
        self.changePattern_('light_off')
        self.cross = ''
        self.intersection = ""
        self.cross_dict={'1':{'35','61','52','32','57'},
		  '2':{'31','58','49','41','60','66','1','71'},
		  '3':{'30','9','33','68','72','64','38'},
		  '4':{'36','62','65','70','51','63','119'},
		  }

        self.intersection_dict={'trafficLight':{'49','52','51','53','78','70','72','71'},
		  'stopSign1':{'35','61','36','9','65','30'},
		  'stopSign2':{'33','62','31','68','58'},
		  'stopSign3':{'39','63','119','41','60','67'},
		  'stopSign4':{'66','1','38','64','57'},}
        self.veh_name = rospy.get_namespace().strip("/")
        if not self.veh_name:
            # fall back on private param passed thru rosrun
            # syntax is: rosrun <pkg> <node> _veh:=<bot-id>
            if rospy.has_param('~veh'):
                self.veh_name = rospy.get_param('~veh')
        rospy.loginfo('[%s] Vehicle: %s'%(self.node_name, self.veh_name))
        self.pattern.car =self.veh_name


    def cbSwitch(self, switch_msg): # active/inactive switch from FSM
        self.active = switch_msg.data



#-----------------------------------------------------------
    def changePattern(self, msg):
        self.changePattern_(msg.data)

    def changePattern_(self, pattern_name):
        #rospy.loginfo('changePattern(%r)' % pattern_name)
        color = self.protocol['signals'][pattern_name]['color']
        self.cycle = self.protocol['signals'][pattern_name]['frequency']
        #print("color: %s, freq (Hz): %s "%(color, self.cycle))


        self.pattern.color= str(pattern_name)
        #self.pattern.id = self.tags_id_seen
        

    def cbTag(self, tag_msgs):
            #loop through list of april tags
        self.tags_id_seen=[]
        for taginfo in tag_msgs.detections:
            # rospy.loginfo("[%s] taginfo." %(taginfo))
            #print(self.get_rotation(taginfo.pose))
            if self.get_rotation(taginfo.pose) >0.3 or self.get_rotation(taginfo.pose) <-0.3 or taginfo.pose.pose.position.x >0.7:
                return
            self.tags_id_seen.append(str(taginfo.id))
           
        if len([x for x in self.tags_id_seen if x in self.cross_dict['1'] ])!= 0:
            self.cross = "1"
        elif len([x for x in self.tags_id_seen if x in self.cross_dict['2'] ])!= 0:
            self.cross = "2"
        elif len([x for x in self.tags_id_seen if x in self.cross_dict['3'] ])!= 0:
            self.cross = "3"  
        elif len([x for x in self.tags_id_seen if x in self.cross_dict['4'] ])!= 0:
            self.cross = "4"  

        else:
            self.cross = ''
        self.pattern.cross= self.cross

        if len([x for x in self.tags_id_seen if x in self.intersection_dict['trafficLight'] ])!= 0:
            #print self.tags_id_seen,self.intersection_dict['trafficLight']
            self.intersection = "trafficLight"
        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign1'] ])!= 0:
            self.intersection = "stopSign1"
        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign2'] ])!= 0:
            self.intersection = "stopSign2" 
        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign3'] ])!= 0:
            self.intersection = "stopSign3" 
        elif len([x for x in self.tags_id_seen if x in self.intersection_dict['stopSign4'] ])!= 0:
            self.intersection = "stopSign4"
        else:
            self.intersection = ""
        #print self.intersection
        self.pattern.intersection = self.intersection

    def cycleTimer(self,event):
        if True:
            self.pub_pattern.publish(self.pattern)
            #rospy.loginfo("%s in %s." %(self.pattern.car,self.pattern.color))
            text = Marker()
            text.header.frame_id = "/world"
            text.header.stamp = rospy.Time.now()
            text.ns =  self.veh_name
            text.id = 1
            text.type = 9	# text
            text.action = 0
            text.pose.position.x = self.x + 0.2
            text.pose.position.y = self.y + 0.2
            text.pose.position.z = 0.0
            text.pose.orientation.w = 1.0
            text.scale.z = 0.08
            text.color.r = 1.0		# red
            text.color.g = 1.0
            text.color.b = 0.0
            text.color.a = 1.0
            text.text = str(self.pattern.color) 
            self.pub_state.publish(text)
    def cbOdom(self,odo):
        self.x = odo.pose.pose.position.x
        self.y = odo.pose.pose.position.y

    def get_rotation (self, msg):
        orientation_q = msg.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw

if __name__ == '__main__':
    rospy.init_node('led_emitter',anonymous=False)
    node = LEDEmitter()
    rospy.spin()

