<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ArchitectureExamples\Objects\SlopedGeneralOpening.py</Name>
    <Title>General opening</Title>
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
        <Name>GeneralSlopedOpening</Name>
        <Text>Geometry</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Text>Shape</Text>
            <Name>Shape</Name>
            <Value>AllplanArchEle.VerticalOpeningShapeType.eRectangle</Value>
            <EnumList>AllplanArchEle.VerticalOpeningShapeType.eRectangle|
                          AllplanArchEle.VerticalOpeningShapeType.eCircle</EnumList>
            <ValueTextIdList>AllplanSettings.TextResShapeType.eRectangle|
                                 AllplanSettings.TextResShapeType.eCircle</ValueTextIdList>
            <EnumList2>AllplanSettings.PictResShapeType.eRectangle|
                           AllplanSettings.PictResShapeType.eCircle</EnumList2>
            <ValueType>PictureResourceButtonList</ValueType>
          </Parameter>
          <Parameter>
            <Name/>
            <ValueType>ConditionGroup</ValueType>
            <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eRectangle</Visible>
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
            <Visible>Shape == AllplanArchEle.VerticalOpeningShapeType.eCircle</Visible>
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
            <Name>HasIndependent2DInteraction</Name>
            <Text>Above/below section plane</Text>
            <Value/>
            <ValueType>CheckBox</ValueType>
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
