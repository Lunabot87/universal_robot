#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from pynput import keyboard


global mod
global t1_flag
global teach_flag
global path_angle

t1_flag = 0
teach_flag = 1
path_angle = []
mod = 'a'

def timecb(event):
	global t1_flag
	t1_flag = 1

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("manipulator")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)
rospy.Timer(rospy.Duration(1), timecb)

def teach_mode():
	global t1_flag
	global teach_flag
	global path_angle
	if t1_flag and teach_flag:
		path_angle.append(group.get_current_joint_values())
		print("save")
		t1_flag = 0

def save_mode():
	global path_angle
	f = open("save_path.txt", 'w')
	for list in path_angle:
		for i in list:
			f.write(str(i))
			f.write(",")
		f.write("\n")
	f.close()
	quit()

def end_mode():
	global mod
	global teach_flag
	global path_angle
	print(len(path_angle))
	teach_flag = 0
	mod = 's'

def check_mode(mod):
	if mod == 't':
		teach_mode()
		#time to teaching
	elif mod == 'e':
		end_mode()
	elif mod == 's':
		save_mode()
	else:
		pass

def on_release(key):
	global mod
	mod = key.char
	print(mod)
	if key == keyboard.Key.esc:
        # Stop listener
	    return False

def on_press(key):
	global mod
	try:
		mod = key
		print(mod)
	except AttributeError:
	    print('special key {0} pressed'.format(
	            key))

def main():
	global mod
	listener = keyboard.Listener( on_press=on_press, on_release=on_release)
	listener.start()
	while not rospy.is_shutdown():
		check_mode(mod)


if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass