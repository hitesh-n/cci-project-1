#!/usr/bin/env python3
"""shebang to exceute code using python 2.7"""

# ----------------------------importing necessary packages------------------

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# --------------------------------------------------------------------------
# Function_brief:- pose_callback function updates current position values
# of the turtle from turtle pose rostopic when the subscriber method is used.


def pose_callback(msg):
    """updates the global variables"""
    CURRENT_POSITION.x, CURRENT_POSITION.y = msg.x, msg.y
    CURRENT_POSITION.theta = msg.theta

# -------------------------------------main function------------------------
# Function_brief:- main function is where all the conditions are
# checked and met for circular motion.


def main():
    """Returns nothing is the main function"""
    global CURRENT_POSITION
    # global Pose() class object for storing and updating turtle
    # position values
    CURRENT_POSITION = Pose()
    # local Pose() class obect for storing initial turtle position values
    # which is the final goal
    goal = Pose()

    # initialising this file as a rosnode
    rospy.init_node('turtle_revolve', anonymous=True)

    # Twist() class object to store velocity values
    vel_msg = Twist()
    # setting liner velocity 4 in x direction and angular velocity as
    # in z direction and rest is set to 0 to give anticlockwise circle
    vel_msg.linear.x = 4
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 2

    # rospy.Publisher() class object for publishing velocity data
    # through publish method to turtle velocity rostopic
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist,
                                         queue_size=10)
    velocity_publisher.publish(vel_msg)

    # subscribing for position data from turtle pose rostopic
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
    # necessary delay for updating the position values and velocity values
    rospy.sleep(0.05)
    # updating initial position to goal
    goal.x, goal.y = CURRENT_POSITION.x, CURRENT_POSITION.y
    goal.theta = CURRENT_POSITION.theta

    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

        # message to indicate that the turtle is in motion
        rospy.loginfo("Moving in a circle")
        # printing updated tutle position in x axis
        print(CURRENT_POSITION.x)

        rospy.sleep(0.05)
        if (round(CURRENT_POSITION.x, 3)-round(goal.x, 3) <= 0.1 and
                round(CURRENT_POSITION.y, 3)-round(goal.y, 3) <= 0.1 and
                abs(CURRENT_POSITION.theta)-abs(goal.theta) <= 0.1 and
                goal.theta-CURRENT_POSITION.theta != 0):
            # checking if the turtle has reached the goal position and
            # stopping it by considering a small error of 0.1
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)
            rospy.sleep(0.05)
            rospy.loginfo("Goal Reached!!!")
            break
            # ending the loop

# -----------------------------------excecuting the script-------------------
# checking for any error with try and except method.


if __name__ == '__main__':
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024)
            if(data == b'circle'):
                    main()
        
    except rospy.ROSInterruptException:
        pass
