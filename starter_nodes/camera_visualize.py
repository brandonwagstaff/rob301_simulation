#!/usr/bin/env python

'''
line sensor: get the index of the lowest intensity value, and publish to 'color_mono'
'''

import roslib
import sys
import rospy
import numpy as np
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import matplotlib.pyplot as plt

class camera_vis(object):
    def __init__(self):
        self.camera_subscriber = rospy.Subscriber('/camera/rgb/image_raw', Image, self.camera_callback, queue_size = 1)
    
    def camera_callback(self,data):
        bridge = CvBridge()
        try:
            cv_img = bridge.imgmsg_to_cv2(data, "mono8")
            rgb_cv_img = bridge.imgmsg_to_cv2(data, "rgb8")
            #print(cv_img.shape)
        except CvBridgeError as e:
            print(e)


        plt.imshow(rgb_cv_img)
        plt.savefig('rgb_cv_img.png')           
        return


def main():
    rospy.init_node('camera_vis')
    Camera = camera_vis()
    rospy.spin()


if __name__ == '__main__':
    main()
