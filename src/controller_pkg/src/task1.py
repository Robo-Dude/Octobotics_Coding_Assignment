#! /usr/bin/env python3

import rospy
from inverted_pendulum_sim.srv import SetParams, SetParamsRequest

def client():

    rospy.init_node('task1_client')
    rospy.wait_for_service('/inverted_pendulum/set_params')

    try:
        params_service = rospy.ServiceProxy('/inverted_pendulum/set_params', SetParams)
        params_object = SetParamsRequest()
        params_object.pendulum_mass = 2.0
        params_object.pendulum_length = 300
        params_object.cart_mass = 0.5
        params_object.theta_0 = 0.0
        params_object.theta_dot_0 = 0.0
        params_object.theta_dot_dot_0 = 0.0
        params_object.cart_x_0 = 0.0
        params_object.cart_x_dot_0 = 0.0
        params_object.cart_x_dot_dot_0 = 0.0
        result = params_service(params_object)
        return result

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    print(client())
