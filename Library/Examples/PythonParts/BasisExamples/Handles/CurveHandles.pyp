<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
    <Script>
        <Name>BasisExamples\Handles\CurveHandles.py</Name>
        <Title>CurveHandles</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>
        <Parameters>
            <Parameter>
                <Name>Polygon3DExp</Name>
                <Text>Polygon</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                  <Parameter>
                    <Name>Polygon</Name>
                    <Text>Point</Text>
                    <Value>Polygon3D(Points((0,0,0)(5000,-1000,2000)(5000,5000,2000)(0,3000,0)(0,0,0)))</Value>
                    <ValueType>Polygon3D</ValueType>
                    <XYZinRow>True</XYZinRow>
                  </Parameter>
                </Parameters>
            </Parameter>
            <Parameter>
                <Name>LineExp</Name>
                <Text>Line</Text>
                <ValueType>Expander</ValueType>
                <Parameters>
                    <Parameter>
                        <Name>Line</Name>
                        <Text></Text>
                        <Value>Line2D(0,7000,5000, 9000)</Value>
                        <ValueType>Line2D</ValueType>
                        <XYZinRow>True</XYZinRow>
                    </Parameter>
                </Parameters>
            </Parameter>
        </Parameters>
    </Page>
</Element>
