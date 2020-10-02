#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry

class Pose:
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta

    def update(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

curr_pose = Pose()

def publisher_node():
    global curr_pose

    vel_factor = 0.1
    ang_factor = 0.5
    target1 = [Pose(2, .5, 135/180*math.pi)]
    target_index = 0

    cmd_twist = Twist()

    stop_movement = Twist()
    stop_movement.linear.x = 0
    stop_movement.linear.y = 0
    stop_movement.linear.z = 0
    stop_movement.angular.x = 0
    stop_movement.angular.y = 0
    stop_movement.angular.z = 0
    
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        vel_mag = min(0.26, vel_factor*((target1[target_index].x - curr_pose.x)**2 \
            + (target1[target_index].y - curr_pose.y)**2)**0.5)

        ang_vel = max(-1.28, min(1.28, ang_factor*math.degrees(target1[target_index].theta - curr_pose.theta)))

        rospy.loginfo(ang_vel)

        cmd_twist.linear.x = vel_mag
        cmd_twist.angular.z = ang_vel

        pub.publish(cmd_twist)

        rate.sleep()

def get_yaw_from_quarternion(q):
	siny_cosp = 2*(q.w*q.z + q.x*q.y)
	cosy_cosp=1-2*(q.y*q.y+q.z*q.z)
	yaw=math.atan(siny_cosp/cosy_cosp)
	return yaw

def callback(odom_data):
    global curr_pose

    point = odom_data.pose.pose.position 
    quart = odom_data.pose.pose.orientation 
    theta = get_yaw_from_quarternion(quart)
    cur_pose = (point.x, point.y, theta) 
    # rospy.loginfo(cur_pose)

    curr_pose.update(point.x, point.y, theta)

def main():
    try:
        rospy.init_node('lab02')

        rate = rospy.Rate(10) 
        listen = rospy.Subscriber('odom', Odometry, callback, queue_size=1)

        publisher_node()

        rate.sleep()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()