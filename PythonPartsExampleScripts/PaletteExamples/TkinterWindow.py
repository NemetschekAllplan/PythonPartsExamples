"""
Example Script for TkinterWindow
"""

import tkinter as tk
from tkinter import Frame, Button, N, S, E, W, Label, Text, Radiobutton, messagebox

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from BuildingElement import BuildingElement
from HandleProperties import HandleProperties
from PythonPart import View2D3D, PythonPart

print('Load TkinterWindow.py')


class TkApplication(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("Set Box Dimentions")
        self.master.grab_set()
        self.master.minsize(300, 150)
        self.setRootGrid()
        self.dimensions = []
        self.createStringControlVariable()
        self.createWidgets()
        #self.master.protocol("WM_DELETE_WINDOW", lambda:self.saveAndQuit(tk.Event()))


    def setRootGrid(self):
        self.master.columnconfigure(0, weight = 1)
        self.master.rowconfigure(0, weight = 1)
        self.grid(sticky = N+S+E+W)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 2)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 1)


    def createStringControlVariable(self):
        self.lengthsv = tk.StringVar()
        self.widthsv = tk.StringVar()
        self.heightsv = tk.StringVar()
        self.unitsv = tk.StringVar()
        self.unitsv.set("[m]")


    def createWidgets(self):
        self.createLabel("length", 0, 0)
        self.createLabel("width", 0, 1)
        self.createLabel("height", 0, 2)

        self.unitLabel = Label(self, text = "unit")
        self.unitLabel.grid(column = 0, row = 3)

        self.bind_class("Text", "<Tab>", self.focus_next_widget)
        self.bind_class("Text", "<Return>", self.disable_return)
        self.createText("lengthText", 1, 0)
        self.createText("widthText", 1, 1)
        self.createText("heightText", 1, 2)

        self.createRadioButtonGroup()

        self.saveAndQuitButton = Button(self, text = "Save and quit", command = lambda: self.saveAndQuit(tk.Event()))
        self.saveAndQuitButton.bind("<Return>", self.saveAndQuit)
        self.saveAndQuitButton.grid(column = 0, columnspan = 2, row = 6)


    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")


    def disable_return(self, event):
        pass


    def createRadioButtonGroup(self):
        self.createRadioButton("unitRadiobutton1", "[m]", 1, 3)
        self.createRadioButton("unitRadiobutton2", "[cm]", 1, 4)
        self.createRadioButton("unitRadiobutton3", "[mm]", 1, 5)


    def createRadioButton(self, buttonname, value, col, row):
        self.__dict__[buttonname] = Radiobutton(self, value = value, text = value, variable = self.unitsv, command = self.radiobutton_changed_handler)
        self.__dict__[buttonname].grid(column = col, row = row, sticky = N+S+E+W)


    def radiobutton_changed_handler(self):
        val = self.unitsv.get()
        self.lengthsv.set("length " + val)
        self.widthsv.set("width " + val)
        self.heightsv.set("height " + val)


    def createLabel(self, name, col, row):
        self.__dict__[name + "sv"].set(name + self.unitsv.get())
        self.__dict__[name + "Label"] = Label(self, textvariable = self.__dict__[name + "sv"])
        self.__dict__[name + "Label"].grid(column = col, row = row)


    def createText(self, name, col, row):
        self.__dict__[name] = Text(self, width = 20, height = 1, wrap = "none")
        self.__dict__[name].grid(column = col, row = row)


    def saveAndQuit(self, event):
        val = self.unitsv.get()

        result1 = self.convertor(self.lengthText, val, "length")
        result2 = self.convertor(self.widthText, val, "width")
        result3 = self.convertor(self.heightText, val, "height")

        if result1 != "ok" and result2 != "ok" and result3 != "ok":
            self.dimensions.append(result1)
            self.dimensions.append(result2)
            self.dimensions.append(result3)
            self.quit()


    def getText(self, text):
        return text.get("0.0", index2 = "end-1c")


    def convertor(self, text, unit, info):
        try:
            val = self.getText(text)
            res = val.replace(",", ".")
            d = float(res)
            if unit == "[m]":
                return d*1000
            if unit == "[cm]":
                return d*10
            if unit == "[mm]":
                return d
        except:
            return messagebox.showwarning("Warning", "Wrong input %s!"%(info))



def check_allplan_version(build_ele: BuildingElement,
                          version:   float):
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


def create_element(build_ele: BuildingElement,
                   doc: AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """
    element = TkinterWindow(doc)

    return element.create(build_ele)


def move_handle(build_ele:
                BuildingElement,
                handle_prop: HandleProperties,
                input_pnt: AllplanGeo.Point3D,
                doc: AllplanElementAdapter.DocumentAdapter):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    element = TkinterWindow(doc)

    return element.create(build_ele)


def on_control_event(build_ele: BuildingElement,
                     event_id: int):
    """
    On control event

    Args:
        build_ele:  the building element.
        event_id:   event id of control.

    Returns:
        True/False if palette refresh is necessary
    """
    print ("TkinterWindow.py (on_control_event called, eventId: ", event_id, ")")

    if event_id == 1000:
        root = tk.Tk()
        app = None

        try:
            root.focus_force()
            app = TkApplication(master = root)
            root.mainloop()
        except:
            pass
        finally:
            try:
               root.destroy()
            except:
                pass

        if app and len(app.dimensions) == 3:
            build_ele.Length.value = app.dimensions[0]
            build_ele.Width.value = app.dimensions[1]
            build_ele.Height.value = app.dimensions[2]
            return True

    return False


class TkinterWindow():
    """
    Definition of class TkinterWindow
    """

    def __init__(self,
                 doc: AllplanElementAdapter.DocumentAdapter):
        """
        Initialization of class TkinterWindow

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.handle_list = None
        self.document = doc


    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.create_geometry(build_ele)
        return (self.model_ele_list, self.handle_list)


    def create_geometry(self,
                        build_ele: BuildingElement):
        """
        Create the element geometries

        Args:
            build_ele:  the building element.
        """

        #----------------- Extract palette parameter values
        length = build_ele.Length.value
        width = build_ele.Width.value
        height = build_ele.Height.value

        #------------------ Define the cube polyhedron
        polyhed = AllplanGeo.Polyhedron3D.CreateCuboid(length, width, height)

        #------------------ Define common properties, take global Allplan settings

        com_prop = AllplanSettings.AllplanGlobalSettings.GetCurrentCommonProperties()

        #------------------ Append cubes as new Allplan elements

        views = [View2D3D ([AllplanBasisElements.ModelElement3D(com_prop, polyhed)])]
        pythonpart = PythonPart ("Tkinter window",
                                 build_ele.get_params_list(),
                                 build_ele.get_hash(),
                                 build_ele.pyp_file_name,
                                 views)
        self.model_ele_list = pythonpart.create()

        #------------------ No handles

        self.handle_list = []

