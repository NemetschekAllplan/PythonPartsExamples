<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\CheckBox.py</Name>
        <Title>CheckBox</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Single controls</Text>

        <Parameter>
            <Name>Format</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>DrawCubeExp</Name>
            <Text>Check box</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DrawCube</Name>
                <Text>Draw cube</Text>
                <Value>1</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>OneDimList</Name>
            <Text>One dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DrawCubeCount</Name>
                <Text>DrawCube count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>DrawCubeSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>DrawCubeList</Name>
                <Text></Text>
                <TextDyn>"Draw cube " + str($list_row + 1)</TextDyn>
                <Value>[1,0,1]</Value>
                <ValueType>CheckBox</ValueType>
                <Dimensions>DrawCubeCount</Dimensions>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TwoDimListExp</Name>
            <Text>Two dimensional list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DrawCubeList2Dim</Name>
                <Text></Text>
                <TextDyn>"Draw cube " + str($list_row + 1)</TextDyn>
                <Value>[[1,0],[0,1],[1,1]]</Value>
                <ValueType>CheckBox</ValueType>
                <Dimensions>DrawCubeCount,2</Dimensions>
            </Parameter>
        </Parameter>
    </Page>
</Element>
