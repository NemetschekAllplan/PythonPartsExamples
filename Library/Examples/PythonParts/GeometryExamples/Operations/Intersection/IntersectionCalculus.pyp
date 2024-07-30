<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>GeometryExamples\Operations\Intersection\IntersectionCalculus.py</Name>
        <Title>Intersection</Title>
        <Version>1.0</Version>
        <Interactor>True</Interactor>
    </Script>
    <Page>
        <Name>SelectGeometry</Name>
        <Text>Calculate intersection</Text>

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Selectable objects:</Text>
            <Value>General objects
(e.g. Line, Hatching, Area, 3D object)
            </Value>
            <ValueType>Text</ValueType>
        </Parameter>

        <Parameter>
            <Name>IntersectionCalculusOptions</Name>
            <Text>Options of IntersectionCalculus</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MaxSolutionNumber</Name>
                <Text>Maximum number of solutions</Text>
                <Value>10</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>Tolerance</Name>
                <Text>Tolerance</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
