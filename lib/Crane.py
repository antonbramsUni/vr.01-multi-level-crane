#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.Arm import Arm
from lib.Hook import Hook


class Crane:
  
	## constructor
	def __init__(self,
		PARENT_NODE = None,
		TARGET_LIST = [],
	):
		## init internal sub-classes
		self.input = KeyboardInput()
		# b.Input.connect_from(a.Output)
		## init base node for whole crane
		self.base_node = avango.gua.nodes.TransformNode(
			Name = "base_node")
		self.base_node.Transform.value = \
			avango.gua.make_trans_mat(.0, -.1,.0)
		PARENT_NODE.Children.value.append(self.base_node)

		# rotational axises
		rotAxi0 = avango.gua.Vec3(0,1,0)
		rotAxi1 = avango.gua.Vec3(0,0,1)
		# FIRST
		hinge0 = Hinge()
		hinge0.my_constructor(
			self.base_node, .1, .01, 
			avango.gua.make_identity_mat(), 
			rotAxi0, 
			[-180, 180])
		hinge0.sf_rot_value.connect_from(self.input.sf_rot_input0)
		arm0 = Arm(hinge0.matrix, .01, .1, avango.gua.make_identity_mat())
		# SECOND
		rotMat1 = avango.gua.make_identity_mat() * \
			avango.gua.make_trans_mat(.0, arm0.length, .0)
		hinge1 = Hinge()
		hinge1.my_constructor(
			hinge0.matrix, .02, .01, 
			rotMat1, rotAxi1,
			[0, 90])
		hinge1.sf_rot_value.connect_from(self.input.sf_rot_input1)
		arm1 = Arm(hinge1.matrix, .005, .08, rotMat1)
		# THIRD
		rotMat2 = avango.gua.make_identity_mat() * \
			avango.gua.make_trans_mat(.0, arm1.length, .0)
		hinge2 = Hinge()
		hinge2.my_constructor(
			hinge1.matrix, .02, .01, 
			rotMat2, rotAxi1,
			[-90, 90])
		hinge2.sf_rot_value.connect_from(self.input.sf_rot_input2)
		arm2 = Arm(hinge2.matrix, .005, .08, rotMat2)
		# FOURTH
		hook = Hook()
		hook.rot_mat = avango.gua.make_identity_mat() * \
			avango.gua.make_trans_mat(.0, arm2.length, .0)
		hook.my_constructor(hinge2.matrix, .02, TARGET_LIST)
		hinge0.hook = hook
		hinge1.hook = hook
		hinge2.hook = hook
					 
		