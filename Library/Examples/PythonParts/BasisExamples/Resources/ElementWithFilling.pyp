<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\Resources\ElementWithFilling.py</Name>
    <Title>Expander</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>Geometry</Text>
    <Parameters>
      <Parameter>
        <Name>Cube</Name>
        <Text>Cube</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Length</Name>
            <Text>Length</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>2000.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>5000.</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateAsPythonPart</Name>
            <Text>Create as PythonPart</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>SurfacePropertiesExpander</Name>
        <Text>Hatching/Pattern/Filling</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>InfoRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>InfoPicture</Name>
                <Text>To see the hatching/pattern/filling you have to create a section
that cuts right through the 3D object. Surface elements applied
on 3D objects are not visible directly in a plan or isometric view.</Text>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>SurfaceElementProperties</Name>
            <Text/>
            <Value/>
            <ValueType>SurfaceElementProperties</ValueType>
            <Visible>|SurfaceElementProperties.UseAreaInGroundplan:False</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
