<?xml version="1.0" encoding="utf-8"?>
<Element>
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

        <Parameter>
            <Name>Expander</Name>
            <Text>File selection</Text>
            <ValueType>Expander</ValueType>

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
                <Value></Value>
                <ValueType>String</ValueType>
                <ValueDialog>OpenFileDialog</ValueDialog>
                <FileFilter>SKP-files(*.SKP)|*.SKP|</FileFilter>
                <FileExtension>SKP</FileExtension>
            </Parameter>

            <Parameter>
                <Name>IfcFile</Name>
                <Text>Open IFC file</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <ValueDialog>OpenFileDialog</ValueDialog>
                <FileFilter>OBJ-files(*.IFC)|*.IFC|</FileFilter>
                <FileExtension>IFC</FileExtension>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>Expander</Name>
            <Text>Rotation</Text>
            <ValueType>Expander</ValueType>

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
        </Parameter>
        <Parameter>
            <Name>CreateButtonRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameter>
                <Name>CreateButtonRow</Name>
                <Text>Create</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
                <Visible>__is_input_mode()</Visible>
            </Parameter>
        </Parameter>
    </Page>
</Element>
