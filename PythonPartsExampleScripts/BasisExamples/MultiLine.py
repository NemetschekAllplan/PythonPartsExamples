"""
Example Script for MultiLine ElementGroup
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements


print('Load MultiLine ElementGroup.py')


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
    element = MultiLineElementGroupExample(doc)
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


class MultiLineElementGroupExample():
    """
    Definition of class MultiLineElementGroupExample
    """

    def __init__(self, doc):
        """
        Initialisation of class MultiLineElementGroupExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.create_geometry(build_ele)
        return (self.model_ele_list, self.handle_list)

    def move_polygon(self, polygon):
        """
        Create the element geometries

        Args:
            polygon:  polygon which is translated
        """
        translation = AllplanGeo.Matrix2D()
        translation.Translate(AllplanGeo.Vector2D(1500, 0))
        polygon = AllplanGeo.Transform(polygon, translation)
        return polygon

    def create_geometry(self, build_ele):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define the Allplan elements for the element group
        elemenentgroup_object_list = []

        count = build_ele.Count.value
        for ind in range (1, count+1):
            # define a line 3D element
            line_list = []
            point1 = AllplanGeo.Point3D(0, 0, float(ind*100))
            point2 = AllplanGeo.Point3D(1000, 0, float(ind*100))
            line = AllplanGeo.Line3D(point1,point2)
            line_list.append(AllplanBasisElements.ModelElement3D(com_prop, line))

            # create one element group holding a line 3D
            prop = AllplanBasisElements.ElementGroupProperties()
            prop.Name = "ID" + str(ind)
            prop.ModifiableFlag = False
            prop.SubType = AllplanBasisElements.SubType.eMultiLine3D
            elemenentgroup_object_list.append(AllplanBasisElements.ElementGroupElement(com_prop, prop, line_list))

        #------------------ Define element group holding all other element groups

        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = build_ele.Name.value
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eMultiLine3D_Group
        self.model_ele_list.append(AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list))



