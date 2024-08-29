"""
Script for GetBarShapeCode
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Reinforcement as AllplanReinf

print('Load GetBarShapeCode.py')


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
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = GetBarShapeCode(doc)

    return [], []


class GetBarShapeCode():
    """
    Definition of class GetBarShapeCode
    """

    def __init__(self, doc):
        """
        Initialization of class GetBarShapeCode
        """

        placement_uuids = [AllplanElementAdapter.BarsLinearPlacement_TypeUUID,
                           AllplanElementAdapter.BarsLinearMultiPlacement_TypeUUID,
                           AllplanElementAdapter.BarsAreaPlacement_TypeUUID,
                           AllplanElementAdapter.BarsSpiralPlacement_TypeUUID,
                           AllplanElementAdapter.BarsCircularPlacement_TypeUUID,
                           AllplanElementAdapter.BarsRotationalSolidPlacement_TypeUUID,
                           AllplanElementAdapter.BarsRotationalPlacement_TypeUUID,
                           AllplanElementAdapter.BarsTangentionalPlacement_TypeUUID,
                           AllplanElementAdapter.BarsEndBendingPlacement_TypeUUID]

        for element in AllplanBaseElements.ElementsSelectService.SelectAllElements(doc):
            if element == AllplanElementAdapter.BarsDefinition_TypeUUID:
                print("----------------------------------------------------------------------")
                print(element, "Pos.-Nr.=",AllplanElementAdapter.ReinforcementPropertiesReader.GetPositionNumber(element))

                code_count, bar_shape_codes, lengths = AllplanReinf.ReinforcementService.GetBarShapeCode(element, AllplanReinf.ReinforcementService.BarShapeCodeStandard.eIso4066)

                print("Iso4066: ", code_count, bar_shape_codes, lengths)

                code_count, bar_shape_codes, lengths = AllplanReinf.ReinforcementService.GetBarShapeCode(element, AllplanReinf.ReinforcementService.BarShapeCodeStandard.eIso3766)

                print("Iso3766: ", code_count, bar_shape_codes, lengths)

                code_count, bar_shape_codes, lengths = AllplanReinf.ReinforcementService.GetBarShapeCode(element, AllplanReinf.ReinforcementService.BarShapeCodeStandard.eBS)

                print("BS:      ", code_count, bar_shape_codes, lengths)

                code_count, bar_shape_codes, lengths = AllplanReinf.ReinforcementService.GetBarShapeCode(element, AllplanReinf.ReinforcementService.BarShapeCodeStandard.eSANS)

                print("SANS:    ", code_count, bar_shape_codes, lengths)

                code_count, bar_shape_codes, lengths = AllplanReinf.ReinforcementService.GetBarShapeCode(element, AllplanReinf.ReinforcementService.BarShapeCodeStandard.eACI)

                print("ACI:     ", code_count, bar_shape_codes, lengths)
                print("ACI rebar mark ",  AllplanReinf.ReinforcementService.GetACIBarMark(element, True))

                bar_pos_data = AllplanReinf.BarPositionData(element)

                print(bar_pos_data)
                print(AllplanReinf.ReinforcementSettings.GetBarWeight(bar_pos_data.SteelGrade, bar_pos_data.Diameter))

            elif element.GetElementAdapterType().GetGuid() in placement_uuids:
                def_element = AllplanElementAdapter.BaseElementAdapterParentElementService.GetParentElement(element)

                print("----------------------------------------------------------------------")
                print(element, "Pos.-Nr.=",AllplanElementAdapter.ReinforcementPropertiesReader.GetPositionNumber(def_element))

                print("ACI placement rebar mark ",  AllplanReinf.ReinforcementService.GetACIPlacementBarMark(element, True))

                placement_ele_vec = AllplanElementAdapter.BaseElementAdapterList()

                placement_ele_vec.append(element)

                if (bar_pos_data := AllplanReinf.ReinforcementService.GetBarPositionData(placement_ele_vec)):
                    print(bar_pos_data)
                    print(AllplanReinf.ReinforcementSettings.GetBarWeight(bar_pos_data[0].SteelGrade, bar_pos_data[0].Diameter))
