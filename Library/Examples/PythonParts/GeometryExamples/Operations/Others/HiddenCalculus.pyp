<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Others\HiddenCalculus.py</Name>
        <Title>Hidden calculation</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Hidden calculation</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>3D objects</Value>
            <ValueType>Text</ValueType>
        </Parameter>
        <Parameter>
            <Name>HiddenCalculusOptionsExapander</Name>
            <Text>Options of HiddenCalculus</Text>
            <ValueType>Expander</ValueType>
            <Visible>True</Visible>

            <Parameter>
                <Name>GetObserverMatrixFrom</Name>
                <Text>Observer matrix</Text>
                <Value>CurrentView</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>GetObserverMatrixFromCurrentView</Name>
                    <Text>get from current view</Text>
                    <Value>CurrentView</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>GetObserverMatrixFromManualInput</Name>
                    <Text>by eye and view points</Text>
                    <Value>ManualInput</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>EyePoint</Name>
                <Text>Eye point</Text>
                <Value>Point3D(0,0,0)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Visible>GetObserverMatrixFrom == "ManualInput"</Visible>
            </Parameter>

            <Parameter>
                <Name>ViewPoint</Name>
                <Text>View point</Text>
                <Value>Point3D(0,0,-1000)</Value>
                <ValueType>Point3D</ValueType>
                <XYZinRow>True</XYZinRow>
                <Visible>GetObserverMatrixFrom == "ManualInput"</Visible>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>AdjacentEdgesAngle</Name>
                <Text>Adjacent edges angle</Text>
                <Value>10</Value>
                <ValueType>Angle</ValueType>
                <MinValue>0</MinValue>
                <MaxValue>90</MaxValue>
            </Parameter>

            <Parameter>
                <Name>ExtraSmooth</Name>
                <Text>Extra smooth calculation</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>CreateObjectsExpander</Name>
            <Text>Objects to create</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CreateVisibleLines</Name>
                <Text>Visible lines</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateHiddenLines</Name>
                <Text>Hidden lines</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <Text></Text>
                <ValueType>Separator</ValueType>
                <Visible>CreateVisibleLines or CreateHiddenLines</Visible>
            </Parameter>

            <Parameter>
                <Name>DeleteOriginalObjects</Name>
                <Text>Delete source solids</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>CreateVisibleLines or CreateHiddenLines</Visible>
            </Parameter>
        </Parameter>

    </Page>
</Element>
