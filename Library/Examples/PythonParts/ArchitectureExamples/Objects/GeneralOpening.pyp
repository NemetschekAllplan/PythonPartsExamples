<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\Objects\GeneralOpening.py</Name>
    <Title>General opening</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ELEMENT_SELECT</Name>
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
      <Parameter>
        <Name>GeometryExp</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Text>Shape</Text>
            <Name>Shape</Name>
            <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
            <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eSemiCircle|
                          AllplanArchEle.VerticalOpeningShapeType.eArbitrary</EnumList>
            <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eCircle|
                                 AllplanSettings.TextResShapeType.eSemiCircle|
                                 AllplanSettings.TextResShapeType.eArbitrary</ValueTextIdList>
            <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eSemiCircle|
                           AllplanSettings.PictResShapeType.eArbitrary</EnumList2>
            <ValueType>PictureResourceButtonList</ValueType>
          </Parameter>
          <Parameter>
            <Name>ProfileRow</Name>
            <Text>Select geometry</Text>
            <ValueType>Row</ValueType>
            <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eArbitrary</Visible>
            <Parameters>
              <Parameter>
                <Name>Profile</Name>
                <Text>Selection</Text>
                <Value/>
                <ValueType>String</ValueType>
                <ValueDialog>SymbolDialog</ValueDialog>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Opening width</Text>
            <Value>1010</Value>
            <ValueType>Length</ValueType>
            <MinValue>10</MinValue>
            <Enable>Shape != AllplanArchEle.VerticalOpeningShapeType.eArbitrary</Enable>
          </Parameter>
          <Parameter>
            <Name>Depth</Name>
            <Text>Depth</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>ElementThickness</MaxValue>
          </Parameter>
          <Parameter>
            <Name>RiseAtTop</Name>
            <Text>Rise at top</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
            <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eSemiCircle</Visible>
            <MinValue>1</MinValue>
            <MaxValue>HeightSettings.Height</MaxValue>
          </Parameter>
          <Parameter>
            <Name>HeightToRise</Name>
            <Text>Height to rise</Text>
            <Value/>
            <ValueType>Length</ValueType>
            <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eSemiCircle</Visible>
            <MinValue>0</MinValue>
            <Constraint>HeightSettings.Height - RiseAtTop</Constraint>
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
            <Constraint>BottomElevation=SillHeight;Height=(RiseAtTop + HeightToRise) if Shape == AllplanArchEle.VerticalOpeningShapeType.eSemiCircle else HeightSettings.Height</Constraint>
            <Enable>|HeightSettings.Height:Shape != AllplanArchEle.VerticalOpeningShapeType.eArbitrary</Enable>
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
        <Name/>
        <Text/>
        <Value>etc\PythonPartsFramework\ParameterIncludes\GeneralOpeningSymbolsProperties.incl</Value>
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
      <Parameter>
        <Name>ElementTierCount</Name>
        <Text>Element tier count</Text>
        <Value>1</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
