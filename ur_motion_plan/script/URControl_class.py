#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from pynput import keyboard
from sensor_msgs.msg import JointState


class UR_CONTROL:

	def timecb(self,event):
		self.t1_flag = 1

	def on_press(self,key):
		try:
			self.mod = key.char
			print("press")
		except AttributeError:
			print('special key {0} pressed but is not use'.format(key))


	def __init__(self):
		self.t1_flag = 0
		self.teach_flag = 0
		self.path_angle = []
		self.mod = ''
		self.vel = []

		#if you use to code, you must be change file path!
		self.file_path = "/home/parallels/catkin_ws/src/universal_robot/ur_motion_plan/script/save_path.txt"
		moveit_commander.roscpp_initialize(sys.argv)
		rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
		robot = moveit_commander.RobotCommander()
		scene = moveit_commander.PlanningSceneInterface()
		self.group = moveit_commander.MoveGroupCommander("manipulator")
		self.group.set_max_velocity_scaling_factor(0.6)
		self.group.set_max_acceleration_scaling_factor(0.8)
		self.group.set_num_planning_attempts(2)
		self.group.set_planning_time(0.05)
		display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)
		rospy.Timer(rospy.Duration(0.1), self.timecb)
		listener = keyboard.Listener(on_press=self.on_press)
		listener.start()


	def teach_mode(self):
		self.teach_flag = 1
		if self.t1_flag and self.teach_flag:
			temp_vel = rospy.wait_for_message("joint_states", JointState)
			self.path_angle.append(temp_vel.position)
			self.vel.append(temp_vel.velocity)
			self.t1_flag = 0
			print("check")

	def save_mode(self):
		with open(self.file_path, 'w') as f:
			for list in self.path_angle:
				count = 0
				for i in list:
					if (count < 5):
						f.write(str(i)+',')
					else:
						f.write(str(i))
					count += 1
				f.write("\n")
			print("save_finish")
			self.mod = 'sv' #wait mode

	def save_mode_v(self):
		with open("/home/parallels/catkin_ws/src/universal_robot/ur_motion_plan/script/save_vel.txt", 'w') as f:
			for list in self.vel:
				count = 0
				for i in list:
					if (count < 5):
						f.write(str(i)+',')
					else:
						f.write(str(i))
					count += 1
				f.write("\n")
			print("save_vel")
			self.mod = 'w' #wait mode

	def read_mode(self):
		self.path_angle = []
		with open(self.file_path, 'r') as f:
			for line in f:
				self.path_angle.append(map(float,line.strip().split(',')))

	def end_mode(self):
		self.teach_flag = 0
		#print(self.vel)
		self.mod = 'w'

	def wait_mode(self):
		pass

	def move_mode(self):
		try:
			for path in self.path_angle:
				test = self.group.plan()
				self.group.set_joint_value_target(path)
				self.group.go(wait = True)
			self.mod = 'w'
			print("move_finish")
		except KeyboardInterrupt:
			raise


	def check_mode(self,mod):
		if mod == 't':
			self.teach_mode()
		elif mod == 'e':
			self.end_mode()
		elif mod == 's':
			self.save_mode()
		elif mod == 'sv':
			self.save_mode_v()
		elif mod == 'r':
			self.read_mode()
		elif mod == 'w':
			self.wait_mode()
		elif mod == 'm':
			self.move_mode()
		else:
			pass

	def main(self):
		while not rospy.is_shutdown():
			self.check_mode(self.mod)

if __name__ == "__main__":
	try:
		ur3 = UR_CONTROL()
		ur3.main()
	except rospy.ROSInterruptException:
		pass