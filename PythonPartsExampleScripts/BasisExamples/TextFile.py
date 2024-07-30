"""
Example Script for reading text from file
"""

import os
import codecs

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements

print('Load TextFile.py')

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
    element = TextFileExample(doc)
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


class TextFileExample():
    """
    Definition of class TextFileExample
    """

    def __init__(self, doc):
        """
        Initialisation of class TextFileExample

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = None
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        #------------------ Create one text element for file
        self.model_ele_list.append(self.create_text(build_ele.TextFile.value, 0, 0))
        #------------------ Return element- and handle-lists to python framework
        return (self.model_ele_list, self.handle_list)


    def create_text(self, filename, xlocation, ylocation):
        """
        Create one text element

        Args:
            filename:  Filename of text file
            xlocation: Global X coordinate for text element
            ylocation: Global Y coordinate for text element
        Return:
            Created text element
        """

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #------------------ Define Text properties
        rotation_angle                    = AllplanGeo.Angle ()
        rotation_angle.Deg                = 90

        text_prop = AllplanBasisElements.TextProperties()
        text_prop.Height                  = 4.0
        text_prop.Width                   = 4.0
        text_prop.Alignment               = AllplanBasisElements.TextAlignment.eLeftBottom
        text_prop.TextAngle               = AllplanGeo.Angle ()
        text_prop.FontAngle               = rotation_angle
        text_prop.ColumnSlopeAngle        = rotation_angle
        text_prop.LineFeed                = 2.0
        text_prop.HasBackgroundColor      = False
        text_prop.Type                    = AllplanBasisElements.TextType.eNormalText

        location = AllplanGeo.Point2D(xlocation,ylocation)

        filename = os.path.dirname(os.path.abspath(__file__)) + '\\' + filename
        print("Filename: ", filename)

        text = ""
        try:
            file = codecs.open(filename, encoding='utf-8')
            for line in file:
                text += line
        except (FileNotFoundError, IndexError, ValueError, UnicodeDecodeError):
            text += "Error reading from file"

        return AllplanBasisElements.TextElement(com_prop, text_prop, text, location)

