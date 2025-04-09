<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\Objects\SlopedSlabOpening.py</Name>
    <Title>Sloped slab opening</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>START_AXIS_INPUT</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>END_AXIS_INPUT</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>OPENING_INPUT</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Test</Text>
    <Parameters>
      <Parameter>
        <Name>SlopedSlabOpening</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Text>Shape</Text>
            <Name>Shape</Name>
            <Value>AllplanArchEle.ShapeType.eRectangular</Value>
            <EnumList>AllplanArchEle.ShapeType.eRectangular|
                          AllplanArchEle.ShapeType.eCircular,
                          AllplanArchEle.ShapeType.eRegularPolygonCircumscribed|</EnumList>
            <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eCircle|
                                 AllplanSettings.TextResShapeType.eRegularPolygonCircumscribed</ValueTextIdList>
            <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle|
                           AllplanSettings.PictResShapeType.eRegularPolygonCircumscribed</EnumList2>
            <ValueType>PictureResourceButtonList</ValueType>
          </Parameter>
          <Parameter>
            <Name/>
            <ValueType>ConditionGroup</ValueType>
            <Visible>Shape == AllplanArchEle.ShapeType.eRectangular</Visible>
            <Parameters>
              <Parameter>
                <Name>CuboidWidth</Name>
                <Text>Cuboid width</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
              </Parameter>
              <Parameter>
                <Name>CuboidHeight</Name>
                <Text>Cuboid height</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>PipeRadius</Name>
            <Text>Pipe radius</Text>
            <Value>250</Value>
            <ValueType>Length</ValueType>
            <Visible>Shape in (AllplanArchEle.ShapeType.eCircular, AllplanArchEle.ShapeType.eRegularPolygonCircumscribed)</Visible>
          </Parameter>
          <Parameter>
            <Name>NumberOfCorners</Name>
            <Text>Number of corners (3-19)</Text>
            <Value>6</Value>
            <ValueType>Integer</ValueType>
            <MinValue>3</MinValue>
            <MaxValue>19</MaxValue>
            <Visible>Shape == AllplanArchEle.ShapeType.eRegularPolygonCircumscribed</Visible>
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
    </Parameters>
  </Page>
</Element>
