#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

class Hinge(avango.script.Script):

	## input fields
	sf_rot_value = avango.SFFloat()

	# Number of Hinge instances that have already been created.
	number_of_instances = 0
	angle = 40
	hook = None
	## constructor
	def __init__(self):
		self.super(Hinge).__init__()

		## get unique id for this instance
		self.id = Hinge.number_of_instances
		Hinge.number_of_instances += 1

	def my_constructor(self,
		PARENT_NODE = None,
		DIAMETER = 0.1, # in meter
		HEIGHT = 0.1, # in meter
		ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
		ROT_AXIS = avango.gua.Vec3(0,1,0), # the axis to rotate arround with the rotation input (default is head axis)        
		SF_ROT_INPUT_MAT = None
	):
		self.ROT_OFFSET_MAT = ROT_OFFSET_MAT
		self.ROT_AXIS = ROT_AXIS
		self.SF_ROT_INPUT_MAT = SF_ROT_INPUT_MAT
		_loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes
		self.matrix = avango.gua.nodes.TransformNode(Name = "Hinge")
		self.matrix.Transform.value = self.ROT_OFFSET_MAT
		PARENT_NODE.Children.value.append(self.matrix)

		angle = 90 if self.ROT_AXIS[2] == 1 else 0

		self.obj = _loader.create_geometry_from_file(
			"obj", "data/objects/cylinder.obj", 
			avango.gua.LoaderFlags.DEFAULTS)
		self.obj.Transform.value = \
			avango.gua.make_rot_mat(angle, 1, 0, 0) * \
			avango.gua.make_scale_mat(DIAMETER, HEIGHT, DIAMETER)
		self.obj.Material.value.set_uniform(
			"Color", avango.gua.Vec4(1.0, .0, .0, 1))
		self.matrix.Children.value.append(self.obj)
	
	@field_has_changed(sf_rot_value)
	def sf_rot_value_changed(self):
		pass
		self.angle += self.sf_rot_value.value * 50
		self.angle = min(max(self.angle, 
			self.SF_ROT_INPUT_MAT[0]), 
			self.SF_ROT_INPUT_MAT[1])
		self.matrix.Transform.value = self.ROT_OFFSET_MAT * \
			avango.gua.make_rot_mat(self.angle, self.ROT_AXIS)
		if self.hook != None:
			self.hook.sf_mat.value = self.hook.obj.WorldTransform.value