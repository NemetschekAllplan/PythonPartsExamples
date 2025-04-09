<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Dialogs\PlaneReferencesControls.py</Name>
    <Title>PlaneControls</Title>
    <Version>1.0</Version>
    <DataColumnWidth>150</DataColumnWidth>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>PlaneDialogs</Name>
    <Text>Dialogs</Text>
    <Parameters>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PlanesExp</Name>
        <Text>Planes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlanRefPolyhed1</Name>
            <Text>Polyhedron height</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
            <Visible>|PlanRefPolyhed1.Height:False</Visible>
          </Parameter>
          <Parameter>
            <Name>PlanRefPolyhed2</Name>
            <Text>Polyhedron bottom</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>BottomPlaneReferences</ValueDialog>
            <Visible>|PlanRefPolyhed2.AbsBottomElevation:False</Visible>
          </Parameter>
          <Parameter>
            <Name>PlanRefPolyhed3</Name>
            <Text>Polyhedron top</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>TopPlaneReferences</ValueDialog>
            <Visible>|PlanRefPolyhed3.AbsTopElevation:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PlanesExp1</Name>
        <Text>Planes with input control</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlanRefCylinder1</Name>
            <Text>Cylinder height</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>PlanRefCylinder2</Name>
            <Text>Cylinder bottom</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>BottomPlaneReferences</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>PlanRefCylinder3</Name>
            <Text>Cylinder top</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>TopPlaneReferences</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Constraints</Name>
    <Text>Constraints</Text>
    <Parameters>
      <Parameter>
        <Name>ConstraintFormat</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ConstraintCommonProp</Name>
            <Text/>
            <Value>CommonProperties(Color(5))</Value>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PlanesExp</Name>
        <Text>Planes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>BoxBottomElevation</Name>
            <Text>Box bottom</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Constraint>PlaneRefBoxCylinder.BottomElevation</Constraint>
            <Persistent>FAVORITE</Persistent>
          </Parameter>
          <Parameter>
            <Name>AbsBoxBottomElevation</Name>
            <Text>Absolute Box bottom</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Constraint>PlaneRefBoxCylinder.AbsBottomElevation</Constraint>
            <Persistent>FAVORITE</Persistent>
          </Parameter>
          <Parameter>
            <Name>CylinderHeight</Name>
            <Text>Cylinder height</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
            <MinValue>1</MinValue>
            <MaxValue>PlaneRefBoxCylinder.Height</MaxValue>
          </Parameter>
          <Parameter>
            <Name>BoxHeight</Name>
            <Text>Box height</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Constraint>PlaneRefBoxCylinder.Height - CylinderHeight</Constraint>
            <MinValue>0</MinValue>
            <Persistent>FAVORITE</Persistent>
          </Parameter>
          <Parameter>
            <Name>CylinderTopElevation</Name>
            <Text>Cylinder top</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Constraint>PlaneRefBoxCylinder.TopElevation</Constraint>
            <Persistent>FAVORITE</Persistent>
          </Parameter>
          <Parameter>
            <Name>AbsCylinderTopElevation</Name>
            <Text>Absolute cylinder top</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Constraint>PlaneRefBoxCylinder.AbsTopElevation</Constraint>
            <Persistent>FAVORITE</Persistent>
          </Parameter>
          <Parameter>
            <Name>PlaneRefBoxCylinder</Name>
            <Text>Height</Text>
            <Value/>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
            <Constraint>BottomElevation=BoxBottomElevation;AbsBottomElevation=AbsBoxBottomElevation;Height=BoxHeight + CylinderHeight;TopElevation=CylinderTopElevation;AbsTopElevation=AbsCylinderTopElevation</Constraint>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>List</Name>
    <Text>List</Text>
    <Parameters>
      <Parameter>
        <Name>PlaneRefCount</Name>
        <Text>Plane count</Text>
        <Value>3</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>PlaneRefSep</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>PlaneReferencesCone</Name>
        <Text/>
        <TextDyn>"Plane " + str($list_row + 1)</TextDyn>
        <Value>[PlaneReferences();PlaneReferences();PlaneReferences()]</Value>
        <ValueType>PlaneReferences</ValueType>
        <ValueDialog>PlaneReferences</ValueDialog>
        <Dimensions>PlaneRefCount</Dimensions>
      </Parameter>
    </Parameters>
  </Page>
</Element>
