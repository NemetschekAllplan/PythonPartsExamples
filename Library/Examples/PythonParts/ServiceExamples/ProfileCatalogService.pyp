<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ServiceExamples\ProfileCatalogService.py</Name>
    <Title>ProfileCatalogService</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>GET_PROFILE</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>GET_BOUNDARY_POLYLINE</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>GET_BOUNDARY_PATH</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>Page1</Name>
    <Text>Page 1</Text>
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
        <Name>ProfileExp</Name>
        <Text>Profile</Text>
        <ValueType>Expander</ValueType>
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
        <Name>ProfileAccess</Name>
        <Text>Profile access</Text>
        <Value>GET_PROFILE</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>GetProfile</Name>
            <Text>Get profile</Text>
            <Value>GET_PROFILE</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>GetBoundaryPolyline</Name>
            <Text>Get boundary polyline</Text>
            <Value>GET_BOUNDARY_POLYLINE</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>GetBoundaryPath</Name>
            <Text>Get boundary path</Text>
            <Value>GET_BOUNDARY_PATH</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DoubleProfileExp</Name>
        <Text>Double profile</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>OverrideDefaultGap</Name>
            <Text>Override default gap</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>OverrideGap</Name>
            <Text>Override gap</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
            <MinValue>0</MinValue>
            <Enable>OverrideDefaultGap</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
