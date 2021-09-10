#!/usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry


def get_yaw_from_quarternion(q):
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return yaw


def callback(odom_data):
    """TODO: complete the call back function for subscriber"""
    pass


def main():
    rospy.init_node("odometry_node")

    """TODO: initialize the subscriber of odometery here"""

    rospy.spin()


if __name__ == "__main__":
    main()
