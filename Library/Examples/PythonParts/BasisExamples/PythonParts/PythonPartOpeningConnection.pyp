<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Title>PythonPartOpeningConnection.py</Title>
    <Name>BasisExamples\PythonParts\PythonPartOpeningConnection.py</Name>
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
      <Name>PARAMETER_MODIFICATION</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>FrameExp</Name>
        <Text>Frame</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FrameWidth</Name>
            <Text>Frame width</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>FrameThickness</Name>
            <Text>Frame thickness</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>FrameSurface</Name>
            <Text>Surface</Text>
            <Value>Materials\Plastic\Finishes\General_Plastic002</Value>
            <ValueType>MaterialButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PaneExp</Name>
        <Text>Pane</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PaneThickness</Name>
            <Text>Thickness</Text>
            <Value>20</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>PaneSurface</Name>
            <Text>Surface</Text>
            <Value>Materials\Glass\Transparent\Simple_Glass002</Value>
            <ValueType>MaterialButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text />
    <Parameters>
      <Parameter>
        <Name>PythonPartUUID</Name>
        <Value />
        <ValueType>String</ValueType>
      </Parameter>
      <Parameter>
        <Name>OpeningConnection</Name>
        <Value />
        <ValueType>ElementGeometryConnection</ValueType>
      </Parameter>
      <Parameter>
        <Name>InputMode</Name>
        <Text>Input mode</Text>
        <Value />
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>