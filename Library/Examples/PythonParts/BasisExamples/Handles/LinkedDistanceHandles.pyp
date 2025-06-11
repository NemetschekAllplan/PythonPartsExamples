<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>BasisExamples\Handles\LinkedDistanceHandles.py</Name>
        <Title>LinkedDistanceHandles</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>
        <Parameters>
            <Parameter>
                <Name>RoundedRectExp</Name>
                <Text>Rounded rectangle</Text>
                <ValueType>Expander</ValueType>

                <Parameters>
                    <Parameter>
                        <Name>RectLength</Name>
                        <Text>Rect length</Text>
                        <Value>1000</Value>
                        <ValueType>Length</ValueType>
                        <MinValue>RectThickness / 2</MinValue>
                    </Parameter>
                    <Parameter>
                        <Name>RectThickness</Name>
                        <Text>Rect thickness</Text>
                        <Value>1000</Value>
                        <ValueType>Length</ValueType>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>
