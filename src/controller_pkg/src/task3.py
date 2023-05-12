#! /usr/bin/env python3

import rospy                             
from inverted_pendulum_sim.msg import ControlForce , CurrentState  
from inverted_pendulum_sim.srv import SetParams, SetParamsRequest
import math
from simple_pid import PID
import time

class Control():

    def __init__(self):

        rospy.init_node("Task2_control_balance")       
        rospy.loginfo_once("Control Node started")
    
        self.angle = 0
        self.force_object = ControlForce()
        self.force_object.force = 0.0

        ############################################

        self.sample_time = 1000

        ###########################################

        self.pid = PID(80, 0.2, 0.2, setpoint = 3.14)
        # self.pid.output_limits = (-10, 10)

        self.reset()

        ##############################################

        self.pub = rospy.Publisher('/inverted_pendulum/control_force', ControlForce, queue_size = 10)

        rospy.Subscriber('/inverted_pendulum/current_state', CurrentState, self.callback)

    def callback(self, msg):

        self.angle = msg.curr_theta
        # print(self.angle)


    def reset(self):

        rospy.wait_for_service('/inverted_pendulum/set_params')
        params_service = rospy.ServiceProxy('/inverted_pendulum/set_params', SetParams)
        params_object = SetParamsRequest()
        params_object.pendulum_mass = 2.0
        params_object.pendulum_length = 300
        params_object.cart_mass = 0.5
        params_object.theta_0 = 3.14
        params_object.theta_dot_0 = 0.0
        params_object.theta_dot_dot_0 = 0.0
        params_object.cart_x_0 = 0.0
        params_object.cart_x_dot_0 = 0.0
        params_object.cart_x_dot_dot_0 = 0.0
        result = params_service(params_object)

    def Pid(self):

        if self.angle < 0.0:
            self.angle = 2*math.pi + self.angle

        # print(self.angle)
        output = self.pid(self.angle)

        # print(output)

        self.force_object.force = output
        self.pub.publish(self.force_object)

if __name__ == "__main__":

    time.sleep(5)
    control = Control()
    rate = rospy.Rate(control.sample_time)
    while not rospy.is_shutdown():
        control.Pid()
        rate.sleep()
    