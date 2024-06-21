<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\QuantityTakeOff\CalcMass.py</Name>
        <Title>Quantity take-off</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Quantity take-off from solids</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>Volumetric 3D objects</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>
        <Parameter>
            <Name>CreateCGPoint</Name>
            <Text>Create CG symbol</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>CGSymbolPropertiesExpander</Name>
            <Text>CG symbol properties</Text>
            <ValueType>Expander</ValueType>
            <Visible>CreateCGPoint</Visible>

            <Parameter>
                <Name>CGSymbolCommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>

            <Parameter>
                <Name>CGSymbolSize</Name>
                <Text>Symbol size</Text>
                <Value>100</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
