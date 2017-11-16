#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


class Hook(avango.script.Script):

    ## internal fields
    sf_mat = avango.gua.SFMatrix4()
 
    # constructor
    def __init__(self):
        self.super(Hook).__init__()


    def my_constructor(self,
        PARENT_NODE = None,
        SIZE = 0.1,
        TARGET_LIST = [],
        ):

        self.TARGET_LIST = TARGET_LIST

        _loader = avango.gua.nodes.TriMeshLoader()
        self.obj = _loader.create_geometry_from_file(
            "obj", "data/objects/sphere.obj", 
            avango.gua.LoaderFlags.DEFAULTS)
        self.obj.Transform.value = self.rot_mat * \
            avango.gua.make_scale_mat(SIZE, SIZE, SIZE)
        self.obj.Material.value.set_uniform(
            "Color", avango.gua.Vec4(1.0, 1.0, .0, 1))
        PARENT_NODE.Children.value.append(self.obj)
    
    @field_has_changed(sf_mat)
    def sf_mat_changed(self):
        _pos = self.sf_mat.value.get_translate() # world position of hook
        for _node in self.TARGET_LIST: # iterate over all target nodes
            _bb = _node.BoundingBox.value # get bounding box of a node
            if _bb.contains(_pos) == True: # hook inside bounding box of this node
                _node.Material.value.set_uniform(
                    "Color", avango.gua.Vec4(1.0,0.0,0.0,0.85)) # highlight color
            else:
                _node.Material.value.set_uniform(
                    "Color", avango.gua.Vec4(1.0,1.0,1.0,1.0)) # default color
       
