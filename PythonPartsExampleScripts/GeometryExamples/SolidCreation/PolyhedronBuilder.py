"""Example script of using polyhedron builder to build a pyramid vertex-by-vertex,
edge-by-edge and face-by-face.
"""
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult
from PreviewSymbols import PreviewSymbols
from Utils import TextReferencePointPosition

from TypeCollections.ModelEleList import ModelEleList


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True

def create_element(build_ele: BuildingElement,
                   _doc     : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """Creation of a

    Args:
        build_ele: building element with the parameter properties
        _doc:      document of the Allplan drawing files

    Returns:
        created element result with cylinder brep if the creation was successful,
        or with just edge curves otherwise
    """

    # get common properties

    common_properties = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

    model_elements = ModelEleList(common_properties)
    preview_symbols = PreviewSymbols()


    # construct the polyhedron and the builder

    pyramid = AllplanGeo.Polyhedron3D()
    pyramid.SetType(AllplanGeo.PolyhedronType.names[build_ele.PolyhedronType.value])

    builder = AllplanGeo.Polyhedron3DBuilder(pyramid)


    # append vertices to the polyhedron
    # show the vertex number and a cross in the preview

    for i, vertex in enumerate(build_ele.PolyhedronVertices.value):
        builder.AppendVertex(vertex)

        preview_symbols.add_text(text=              str(i),
                                 reference_point=   vertex + AllplanGeo.Point3D(-40,0,0),
                                 ref_pnt_pos=       TextReferencePointPosition.CENTER_RIGHT,
                                 height=            25.0,
                                 color=             6,
                                 rotation_angle=    AllplanGeo.Angle())

        preview_symbols.add_cross(reference_point=  vertex,
                                  width=            25,
                                  color=            6)


    # append edges

    pyramid.AppendEdge(AllplanGeo.GeometryEdge(0,1))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(1,2))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(2,3))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(3,0))

    pyramid.AppendEdge(AllplanGeo.GeometryEdge(0,4))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(1,4))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(2,4))
    pyramid.AppendEdge(AllplanGeo.GeometryEdge(3,4))

    # append faces

    base = pyramid.CreateFace(4)
    base.AppendEdge(AllplanGeo.OrientedEdge(0, True))
    base.AppendEdge(AllplanGeo.OrientedEdge(1, True))
    base.AppendEdge(AllplanGeo.OrientedEdge(2, True))
    base.AppendEdge(AllplanGeo.OrientedEdge(3, True))

    face_1 = pyramid.CreateFace(3)
    face_1.AppendEdge(4, True)
    face_1.AppendEdge(5, False)
    face_1.AppendEdge(0, False)

    face_2 = pyramid.CreateFace(3)
    face_2.AppendEdge(5, True)
    face_2.AppendEdge(6, False)
    face_2.AppendEdge(1, False)

    face_3 = pyramid.CreateFace(3)
    face_3.AppendEdge(6, True)
    face_3.AppendEdge(7, False)
    face_3.AppendEdge(2, False)

    face_4 = pyramid.CreateFace(3)
    face_4.AppendEdge(7, True)
    face_4.AppendEdge(4, False)
    face_4.AppendEdge(3, False)


    # complete the polyhedron and check it for validity

    builder.Complete()

    if pyramid.IsValid():
        model_elements.append_geometry_3d(pyramid)

        return CreateElementResult(elements=        model_elements,
                                   preview_symbols= preview_symbols)

    print("Polyhedron is invalid")

    return CreateElementResult()
