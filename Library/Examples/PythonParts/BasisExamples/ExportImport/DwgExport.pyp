<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\ExportImport\DwgExport.py</Name>
        <Title>DWGExport</Title>
    </Script>
    <Constants>
        <Constant>
            <Name>EXPORT_DWG</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>IMPORT_DWG</Name>
            <Value>1002</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Example</Text>

        <Parameter>
            <Name>DwgExportConfigFileName</Name>
            <Text>DWG export configuration file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>DwgImportConfigFileName</Name>
            <Text>DWG import configuration file</Text>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>Expander1</Name>
            <Text>Drawing file</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>DwgDrawingFileName</Name>
                <Text>DWG export file</Text>
                <Value>C:\abc\abc.dwg</Value>
                <ValueType>String</ValueType>
            </Parameter>

            <Parameter>
                <Name>DrawingFileButton1</Name>
                <Text>Export DWG</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>DrawingButton1</Name>
                    <Text>Execute</Text>
                    <EventId>EXPORT_DWG</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>DrawingXOffset</Name>
                <Text>X offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingYOffset</Name>
                <Text>Y offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingZOffset</Name>
                <Text>Z offset</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingZAngle</Name>
                <Text>Rotation around the Z-axis</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingXRotation</Name>
                <Text>X rotation (mm)</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingYRotation</Name>
                <Text>Y rotation (mm)</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DrawingFileButton2</Name>
                <Text>Import DWG</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>DrawingButton2</Name>
                    <Text>Execute</Text>
                    <EventId>IMPORT_DWG</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
</Element>
