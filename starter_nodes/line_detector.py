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

class camera_mono(object):
    def __init__(self):
        self.line_sensor_publisher = rospy.Publisher('line_idx', String ,queue_size=1)
        self.color_sensor_publisher = rospy.Publisher('camera_rgb', String ,queue_size=1)
        self.camera_subscriber = rospy.Subscriber('/camera/rgb/image_raw', Image, self.camera_callback, queue_size = 1)
    
    def camera_callback(self,data):
        bridge = CvBridge()
        try:
            cv_img = bridge.imgmsg_to_cv2(data, "mono8")
            rgb_cv_img = bridge.imgmsg_to_cv2(data, "rgb8")
            #print(cv_img.shape)
        except CvBridgeError as e:
            print(e)

        #publish the line sensor reading
        array = cv_img
        mid = len(array)//2
        line_array = array[300:400]
        line_array = np.mean(line_array, axis=0)
        new_array = []
        for i in range(5,len(line_array)-6):
            new_array.append(np.mean(line_array[i-5:i+5]))
        index = np.argmin(new_array)
        self.line_sensor_publisher.publish(str(index))

        #publish to camera rgb
        color_array = rgb_cv_img[:200,:]
        intermediate=np.mean(color_array, axis=0)
        color=np.mean(intermediate, axis=0)
        # rospy.loginfo('r:{}, g:{}, b:{}'.format(color[0], color[1], color[2]))
        self.color_sensor_publisher.publish('r:{}, g:{}, b:{}'.format(color[0], color[1], color[2]))             
        return


def main():
    rospy.init_node('camera_mono')
    Camera = camera_mono()
    rospy.spin()


if __name__ == '__main__':
    main()
