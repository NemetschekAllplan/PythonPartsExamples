<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\ModifyObjects\ModifyPolygonalGeneralOpening.py</Name>
        <Title>General opening</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Constants>
        <Constant>
            <Name>ELEMENT_SELECT</Name>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>OPENING_INPUT</Name>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>

        <Parameter>
            <Name>GeometryExp</Name>s
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SillHeight</Name>
                <Text>Height to BL</Text>
                <Value></Value>
                <ValueType>Length</ValueType>
                <Constraint>HeightSettings.BottomElevation</Constraint>
                <Persistent>NO</Persistent>
            </Parameter>

            <Parameter>
                <Name>HeightSettings</Name>
                <Text>Opening height</Text>
                <Value>PlaneReferences(BottomElevation(1000)Height(1010))</Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
                <Constraint>BottomElevation=SillHeight;Height=RiseAtTop + HeightToRise</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name></Name>
            <Text></Text>
            <Value>etc\PythonPartsFramework\ParameterIncludes\OpeningSillProperties.incl</Value>
            <ValueType>Include</ValueType>
        </Parameter>

        <Parameter>
            <Name>AttributesExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>NicheType</Name>
                <Text>Type</Text>
                <Value>Niche</Value>
                <ValueList>Niche|Recess, opening</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>HasIndependent2DInteraction</Name>
                <Text>Above/below section plane</Text>
                <Value></Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>IsVisibleInViewSection3D</Name>
                <Text>Visible in view/section/3D model</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
                <Visible>NicheType != "Niche"</Visible>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>__HiddenPage__</Name>
        <Text></Text>
        <Parameter>
            <Name>InputMode</Name>
            <Text>Input mode</Text>
            <Value></Value>
            <ValueType>Integer</ValueType>
        </Parameter>

        <Parameter>
            <Name>ElementThickness</Name>
            <Text>Element thickness</Text>
            <Value>1000</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>
</Element>
