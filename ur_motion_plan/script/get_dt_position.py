#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

global t1_flag
global t1_count
global save_path
global mod
mod = 't'
save_path = []
t1_flag = 0
t1_count = 0

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("manipulator")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

def timecb(event):
	global t1_count
	global t1_flag
	t1_flag = 1
	rospy.sleep(1)

def teach_mode():
	global t1_flag
	global t1_count
	global mod
	global save_path
	rospy.Timer(rospy.Duration(2.0), timecb)
	if t1_flag and t1_count <= 10:
		save_path.append(group.get_current_joint_values())
		t1_count = 1 + t1_count
		print(t1_count)
		t1_flag = 0
	if t1_count > 10:
		print(len(save_path))
		rospy.sleep(10)
def end_mode():
	wait(1000)

def check_mode(mod):
	while not rospy.is_shutdown():
		if mod == 't':
			teach_mode()
			#time to teaching
		elif mod == 'e':
			end_mode()
		else:
			pass

if __name__ == "__main__":
	try:
		global mod
		check_mode(mod)
	except rospy.ROSInterruptException:
		pass

