<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>BasisExamples\ExportImport\IfcExportImport.py</Name>
    <Title>IfcExportImport</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Constants>
    <Constant>
      <Name>ACTIVE_FILE</Name>
      <Value>1</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>ALL_FILES</Name>
      <Value>2</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>SELECTED_FILES</Name>
      <Value>3</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>EXPORT_IFC</Name>
      <Value>1000</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>IMPORT_IFC</Name>
      <Value>2000</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>TemplatePage</Name>
    <Text>First Page</Text>
    <Parameters>
      <Parameter>
        <Name>ExportExpander</Name>
        <Text>Export</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IfcExportPath</Name>
            <Text>Export IFC file</Text>
            <Value/>
            <ValueType>String</ValueType>
            <ValueDialog>SaveFileDialog</ValueDialog>
            <FileFilter>IFC-files(*.ifc)|*.ifc|</FileFilter>
            <FileExtension>ifc</FileExtension>
            <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
          </Parameter>
          <Parameter>
            <Name>IfcExportTheme</Name>
            <Text>Export theme</Text>
            <Value>etc\Favoriten Standard\IFC\Ifc_4_standard_export_DEU.nth</Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>Theme-files(*.nth)|*.nth|</FileFilter>
            <FileExtension>nth</FileExtension>
            <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
          </Parameter>
          <Parameter>
            <Name>FilesToExport</Name>
            <Text>Files to export</Text>
            <Value>ACTIVE_FILE</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>FilesToExportActive</Name>
                <Text>Active file</Text>
                <Value>ACTIVE_FILE</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>FilesToExportAll</Name>
                <Text>All files</Text>
                <Value>ALL_FILES</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>FilesToExportSelect</Name>
                <Text>Select files</Text>
                <Value>SELECTED_FILES</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>FileList</Name>
            <Text>Files</Text>
            <Value>[_]</Value>
            <ValueType>namedtuple(Text,CheckBox)</ValueType>
            <NamedTuple>
              <TypeName>FileList</TypeName>
              <FieldNames>FileName,ExportState</FieldNames>
            </NamedTuple>
            <Visible>FilesToExport == 3,FilesToExport == 3</Visible>
            <ValueListStartRow>-1</ValueListStartRow>
          </Parameter>
          <Parameter>
            <Name>ExportButtonRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>ExportButton</Name>
                <Text>Export IFC</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
                <Enable>IfcExportPath</Enable>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ImportExpander</Name>
        <Text>Import</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>IfcImportPath</Name>
            <Text>Import IFC file</Text>
            <Value>etc\PythonPartsExampleScripts\BasisExamples\ExportImport\data\BoxCylinder.ifc</Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpenFileDialog</ValueDialog>
            <FileFilter>IFC-files(*.ifc)|*.ifc|</FileFilter>
            <FileExtension>ifc</FileExtension>
            <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
          </Parameter>
          <Parameter>
            <Name>ImportInto</Name>
            <Text> </Text>
            <Value>Import in drawing file</Value>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>ImportFileNumber</Name>
            <Text>Import file</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>ImportFileSelection</Name>
                <Text>Import</Text>
                <Value>[_]</Value>
                <ValueType>namedtuple(DisplayText,RadioButton)</ValueType>
                <NamedTuple>
                  <TypeName>ImportFileSelection</TypeName>
                  <FieldNames>RowText,FileSelection</FieldNames>
                </NamedTuple>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ImportButtonRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>ImportButton</Name>
                <Text>Import IFC</Text>
                <EventId>2000</EventId>
                <ValueType>Button</ValueType>
                <Enable>IfcImportPath</Enable>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
