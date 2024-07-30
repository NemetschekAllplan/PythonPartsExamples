"""
Example for MessageBox
"""

import NemAll_Python_Utility as AllplanUtil


print('Load MessageBox.py')


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

    Returns:
        Tuple with created elements, handles and (optional) reinforcement.
    """

    # Delete unused arguments
    del build_ele
    del doc

    return (list(), list())


def on_control_event(build_ele, event_id):
    """
    On control event

    Args:
        build_ele:  the building element.
        event_id:   event id of control.

    Returns:
        True/False if palette refresh is necessary
    """

    # Delete unused arguments
    del build_ele

    print ("MessageBox.py (on_control_event called, eventId: ", event_id, ")")

    if event_id == 1000:
        ret = AllplanUtil.ShowMessageBox("Message box with OK", AllplanUtil.MB_OK)

        print("Return value = " , ret)

        ret = AllplanUtil.ShowMessageBox("Message box with OK and Cancel", AllplanUtil.MB_OKCANCEL)

        print("Return value = " , ret)

        ret = AllplanUtil.ShowMessageBox("Message box with Yes and No", AllplanUtil.MB_YESNO)

        print("Return value = " , ret)

        ret = AllplanUtil.ShowMessageBox("Message box with Yes, No and Cancel", AllplanUtil.MB_YESNOCANCEL)

        print("Return value = " , ret)

        ret = AllplanUtil.ShowMessageBox("Message box with\n\nmultiple lines", AllplanUtil.MB_OK)

        print("Return value = " , ret)

        ret = AllplanUtil.ShowMessageBox("Message box with OK and DONOTASKAGAIN", AllplanUtil.MB_OK | AllplanUtil.MB_DONOTASKAGAIN)

        print("Return value = " , ret, " Don't ask again = ", ret & AllplanUtil.MB_DONOTASKAGAIN)


    else:
        print("unknown event id ", event_id)

    return False
