#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("manipulator")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

group_variable_values = group.get_current_joint_values()

group_variable_values[0] = 1.0
group.set_joint_value_target(group_variable_values)
group.set_max_velocity_scaling_factor(0.6)
group.set_max_acceleration_scaling_factor(0.01)

plan2 = group.go()

group_variable_values[0] = 0.0
group.set_joint_value_target(group_variable_values)
group.set_max_velocity_scaling_factor(0.6)
group.set_max_acceleration_scaling_factor(0.01)

group.go()

rospy.sleep(5)

moveit_commander.roscpp_shutdown()
