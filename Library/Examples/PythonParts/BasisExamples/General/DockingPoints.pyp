<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\General\DockingPoints.py</Name>
        <Title>Docking points</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>FixGeometry</Name>
            <Text>Fix geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>PolyhedronLength</Name>
                <Text>Polyhedron length</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PolyhedronWidth</Name>
                <Text>Polyhedron width</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>PolyhedronHeight</Name>
                <Text>Polyhedron height</Text>
                <Value>3000</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>CylinderRadius</Name>
                <Text>Cylinder radius</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>CylinderHeight</Name>
                <Text>Cylinder height</Text>
                <Value>2000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>MultiGeometry</Name>
            <Text>Multiple geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>MultiPolyhedronLength</Name>
                <Text>Length</Text>
                <Value>400</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>MultiPolyhedronWidth</Name>
                <Text>Width</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>MultiPolyhedronHeight</Name>
                <Text>Height</Text>
                <Value>3000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Count</Name>
                <Text>Count</Text>
                <Value>10</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>DynamicGeometry</Name>
            <Text>Dyamic geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DynamicLength</Name>
                <Text>Length</Text>
                <Value>5000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DynamicWidth</Name>
                <Text>Width</Text>
                <Value>300</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>DynamicHeight</Name>
                <Text>Height</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RecessLength</Name>
                <Text>Recess length</Text>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>RecessWidth</Name>
                <Text>Recess width</Text>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RecessLeft</Name>
            <Text>Recess left</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>RecessRight</Name>
            <Text>Recess right</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
    </Page>
</Element>
