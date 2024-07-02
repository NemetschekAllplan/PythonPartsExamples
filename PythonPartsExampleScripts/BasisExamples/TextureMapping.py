"""
Example Script for texture mapping
"""

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo

from BuildingElement import BuildingElement

print('Load TextureMapping.py')

def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
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

    def __init__(self, doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class TextureMappingExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list    = None
        self.document       = doc

        self.com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()


    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """

        local_name = "PythonPartExamples\\TextureMapping"

        surface_path = AllplanSettings.AllplanPaths.GetCurPrjPath() + "design"


        #----------------- cube with selected surface

        self.create_cube3d(build_ele)


        #----------------- cube with color

        self.create_wall_cube3d(build_ele, surface_path, local_name)


        #----------------- with transparency

        self.create_roof3d(build_ele, surface_path, local_name)


        #----------------- with reflection

        self.create_ellipsoid3d(build_ele, surface_path, local_name)


        #----------------- with glance

        self.create_cylinder3d(build_ele, surface_path, local_name)

        self.create_cone3d(build_ele, surface_path, local_name)

        return (self.model_ele_list, self.handle_list)


    def create_cube3d(self, build_ele: BuildingElement):
        """
        Create a cube
        """

        cube = AllplanGeo.Polyhedron3D.CreateCuboid(1000, 2000, 3000)

        cube_texture = AllplanBasisElements.TextureDefinition(build_ele.Texture.value)

        mapping_angle  = AllplanGeo.Angle()

        mapping_angle.Deg = build_ele.MappingAngle.value

        mapping = AllplanBasisElements.TextureMapping ()

        mapping.MappingType   = self.mapping_type_converter(build_ele.MappingType.value)
        mapping.MappingAngle  = mapping_angle.Rad
        mapping.XScale        = build_ele.XScale.value
        mapping.YScale        = build_ele.YScale.value
        mapping.XOffset       = build_ele.XOffset.value
        mapping.YOffset       = build_ele.YOffset.value
        mapping.ReferenceFace = build_ele.ReferenceFace.value
        mapping.ReferenceEdge = build_ele.ReferenceEdge.value

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, cube_texture, mapping, cube))


    def create_wall_cube3d(self,
                           build_ele   : BuildingElement,
                           surface_path: str,
                           local_name  : str):
        """
        Create a wall cube
        """

        surface = AllplanBasisElements.SurfaceDefinition.Create()

        surface.DiffuseColor = AllplanBasisElements.ARGB(build_ele.ColorID.value)

        unique_name = AllplanBaseElements.DocumentResourceService.CreateSurface(self.document, surface_path, local_name, surface)

        wall = AllplanGeo.Polyhedron3D.CreateCuboid(AllplanGeo.Point3D(2000, 0, 0),
                                                    AllplanGeo.Point3D(5000,300,2000))

        texture = AllplanBasisElements.TextureDefinition(unique_name)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, texture, wall))


    def create_roof3d(self,
                      build_ele   : BuildingElement,
                      surface_path: str,
                      local_name  : str):
        """
        Create a wedge
        """
        rail = AllplanGeo.Line3D(0, 0, 0, 0, 1000, 0)

        polyline = AllplanGeo.Polyline3D()
        polyline += AllplanGeo.Point3D(-2000, 0, 0)
        polyline += AllplanGeo.Point3D(-1500, 0, 3000)
        polyline += AllplanGeo.Point3D(-1000, 0, 0)
        polyline += AllplanGeo.Point3D(-2000, 0, 0)

        err, brep = AllplanGeo.CreateSweptBRep3D(polyline,rail, False, None)

        if err or not brep.IsValid:
            return

        surface = AllplanBasisElements.SurfaceDefinition.Create()

        surface.DiffuseColor      = AllplanBasisElements.ARGB(build_ele.TransparentColorID.value)
        surface.ColorKey          = AllplanBasisElements.ARGB(255, 255, 255, 0)
        surface.ColorKeyTolerance = 255
        surface.Transparency      = build_ele.Transparency.value
        surface.Refraction        = build_ele.Refraction.value
        surface.Roughness         = build_ele.Roughness.value

        unique_name = AllplanBaseElements.DocumentResourceService.CreateSurface(self.document, surface_path, local_name, surface)

        texture = AllplanBasisElements.TextureDefinition(unique_name)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, texture, brep))


    def create_ellipsoid3d(self,
                           build_ele   : BuildingElement,
                           surface_path: str,
                           local_name  : str):
        """
        Create an ellipsoid
        """

        ellipsoid = AllplanGeo.Ellipsoid3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(6500, 0, 0)), 500, 500, 500)

        surface = AllplanBasisElements.SurfaceDefinition.Create()

        surface.DiffuseColor        = AllplanBasisElements.ARGB(build_ele.ColorID.value)
        surface.DiffuseReflectivity = build_ele.DiffuseReflection.value

        unique_name = AllplanBaseElements.DocumentResourceService.CreateSurface(self.document, surface_path, local_name, surface)

        texture = AllplanBasisElements.TextureDefinition(unique_name)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, texture, ellipsoid))


    def create_cylinder3d(self,
                           build_ele   : BuildingElement,
                           surface_path: str,
                           local_name  : str):
        """
        Create a cylinder
        """

        cylinder = AllplanGeo.Cylinder3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(8000, 0, 0)),
                                         500, 500, AllplanGeo.Point3D(0, 0, 1000))

        surface = AllplanBasisElements.SurfaceDefinition.Create()

        surface.DiffuseColor        = AllplanBasisElements.ARGB(build_ele.ColorID.value)
        surface.DiffuseReflectivity = 0
        surface.Reflection          = build_ele.GlossyReflection.value

        unique_name = AllplanBaseElements.DocumentResourceService.CreateSurface(self.document, surface_path, local_name, surface)

        texture = AllplanBasisElements.TextureDefinition(unique_name)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, texture, cylinder))


    def create_cone3d(self,
                      build_ele   : BuildingElement,
                      surface_path: str,
                      local_name  : str):
        """
        Create a cone
        """

        cone = AllplanGeo.Cone3D(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(6000, 4000, 0)),
                                 1000, 200, AllplanGeo.Point3D(0, 0, 1000))

        surface = AllplanBasisElements.SurfaceDefinition.Create()

        surface.DiffuseColor        = AllplanBasisElements.ARGB(build_ele.ColorID.value)
        surface.DiffuseReflectivity = 0
        surface.Emission            = build_ele.Lumiance.value

        unique_name = AllplanBaseElements.DocumentResourceService.CreateSurface(self.document, surface_path, local_name, surface)

        texture = AllplanBasisElements.TextureDefinition(unique_name)

        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, texture, cone))


    @staticmethod
    def mapping_type_converter(argument):
        """
        Converter for mapping type
        """
        switcher = {
            "eCube"    : AllplanBasisElements.TextureMappingType.eCube,
            "eWall"    : AllplanBasisElements.TextureMappingType.eWall,
            "eRoof"    : AllplanBasisElements.TextureMappingType.eRoof,
            "eGround"  : AllplanBasisElements.TextureMappingType.eGround,
            "eCylinder": AllplanBasisElements.TextureMappingType.eCylinder,
            "eSphere"  : AllplanBasisElements.TextureMappingType.eSphere,
            }
        return switcher.get(argument, 1)
