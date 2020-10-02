#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String


def publisher_node():
    '''
    TODO: complete the publisher function here
    '''
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)
    
    forward_movement = Twist()
    forward_movement.linear.x = 0.1
    spin_movement = Twist()
    spin_movement.angular.z = math.pi/2
    stop_movement = Twist()
    stop_movement.linear.x = 0
    stop_movement.linear.y = 0
    stop_movement.linear.z = 0
    stop_movement.angular.x = 0
    stop_movement.angular.y = 0
    stop_movement.angular.z = 0

    counter = 0

    while not rospy.is_shutdown():
        print(counter)
        counter += 1
        if counter < 101:
            pub.publish(forward_movement)
        elif counter >= 101 and counter < 141:
            pub.publish(spin_movement)
        else:
            pub.publish(stop_movement)

        rate.sleep()

def main():

    try:
        rospy.init_node('motor')
        publisher_node()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
