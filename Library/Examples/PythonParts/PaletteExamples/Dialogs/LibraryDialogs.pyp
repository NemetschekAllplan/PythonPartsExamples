<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\Dialogs\LibraryDialogs.py</Name>
    <Title>Library dialogs</Title>
    <Version>1.0</Version>
    <ReadLastInput>False</ReadLastInput>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Library dialogs</Text>
    <Parameters>
      <Parameter>
        <Name>LibraryDialogsExpander</Name>
        <Text>Library dialogs</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>LibraryElementType</Name>
            <Text>Type of library element</Text>
            <Value>Symbol</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>SymbolRadioButton</Name>
                <Text>Symbol</Text>
                <Value>Symbol</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>SmartSymbolRadioButton</Name>
                <Text>Smart symbol</Text>
                <Value>SmartSymbol</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>OpeningSymbolRadioButton</Name>
                <Text>Opening symbol</Text>
                <Value>OpeningSymbol</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>FixtureRadioButton</Name>
                <Text>Fixture</Text>
                <Value>Fixture</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>SymbolPath</Name>
            <Text>Select symbol</Text>
            <Value> </Value>
            <ValueType>String</ValueType>
            <ValueDialog>SymbolDialog</ValueDialog>
            <Visible>LibraryElementType == "Symbol"</Visible>
          </Parameter>
          <Parameter>
            <Name>SmartSymbolPath</Name>
            <Text>Select smart symbol</Text>
            <Value> </Value>
            <ValueType>String</ValueType>
            <ValueDialog>SmartSymbolDialog</ValueDialog>
            <Visible>LibraryElementType == "SmartSymbol"</Visible>
          </Parameter>
          <Parameter>
            <Name>OpeningSymbolPath</Name>
            <Text>Select opening symbol</Text>
            <Value> </Value>
            <ValueType>String</ValueType>
            <ValueDialog>OpeningSymbolDialog</ValueDialog>
            <Visible>LibraryElementType == "OpeningSymbol"</Visible>
          </Parameter>
          <Parameter>
            <Name>FixturePath</Name>
            <Text>Select fixture</Text>
            <Value/>
            <ValueType>String</ValueType>
            <ValueDialog>FixtureDialog</ValueDialog>
            <Visible>LibraryElementType == "Fixture"</Visible>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Format</Name>
        <Text>Format</Text>
        <ValueType>Expander</ValueType>
        <Value>True</Value>
        <Visible>False</Visible>
        <Parameters>
          <Parameter>
            <Name>CommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
