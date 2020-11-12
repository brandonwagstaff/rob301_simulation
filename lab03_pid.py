#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

e = """
Communications Failed
"""

def getKey(): #you can ignore this function. It's for stopping the robot when press 'Ctrl+C'
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key



class PIDcontrol():
    def __init__(self):
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.color_sub = rospy.Subscriber('line_idx', String, self.camera_callback, queue_size=1)
        # initialize class variable that updates in camera_callback 
	self.actual = 320	

    def camera_callback(self, data):
       	self.actual = int(data.data)
        pass


    def follow_the_line_BangBang(self):
	desired = 320
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
	    actual = self.actual
	    error = desired - actual
	    twist = Twist()
	    twist.linear.x = 0.1
	    if error < 0: 
		twist.angular.z = - 0.575 
	    elif error > 0:
		twist.angular.z = 0.575
	    else:
	        twist.angular.z = 0

	    self.cmd_pub.publish(twist)
	    rate.sleep()	
        pass

    def follow_the_line_P(self):
        desired = 320
	rate = rospy.Rate(10)
	k_p = 0.0025
	while not rospy.is_shutdown():
	    actual = self.actual
	    error = desired - actual
	    twist = Twist()
	    twist.linear.x = 0.1
	    twist.angular.z = (k_p * error)
	    self.cmd_pub.publish(twist)
	    rate.sleep()	
        pass

    def follow_the_line_PI(self):
        desired = 320
	integral = 0
	rate = rospy.Rate(10)
	k_p = 0.0025
	k_i = 0.00005
	while not rospy.is_shutdown():
	    actual = self.actual
	    error = desired - actual
	    integral = integral + error
	    twist = Twist()
	    twist.linear.x = 0.1
	    twist.angular.z = (k_p * error) + (k_i * integral)
	    self.cmd_pub.publish(twist)
	    rate.sleep()	
        pass

    def follow_the_line_PID(self):
        desired = 320
	integral = 0
        derivative = 0
        lasterror = 0
	rate = rospy.Rate(10)
	k_p = 0.0025    # 0.0025
	k_i = 0.00005   # 0.00005
        k_d = 0.001    # 0.001
	while not rospy.is_shutdown():
	    actual = self.actual
	    error = desired - actual
	    integral = integral + error
  	    derivative = error - lasterror
	    twist = Twist()
	    twist.linear.x = 0.1
	    twist.angular.z = (k_p * error) + (k_i * integral) + (k_d * derivative)
 	    lasterror = error
	    self.cmd_pub.publish(twist)
	    rate.sleep()	
        pass



if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
         
    rospy.init_node('Lab3')
    PID = PIDcontrol()
    try:
        while(1):
            key = getKey()
            PID.follow_the_line_PID()
            if (key == '\x03'): #stop the robot when exit the program
                break
    except rospy.ROSInterruptException:
        print("comm failed")


