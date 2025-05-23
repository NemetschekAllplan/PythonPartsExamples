<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\MacroWithElementGroup.py</Name>
    <Title>Window with elementgroups</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Page1</Text>
    <!-- Dimensions for the window  -->
    <!-- Create PP or elementgroups  -->
    <Parameters>
      <Parameter>
        <Name>Lenght</Name>
        <Text>Lenght</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
        <MinValue>10</MinValue>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <Text>Height</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
        <MinValue>10</MinValue>
      </Parameter>
      <Parameter>
        <Name>Depth</Name>
        <Text>depth</Text>
        <Value>70.</Value>
        <ValueType>Length</ValueType>
        <MinValue>10</MinValue>
      </Parameter>
      <Parameter>
        <Name>Casement_count</Name>
        <Text>Casement count</Text>
        <Value>2</Value>
        <ValueType>Integer</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>2</MaxValue>
      </Parameter>
      <Parameter>
        <Name>Surface_glas</Name>
        <Text>Surface glas</Text>
        <TextId>e_SURFACE</TextId>
        <Value>Glas</Value>
        <DisableButtonIsShown>False</DisableButtonIsShown>
        <ValueType>MaterialButton</ValueType>
      </Parameter>
      <Parameter>
        <Name>Add_attr_price</Name>
        <Text>Add attribute price</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>Guid_first_elementgroup</Name>
        <Text>Guid for first Elementgroup</Text>
        <Value>3e2829d0-ab01-4347-999d-292aabe1b262</Value>
        <ValueType>String</ValueType>
      </Parameter>
      <Parameter>
        <Name>Create_macro</Name>
        <Text>Create Pythonpart</Text>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
