#!/usr/bin/env python

import sys
import rospy
from navigation.srv import *

def graph_search_client():
    print 'fa'
    rospy.wait_for_service('graph_search')
    print 'fa'
    try:
        graph_search = rospy.ServiceProxy('graph_search', GraphSearch)
        resp = graph_search('I15', 'I26')
        return resp.actions
        
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    print "%s"%(graph_search_client())
