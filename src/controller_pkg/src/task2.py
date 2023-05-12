#! /usr/bin/env python3

import rospy                             
from inverted_pendulum_sim.msg import ControlForce   
from inverted_pendulum_sim.srv import SetParams, SetParamsRequest     
import math

class Publisher():

    def __init__(self):

        rospy.init_node("Task2_control_input")       
        rospy.loginfo_once("Control Node Initialized")
        
        self.pub = rospy.Publisher('/inverted_pendulum/control_force', ControlForce, queue_size = 10)

        self.time = 0
        self.force_object = ControlForce()
        self.force_object.force = 0.0
      
        self.frequency = 1
        self.amplitude = 1
        self.change_amp = 5
        self.change_freq = 10
        self.smaple_time = 10
        self.count = 0
        self.toggle = False
     
    def change_amplitude(self):

        if self.amplitude >= 0 and self.amplitude <= 20:
            self.amplitude = self.amplitude + self.change_amp
        else:
            self.toggle = False
            self.frequency = 1
    
    def change_frequency(self):

        if self.frequency >= 0 and self.frequency <= 20:
            self.frequency = self.frequency + self.change_freq
        else:
            self.toggle = True
            self.amplitude = 1
            
    def main(self):

        self.pub.publish(self.force_object)
        self.time += 0.001
        self.force_object.force = self.amplitude * \
                math.sin(2 * math.pi * self.frequency * self.time) 
        
        rospy.loginfo(f"Current Amplitude And Frequency: {self.amplitude} and {self.frequency}")

        if self.count > 50:
            if self.toggle == True:
                self.change_amplitude()
            else:
                self.change_frequency()
            self.count = 0        
        else:
            self.count = self.count + 1

if __name__ == "__main__":

    publisher = Publisher()
    rate = rospy.Rate(publisher.smaple_time)
    while not rospy.is_shutdown():
        publisher.main()
        rate.sleep()