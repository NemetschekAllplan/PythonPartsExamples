<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\Intersection\CutSolidWithPlane.py</Name>
    <Title>Cut solid</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>SelectGeometry</Name>
    <Text>Cut solid with plane</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>volumetric 3D objects</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>CreateObjectsExpander</Name>
        <Text>Objects to create</Text>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>CreateSolidAbove</Name>
            <Text>Create solid above</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateSolidBelow</Name>
            <Text>Create solid below</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <Text/>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>DeleteOriginalObjects</Name>
            <Text>Delete original objects</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <Text/>
        <ValueType>Separator</ValueType>
        <Visible>CreateSolidAbove == True or CreateSolidBelow == True</Visible>
      </Parameter>
      <Parameter>
        <Name>CommonProperties</Name>
        <Text/>
        <Value/>
        <ValueType>CommonProperties</ValueType>
        <Visible>CreateSolidAbove == True or CreateSolidBelow == True</Visible>
      </Parameter>
    </Parameters>
  </Page>
</Element>
