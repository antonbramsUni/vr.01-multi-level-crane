#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua

class Arm:

	# Number of Arm instances that have already been created.
	number_of_instances = 0
	
	## constructor
	def __init__(self,
		PARENT_NODE = None,
		DIAMETER = 0.1, # in meter
		LENGTH = 0.1, # in meter
		ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
	):

		self.id = Arm.number_of_instances
		Arm.number_of_instances += 1
		self.length = LENGTH

		_loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes
		
		self.obj = _loader.create_geometry_from_file(
			"obj", "data/objects/cylinder.obj", 
			avango.gua.LoaderFlags.DEFAULTS)
		self.obj.Transform.value = \
			avango.gua.make_trans_mat(.0,LENGTH/2,.0) * \
			avango.gua.make_scale_mat(DIAMETER, LENGTH, DIAMETER)
		self.obj.Material.value.set_uniform(
			"Color", avango.gua.Vec4(.5, .5, .5, 1.))

		PARENT_NODE.Children.value.append(self.obj)
	