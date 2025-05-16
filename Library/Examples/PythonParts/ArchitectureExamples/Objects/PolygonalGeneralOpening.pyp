<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\Objects\PolygonalGeneralOpening.py</Name>
    <Title>General opening</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>POLYGON_INPUT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>OPENING_INPUT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter><Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameters>
              <Parameter><Text>Shape</Text>
                <Name>Shape</Name>
                <Value>AllplanArchEle.ShapeType.ePolygonal</Value>
                <EnumList>AllplanArchEle.ShapeType.ePolygonal|
                          AllplanArchEle.ShapeType.eProfile</EnumList>
                <ValueTextIdList>AllplanSettings.TextResShapeType.ePolygon|
                                AllplanSettings.TextResShapeType.eArbitrary</ValueTextIdList>
                <EnumList2>AllplanSettings.PictResShapeType.ePolygon|
                          AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
                <ValueType>PictureResourceButtonList</ValueType>
              </Parameter>

            <Parameter>
              <Name>ProfileRow</Name>
              <Text>Select geometry</Text>
              <ValueType>Row</ValueType>
              <Visible>Shape == AllplanArchEle.ShapeType.eProfile</Visible>

              <Parameters>
                <Parameter>
                  <Name>Profile</Name>
                  <Text>Selection</Text><Value/>
                  <ValueType>String</ValueType>
                  <ValueDialog>SymbolDialog</ValueDialog>
                </Parameter>
              </Parameters>
            </Parameter>

            <Parameter>
              <Name>SillHeight</Name>
              <Text>Height to BL</Text>
              <Value/>
              <ValueType>Length</ValueType>
              <Constraint>HeightSettings.BottomElevation</Constraint>
              <Persistent>NO</Persistent>
            </Parameter>

            <Parameter>
              <Name>HeightSettings</Name>
              <Text>Opening height</Text>
              <Value>PlaneReferences(BottomElevation(1000)Height(1010))</Value>
              <ValueType>PlaneReferences</ValueType>
              <ValueDialog>PlaneReferences</ValueDialog>
              <Constraint>BottomElevation=SillHeight;Height=RiseAtTop + HeightToRise</Constraint>
            </Parameter>
          </Parameters>
      </Parameter>
      <Parameter>
        <Name/>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSillProperties.incl</Value>
        <ValueType>Include</ValueType>
      </Parameter>
      <Parameter>
        <Name>AttributesExp</Name>
        <Text>Attributes</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>NicheType</Name>
            <Text>Type</Text>
            <Value>Niche</Value>
            <ValueList>Niche|Recess, opening</ValueList>
            <ValueType>StringComboBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>HasIndependent2DInteraction</Name>
            <Text>Above/below section plane</Text>
            <Value/>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>IsVisibleInViewSection3D</Name>
            <Text>Visible in view/section/3D model</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Visible>NicheType != "Niche"</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value/>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>ElementThickness</Name>
        <Text>Element thickness</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
