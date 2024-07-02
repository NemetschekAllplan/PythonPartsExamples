"""
Example Script for MacroPlacements
"""

import hashlib as hashlib

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Precast as AllplanPrecast

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


def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = FixturePointPlacementExample(doc)

    return element.create(build_ele)


class FixturePointPlacementExample():
    """
    Definition of class FixturePointPlacementExample
    """

    def __init__(self, doc):
        """
        Initialization of class FixturePointPlacementExample

        Args:
            doc: input document
        """
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc


    def create(self, build_ele):
        """
        Create the elements

        Returns:
            tuple  with created elements and handles.
        """
        # define macro definition
        
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()

        #-------------------- create the geometry

        length = build_ele.PlateLength.value
        width  = build_ele.PlateWidth.value
        height = build_ele.PlateHeight.value

        y = build_ele.FixtureHeight.value - height 

        plate1 = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-length / 2, -width / 2, 0)), length, width, height)
        plate2 = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-length / 2, -width / 2, y)), length, width, height)

        y -= height

        bar1 = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(-length / 6, 0, height)), build_ele.BarDiameter.value, y)
        bar2 = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(length / 6, 0, height)), build_ele.BarDiameter.value, y)

        slide_elements = [AllplanBasisElements.ModelElement3D(com_prop, plate1),
                          AllplanBasisElements.ModelElement3D(com_prop, plate2),
                          AllplanBasisElements.ModelElement3D(com_prop, bar1),
                          AllplanBasisElements.ModelElement3D(com_prop, bar2)]


        #-------------------- create the fixture slide
        
        slides = []
       
        slide_prop = AllplanPrecast.FixtureSlideProperties()

        slide_prop.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        slide_prop.VisibilityGeo3D = True
        slide_prop.VisibilityGeo2D = False

        slides.append(AllplanPrecast.FixtureSlideElement(slide_prop, slide_elements))


        #-------------------- create the fixture

        fixture_prop = AllplanPrecast.FixtureProperties()

        fixture_prop.Type = AllplanPrecast.MacroType.ePoint_Fixture
        fixture_prop.SubType =AllplanPrecast.MacroSubType.eConnectorEBT
        fixture_prop.Name = "Connector"

        fixture = AllplanPrecast.FixtureElement(fixture_prop, slides)

        fixture.SetHash(hashlib.sha224(str(fixture).encode('utf-8')).hexdigest())


        #-------------------- create the fixture placement
        
        fixture_placement_prop = AllplanPrecast.FixturePlacementProperties()

        fixture_placement_prop.Name = "Connector"
        fixture_placement_prop.OutlineType = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_NO_AFFECT

        fixture_placement = AllplanPrecast.FixturePlacementElement(com_prop,fixture_placement_prop, fixture)

        #views = [View2D3D([AllplanBasisElements.ModelElement3D(com_prop, AllplanGeo.Line3D(0, 0, 0, 1000, 0, 0))])]

        #pythonpart = PythonPart ("FixtureExample",
        #                         parameter_list   = build_ele.get_params_list(),
        #                         hash_value       = build_ele.get_hash(),
        #                         python_file      = build_ele.pyp_file_name,
        #                         views            = views,
        #                         fixture_elements = [fixture_placement])

        self.model_ele_list = [fixture_placement]

        return (self.model_ele_list, [])