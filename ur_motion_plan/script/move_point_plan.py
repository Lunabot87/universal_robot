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

pose_target = geometry_msgs.msg.Pose()
pose_target.orientation.w = 1.0
pose_target.position.x = 0.3
pose_target.position.y = 0
pose_target.position.z = 0.4
group.set_pose_target(pose_target)
group.set_max_velocity_scaling_factor(0.6)
group.set_max_acceleration_scaling_factor(0.8)


plan1 = group.go()

rospy.sleep(5)

moveit_commander.roscpp_shutdown()