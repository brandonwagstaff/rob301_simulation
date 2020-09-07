#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String


def publisher_node():
    cmd_pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
    r=rospy.Rate(10)

    while not rospy.is_shutdown():
        twist=Twist()
        twist.linear.x=0.1
        cmd_pub.publish(twist)
        rospy.loginfo(twist.linear.x)
        rospy.sleep(10)

    # straight_time=10
    # turn_time=10
    # t = rospy.Time.now()
    # start_time = t.to_sec()
    # while (rospy.Time.now().to_sec()-start_time <4):
	# twist=Twist()
    # 	twist.linear.x=0.25
   	# twist.angular.z=0
    #     # print("first whileloop")
	# cmd_pub.publish(twist)
    # t = rospy.Time.now()
    # start_time2 = t.to_sec()
    #
    # while (rospy.Time.now().to_sec()-start_time2 <4):
	# twist=Twist()
    # 	twist.linear.x=0
   	# twist.angular.z=0.25
    #     # print("second whileloop")
	# cmd_pub.publish(twist)
    #
    # twist.angular.z = 0
    # cmd_pub.publish(twist)
    # # print ("exist")
    rospy.sleep(10)
    pass


def main():

    try:
        rospy.init_node('lab01_motor')
        publisher_node()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
