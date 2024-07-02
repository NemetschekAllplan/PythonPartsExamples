"""
Example Script for texture mapping
"""
import os
import shutil

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load UVTextureMapping.py')

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = TextureMappingExample(doc)
    return element.create(build_ele)

def move_handle(build_ele, handle_prop, input_pnt, doc):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """
    build_ele.change_property(handle_prop, input_pnt)
    return create_element(build_ele, doc)

class TextureMappingExample():
    """
    Definition of class TextureMappingExample
    """

    def __init__(self, doc):
        """
        Initialisation of class TextureMappingExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = None
        self.document = doc

        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()

        self.texture = None

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.texture = AllplanBasisElements.TextureDefinition(build_ele.Texture.value)
        self.copy_texture_definition(build_ele.pyp_file_path, build_ele.Texture.value)

        self.create_cuboids(build_ele.UseUVMapping.value)
        return (self.model_ele_list, self.handle_list)

    def copy_texture_definition(self, surface_path, surface_file):
        """
        Copy surface files to Allplan project

        Args:
            surface_path:  Surface path which will be copied
            surface_file:  Surface file which will be copied
        """
        sourcefilesurf = surface_path + '\\' + surface_file + '.surf'
        targetfilesurf = AllplanSettings.AllplanPaths.GetCurPrjDesignPath() + surface_file + '.surf'
        sourcefileimage = surface_path + '\\' + surface_file + '.png'
        targetfileimage = AllplanSettings.AllplanPaths.GetCurPrjDesignPath() + surface_file + '.png'

        #print("Copy file :", sourcefilesurf, targetfilesurf)
        #print("Copy file :", sourcefileimage, targetfileimage)
        if os.path.exists(sourcefilesurf):
            shutil.copy(sourcefilesurf, targetfilesurf)
        if os.path.exists(sourcefileimage):
            shutil.copy(sourcefileimage, targetfileimage)

    def create_cuboids(self, use_uv_mapping):
        """
        Create a cube
        """
        texture_mapping = AllplanBasisElements.TextureMapping ()

        if use_uv_mapping:
            # define UV texture mapping for cuboid
            coords = AllplanUtil.VecDoubleList()
            coords[:] = [0.25, 0.33, 0.25, 0.66, 0.50, 0.66, 0.50, 0.33,
                         0.25, 0.33, 0.00, 0.33, 0.00, 0.66, 0.25, 0.66,
                         0.25, 0.66, 0.25, 1.00, 0.50, 1.00, 0.50, 0.66,
                         0.25, 0.00, 0.25, 0.33, 0.50, 0.33, 0.50, 0.00,
                         0.50, 0.33, 0.50, 0.66, 0.75, 0.66, 0.75, 0.33,
                         0.75, 0.33, 0.75, 0.66, 1.00, 0.66, 1.00, 0.33]

            texture_mapping = AllplanBasisElements.TextureMapping (coords)

        self.model_ele_list.append(
            AllplanBasisElements.ModelElement3D(
                self.com_prop, self.texture, texture_mapping, AllplanGeo.Polyhedron3D.CreateCuboid(1000,2000,3000)))



