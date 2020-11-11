#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np
import re
import sys, select, os

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

def getKey():
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


class BayesLoc:

    def __init__(self, P0, colourCodes,colourMap, transProbBack, transProbForward):
        self.colour_sub = rospy.Subscriber('camera_rgb', String, self.colour_callback)
        self.cmd_pub= rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self.probability = P0
        self.colourCodes = colourCodes
        self.colourMap = colourMap
        self.transProbBack = transProbBack
        self.transProbForward = transProbForward
        self.numStates = len(P0)
        self.statePrediction = np.zeros(np.shape(P0))

        self.CurColour = None
        self.curPos=0
  
        self.colorProbs = None

 
    def colour_callback(self, msg):
        rgb = msg.data.replace('r:','').replace('b:','').replace('g:','').replace(' ','')
        r,g,b = rgb.split(',')
        r,g,b=(float(r), float(g),float(b))
        self.CurColour = np.array([r,g,b])
    

    def waitforcolour(self):
        while(1):
            if self.CurColour is not None:
                break

    def getSensorReading(self):
        if self.CurColour is None:
            self.waitforcolour()
        dist = np.linalg.norm(self.colourCodes-self.CurColour,axis = 1)
        dist += np.ones(np.shape(dist))*.01
        prob = dist**-1
        prob = prob/np.sum(prob)
        return prob

    def go_forward_one_grid(self):
        rospy.loginfo('going forward one grid')
        """
        TODO: Complete this function to move forward by one grid (75cm)
        """
    

    def stop(self):
        twist = Twist()
        self.cmd_pub.publish(twist)
        

    def statePredict(self,forward):
        rospy.loginfo('predicting state')
        '''
        TODO: Complete this function by updating self.statePrediction
        '''

    def stateUpdate(self):
        rospy.loginfo('updating state')
        '''
        TODO: Complete this function by updating self.probability
        '''
            


if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    # 0: Green, 1: Purple, 2: Orange, 3: Yellow, 4: Line   
    color_maps = [0, 1, 2, 2, 0, 1, 2, 3, 0, 1, 3]
    color_codes = [[72, 255, 72], #green
                    [255, 144, 0], #orange
                    [145,145,255], #purple
                    [255, 255, 0], #yellow 
                    [133,133,133]] #line
                 
    rospy.init_node('final_project')
    bayesian=BayesLoc([1.0/len(color_maps)]*len(color_maps), color_codes, color_maps, [0.2,0.8],[0.1,0.9])
    prob = []
    rospy.sleep(0.5)    
    state_count = 0
    
    prev_state=None
    try:
        
        while (1):
            key = getKey()
            if (key == '\x03'): #1.22:bayesian.curPos >= 1.6 or
                rospy.loginfo('Finished!')
                rospy.loginfo(prob)
                break
            
            bayesian.colorProbs = bayesian.getSensorReading()

            if np.argmax(bayesian.colorProbs) == 4:
                if prev_state !='line':
                    rospy.loginfo('Doing line following now...')
                '''
                TODO: call PID line following function
                '''
                prev_state = 'line'
                
            else:         
                bayesian.stop()
                rospy.loginfo('doing state estimate now...')
                rospy.sleep(3)

                '''
                TODO: call state estimation function. Complete the bayesian.go_forward function to move
                forward for one grid.
                '''
                bayesian.go_forward_one_grid()   
                bayesian.stop()
                state_count += 1
                rospy.sleep(3)
                prev_state='color'
                
    except Exception as e:
        print("comm failed:{}".format(e))

    finally:
        rospy.loginfo(bayesian.probability)
        cmd_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        twist = Twist()
        cmd_publisher.publish(twist)





