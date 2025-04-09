<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Title>CadDataFileReader</Title>
    <Name>BasisExamples\ExportImport\CadDataFileReader.py</Name>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>CadDataFileReader</Name>
    <Text>Properties</Text>
    <Parameters>
      <Parameter>
        <Name>Expander</Name>
        <Text>File selection</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ObjFile</Name>
            <Text>Open OBJ file</Text>
            <Value>etc\PythonPartsExampleScripts\BasisExamples\ExportImport\data\earth.obj</Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>OBJ-files(*.OBJ)|*.OBJ|</FileFilter>
            <FileExtension>OBJ</FileExtension>
          </Parameter>
          <Parameter>
            <Name>SkpFile</Name>
            <Text>Open SKP file</Text>
            <Value/>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>SKP-files(*.SKP)|*.SKP|</FileFilter>
            <FileExtension>SKP</FileExtension>
          </Parameter>
          <Parameter>
            <Name>IfcFile</Name>
            <Text>Open IFC file</Text>
            <Value/>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>OBJ-files(*.IFC)|*.IFC|</FileFilter>
            <FileExtension>IFC</FileExtension>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander</Name>
        <Text>Rotation</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RotationAngleX</Name>
            <Text>Rotation x-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
          <Parameter>
            <Name>RotationAngleY</Name>
            <Text>Rotation y-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
          <Parameter>
            <Name>RotationAngleZ</Name>
            <Text>Rotation z-axis</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
            <ExcludeIdentical>True</ExcludeIdentical>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CreateButtonRow</Name>
        <Text> </Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>CreateButtonRow</Name>
            <Text>Create</Text>
            <EventId>1000</EventId>
            <ValueType>Button</ValueType>
            <Visible>__is_input_mode()</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
