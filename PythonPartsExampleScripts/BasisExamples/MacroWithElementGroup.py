"""
Example Script for a window out of nested elementgroups. Creates a macroplacement or nested elementgroups
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import GeometryValidate as GeometryValidate

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from GeometryExamples.GeometryElements import GeometryElements

from PythonPart import View2D3D, PythonPart

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

def modify_element_property(build_ele, name, value):
    """
    Modify property of element

    Args:
        build_ele:  the building element.
        name:       the name of the property.
        value:      new value for property.

    Returns:
        True/False if palette refresh is necessary
    """
    # disable pylint warning for unused arguments
    del build_ele
    del name
    del value

    return True

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = MacroWithElementGroupExample(doc)

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

class MacroWithElementGroupExample():
    """
    Definition of class MacroWithElementGroupExample
    """

    def __init__(self, doc):
        """
        Initialisation of class MacroWithElementGroupExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc
        self._height = 1000.
        self._lenght = 1000.
        self._depth = 1000.
        self._casement_count = 2
        self._add_attr_price = 1
        self._guid_first_elementgroup = "3e2829d0-ab01-4347-999d-292aabe1b262"
        self._create_3d_body = True
        self._hash_value = ""
        self._python_file = ""

    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        #------------------ Extract property values
        self._height = build_ele.Height.value
        self._lenght = build_ele.Lenght.value
        self._depth = build_ele.Depth.value
        self._casement_count = build_ele.Casement_count.value
        self._add_attr_price = build_ele.Add_attr_price.value
        self._guid_first_elementgroup = build_ele.Guid_first_elementgroup.value
        
        self._surface_glas = build_ele.Surface_glas.value
        self._create_macro = build_ele.Create_macro.value
        self._hash_value = build_ele.get_hash()
        self._python_file = build_ele.pyp_file_name

        self.create_macro(build_ele)
        self.create_handles()

        return (self.model_ele_list, self.handle_list)
        
    def create_casement_object_list(self, lenght, height, frame_thickness, move_vector):
        """
            Create the elements for a casement

        Args:
            lenght
            height
            frame_thickness
            move_vector

        Returns:
            list with Allplan elements
        """
        object_list = []
        object_list =  self.create_object_list_sub_casement(lenght, height - frame_thickness, frame_thickness)

        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (move_vector)
        AllplanBaseElements.ElementTransform(matrix,object_list)

        add_attr_list_glas = []
        add_attr_list_knob = []
        
        add_attr_list_glas.append(220)#lenght 220
        add_attr_list_glas.append(((lenght - 2 * frame_thickness) /1000 )+ 0.04)#2 * 20mm Falzmass
        add_attr_list_glas.append(221)#Depth
        add_attr_list_glas.append(0.005 )#5mm thickness
        add_attr_list_glas.append(222)#Height
        add_attr_list_glas.append(((height - 3 *frame_thickness) /1000 )+ 0.04)#2 * 20mm Falzmass

        add_attr_list_glas.append(27531)
        add_attr_list_glas.append("Glaser")
        add_attr_list_glas.append(935)
        add_attr_list_glas.append("F30")#Fireresistance
        add_attr_list_glas.append(203) #Price
        price_glas = lenght / 1000 * height / 1000 * 20 #price = 20/m2
        print("price glas, lenght, height", price_glas, lenght, height)
        add_attr_list_glas.append(price_glas)
        
        add_attr_list_knob.append(27531)
        add_attr_list_knob.append("Schlosser")
        add_attr_list_knob.append(203) #Price
        add_attr_list_knob.append(10.00)

        name = 'glas'
        object_list.append(self.create_element_group_glas(name, lenght, height, frame_thickness, move_vector))
        object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("glas"), add_attr_list_glas))
        object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("glas"), add_attr_list_glas))

        name = 'knob'
        object_list.append(self.create_element_group_knob(name, lenght, height, frame_thickness, move_vector))
        object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("knob"), add_attr_list_knob))

        return object_list
        
    def create_object_list_frame(self, lenght, height, frame_thickness):
        """
        Create the frame

        Args:
            lenght:
            height:
            frame_thickness:

        Returns:
            Created objects for the frame
        """
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Color = 138

        #------------------ Define the Allplan elements for the element group
        object_list = []
        # left frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(frame_thickness, frame_thickness, height)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        object_list.append(cuboid)

        # lower frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(lenght - 2* frame_thickness, frame_thickness, frame_thickness)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(frame_thickness, 0, 0))
        
        AllplanBaseElements.ElementTransform(matrix,[cuboid])
        
        object_list.append(cuboid)

        # right frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(frame_thickness, frame_thickness, height)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)

        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(lenght - frame_thickness, 0, 0))
        AllplanBaseElements.ElementTransform(matrix,[cuboid])

        object_list.append(cuboid)

        # upper frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(lenght - 2 * frame_thickness, frame_thickness, frame_thickness)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(frame_thickness, 0, height -frame_thickness))
        AllplanBaseElements.ElementTransform(matrix,[cuboid])

        object_list.append(cuboid)

        if self._casement_count == 2:
            lenght = (self._lenght - self._depth) / 2
        else:
            lenght = (self._lenght - self._depth)
                       
        if self._casement_count > 0:
        
            add_attr_list = []
            
            add_attr_list.append(220)#lenght
            add_attr_list.append(lenght /1000 )
            add_attr_list.append(221)#Depth
            add_attr_list.append(self._depth /1000 )
            add_attr_list.append(222)#Height
            add_attr_list.append((height - frame_thickness) /1000 )            
            
            add_attr_list.append(27531)
            add_attr_list.append("Schreiner")
            add_attr_list.append(935)
            add_attr_list.append("F30")
            add_attr_list.append(203)
            price_casement = (2 * lenght /1000 + 2 * height / 1000) * 10 + 4 * 20 # 10/m + 20 for each corner
            print("price casement, lenght, height", price_casement, lenght, height)
            add_attr_list.append(price_casement)
        
            name = 'casement left'
            elementgroup = self.create_element_group_casement_left(name, lenght, self._height, self._depth)
            object_list.append(elementgroup)
            object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("casement_left"), add_attr_list))


        if self._casement_count == 2:
            name = 'casement right'
            elementgroup = self.create_element_group_casement_right(name, lenght, self._height, self._depth)
            object_list.append(elementgroup)
            object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("casement_right"), add_attr_list))

        return object_list

    def create_object_list_sub_casement (self, lenght, height, frame_thickness):
        """
            Create the elements for a casement

        Args:
            lenght:
            height:
            frame_thickness:

        Returns:
            list with Allplan elements
        """
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Color = 130

        #------------------ Define the Allplan elements for the element group
        object_list = []
        # left frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(frame_thickness, frame_thickness, height)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        object_list.append(cuboid)

        # lower frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(lenght - 2* frame_thickness, frame_thickness, frame_thickness)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(frame_thickness, 0, 0))
        
        AllplanBaseElements.ElementTransform(matrix,[cuboid])
        
        object_list.append(cuboid)

        # right frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(frame_thickness, frame_thickness, height)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)

        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(lenght - frame_thickness, 0, 0))
        AllplanBaseElements.ElementTransform(matrix,[cuboid])

        object_list.append(cuboid)

        # upper frame
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(lenght - 2 * frame_thickness, frame_thickness, frame_thickness)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop, cuboid_geo)
        
        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (AllplanGeo.Vector3D(frame_thickness, 0, height -frame_thickness))
        AllplanBaseElements.ElementTransform(matrix,[cuboid])

        object_list.append(cuboid)

        return object_list

    def create_object_list_glas(self, lenght, height, glas_thickness, frame_thickness, move_vector, move_vector_parent):
        """
        Create the glas

        Args:
            lenght:
            height:
            glas_thickness:
            frame_thickness:
            move_vector:
            move_vector_parent:
        Returns:
            Created object for the glas
        """
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Color = 6

        #------------------ Define the Allplan elements for the element group
        object_list = []
        # glas
        cuboid_geo = AllplanGeo.Polyhedron3D.CreateCuboid(lenght, glas_thickness, height)
        texture = AllplanBasisElements.TextureDefinition(self._surface_glas)
        cuboid = AllplanBasisElements.ModelElement3D(com_prop,texture, cuboid_geo)

        matrix = AllplanGeo.Matrix3D()
        matrix.Translate (move_vector_parent)
        matrix.Translate (AllplanGeo.Vector3D(frame_thickness, frame_thickness / 2, frame_thickness))
        AllplanBaseElements.ElementTransform(matrix,[cuboid])
        
        object_list.append(cuboid)

        return object_list

    def create_object_list_knob (self, lenght, height, glas_thickness, frame_thickness, move_vector, move_vector_parent):
        """
        Create the knob

        Args:
            lenght:
            height:
            glas_thickness:
            frame_thickness:
            move_vector:
            move_vector_parent:
        Returns:
            Created object for the knob
        """
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Color = 28

        #------------------ Define the Allplan elements for the element group
        object_list = []
        # horizontal part
        lenght_horiz = 50
        width = 30
        cuboid_geo_1 = AllplanGeo.Polyhedron3D.CreateCuboid( width, lenght_horiz, width)

        trans_to_ref_point_2 = AllplanGeo.Matrix3D()
        trans_to_ref_point_2.Translate(AllplanGeo.Vector3D(lenght + 1.75 * frame_thickness, frame_thickness * 1.5, height / 2))
        cuboid_geo_1 = AllplanGeo.Transform(cuboid_geo_1, trans_to_ref_point_2)

        # vertica part
        lenght_vert = 150
        cuboid_geo_2 = AllplanGeo.Polyhedron3D.CreateCuboid(width, width, lenght_vert)

        matrix = AllplanGeo.Matrix3D()
        trans_to_ref_point_1 = AllplanGeo.Matrix3D()
        trans_to_ref_point_1.Translate(AllplanGeo.Vector3D(0, lenght_horiz, width - lenght_vert))
        cuboid_geo_2 = AllplanGeo.Transform(cuboid_geo_2, trans_to_ref_point_1)
        cuboid_geo_2 = AllplanGeo.Transform(cuboid_geo_2, trans_to_ref_point_2)


        #------------------ Make union of polyhedrons
        err, polyhedron = AllplanGeo.MakeUnion(cuboid_geo_1, cuboid_geo_2)

        #------------------ Draw result body, if no error happens
        if GeometryValidate.polyhedron(err) and polyhedron.IsValid():
            object_list.append(AllplanBasisElements.ModelElement3D(com_prop, polyhedron))

        return object_list

    def create_element_group_frame(self, name, lenght, height, frame_thickness):
        """
        Create one element group

        Args:
            name:       Name of the element group 
            lenght:
            height:
            frame_thickness:
        Returns:
            Created element group
        """
        #------------------ Create some objects for element group
        elemenentgroup_object_list = self.create_object_list_frame(lenght, height, frame_thickness)

        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define common properties, take global Allplan settings

        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = name
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eUseNoSpecialSubType

        return AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list)
        
    def create_element_group_casement_left(self, name, lenght, height, frame_thickness):
        """
        Create one element group

        Args:
            name:       Name of the element group 
            lenght:
            height:
            frame_thickness:
        Returns:
            Created element group
        """
        #------------------ Create some objects for element group
        move_vector = AllplanGeo.Vector3D(frame_thickness / 2 , frame_thickness / 2, frame_thickness / 2)
        elemenentgroup_object_list = self.create_casement_object_list(lenght, height, frame_thickness, move_vector)

        #--- Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define common properties, take global Allplan settings
        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = name
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eUseNoSpecialSubType

        return AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list)

    def create_element_group_casement_right(self, name, lenght, height, frame_thickness):
        """
        Create one element group

        Args:
            name:       Name of the element group 
            lenght:
            height:
            frame_thickness:
        Returns:
            Created element group
        """
        #------------------ Create some objects for element group
        move_vector = AllplanGeo.Vector3D(lenght + frame_thickness / 2, frame_thickness / 2, frame_thickness / 2)
        elemenentgroup_object_list = self.create_casement_object_list(lenght, height, frame_thickness, move_vector)

        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define common properties, take global Allplan settings

        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = name
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eUseNoSpecialSubType

        return AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list)

    def create_element_group_glas(self, name, lenght, height, frame_thickness, move_vector_parent):
        """
        Create one element group

        Args:
            name:       Name of the element group 
            lenght:
            height:
            frame_thickness:
            move_vector_parent:
        Returns:
            Created element group
        """
        #------------------ Create some objects for element group
        move_vector = AllplanGeo.Vector3D(frame_thickness / 2, frame_thickness / 2, frame_thickness / 2)
        elemenentgroup_object_list = self.create_object_list_glas(lenght - (frame_thickness * 2), height - (frame_thickness * 3), frame_thickness / 5,  frame_thickness, move_vector, move_vector_parent)

        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define common properties, take global Allplan settings

        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = name
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eUseNoSpecialSubType

        return AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list)

    def create_element_group_knob(self, name, lenght, height, frame_thickness, move_vector_parent):
        """
        Create one element group

        Args:
            name:       Name of the element group 
            lenght:
            height:
            frame_thickness:
            move_vector_parent:
        Returns:
            Created element group
        """
        #------------------ Create some objects for element group
        move_vector = AllplanGeo.Vector3D(frame_thickness / 2, frame_thickness / 2, frame_thickness / 2)
        elemenentgroup_object_list = self.create_object_list_knob(lenght - (frame_thickness * 2), height - (frame_thickness * 3), frame_thickness / 5,  frame_thickness, move_vector, move_vector_parent)

        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define common properties, take global Allplan settings

        prop = AllplanBasisElements.ElementGroupProperties()
        prop.Name = name
        prop.ModifiableFlag = False
        prop.SubType = AllplanBasisElements.SubType.eUseNoSpecialSubType

        return AllplanBasisElements.ElementGroupElement(com_prop, prop, elemenentgroup_object_list)

    def get_elementgroup_uuid (self, elementgroup_name):
        """
        """   
        if elementgroup_name == "frame":
            return "3e2829d0-ab01-4347-999d-292aabe1b262"
            
        if elementgroup_name == "casement_left":
            return "912a0963-4854-4429-9aad-44978511fd0b"
            
        if elementgroup_name == "casement_right":
            return "0d55df9d-60a0-4568-a7a0-ffb7886c8858"

        if elementgroup_name == "glas":
            return "3684e52f-0c8c-476b-8464-f65565d586e6"

        if elementgroup_name == "knob":
            return "4e5702ab-e5b4-4f37-b83e-38fc56f0bcc5"            
                
        return "00000000-0000-0000-0000-000000000000"    

    def create_macro(self, build_ele):
        """
        Create the macro
        """
        #------------------ Define common properties, take global Allplan settings
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        add_attr_list = []
        add_attr_list.append(220)#lenght
        add_attr_list.append(self._lenght /1000 )
        add_attr_list.append(221)#Depth
        add_attr_list.append(self._depth /1000 )
        add_attr_list.append(222)#Height
        add_attr_list.append(self._height /1000 )
        add_attr_list.append(27531)
        add_attr_list.append("Schlosser")
        add_attr_list.append(935)
        add_attr_list.append("F30")
        add_attr_list.append(203)
        price_frame = (2 * self._lenght /1000 + 2 * self._height / 1000) * 10 + 4 * 30 # 100/m + 50 for each corner
        print("price frame, lenght, height", price_frame, self._lenght, self._height)
        add_attr_list.append(price_frame)

        name = 'frame' 
        elementgroup = self.create_element_group_frame(name, self._lenght,self._height, self._depth)
        macro_object_list = []
        macro_object_list.append(elementgroup)
        #macro_object_list[-1].SetAttributes(self.create_attribute_list(self.get_elementgroup_uuid("frame"), add_attr_list))
        macro_object_list[-1].SetAttributes(self.create_attribute_list(self._guid_first_elementgroup, add_attr_list))

        if(self._create_macro == True):
            ##------------------ Define macro definition
            views = [View2D3D (macro_object_list)]

            pythonpart = PythonPart ("MacroWithElementGroupExample", build_ele.get_params_list(),
                                    self._hash_value, self._python_file, views)
            self.model_ele_list = pythonpart.create()
        else:
            self.model_ele_list = macro_object_list

    def create_handles(self):
        """
        Create the window handles
        """

        #------------------ Define handles
        origin = AllplanGeo.Point3D(0, 0, 0)
        corner = AllplanGeo.Point3D(self._lenght, 0.0, 0.0)
        uppercorner = AllplanGeo.Point3D(0, 0, self._height)

        handle1 = HandleProperties("Lenght",
                                   corner,
                                   origin,
                                   [("Lenght", HandleDirection.x_dir)],
                                   HandleDirection.x_dir,
                                   True)
        self.handle_list.append(handle1)

        handle2 = HandleProperties("Height",
                                   uppercorner,
                                   origin,
                                   [("Height", HandleDirection.z_dir)],
                                   HandleDirection.z_dir,
                                   True)
        self.handle_list.append(handle2)

    def create_attribute_list(self, uuid, add_attr_list):
        """
        Creates attribute sets

        Returns:
            Attribute sets filled with attributes
        """
        #------------------ Define attributes for elements
        attr_list = []

        attr_list.append(AllplanBaseElements.AttributeString(606, uuid))
        # UUID for the elementgroup 
        
        list_len = (len(add_attr_list))
        i = 0
        
        while i < (list_len):
            attr_type = str(type(add_attr_list[i+1]))

            if (attr_type.find("str")) > 0:
                attr_list.append(AllplanBaseElements.AttributeString(add_attr_list[i], add_attr_list[i+1]))
                
            if (attr_type.find("float")) > 0:  
                if add_attr_list[i] != 203:
                    attr_list.append(AllplanBaseElements.AttributeDouble(add_attr_list[i], add_attr_list[i+1]))
                elif self._add_attr_price != 0:
                        attr_list.append(AllplanBaseElements.AttributeDouble(add_attr_list[i], add_attr_list[i+1]))                    
                
            i = i + 2            
        

        attr_set_list = []
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))

        attributes = AllplanBaseElements.Attributes(attr_set_list)
        return attributes
        

