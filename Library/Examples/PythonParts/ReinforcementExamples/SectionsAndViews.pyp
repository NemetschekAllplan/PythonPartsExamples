<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ReinforcementExamples\SectionsAndViews.py</Name>
        <Title>SectionsAndViews</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Reinforcement</Text>

        <Parameter>
            <Name>IsPythonPart</Name>
            <Text>Create PythonPart</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Geometry</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>2000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>3000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>1000</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>Reinforcement</Name>
            <Text>Reinforcement</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter stirrup</Text>
                <Value>10</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>DiameterLongitudinal</Name>
                <Text>Bar diameter Longitudinal</Text>
                <Value>20</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>Distance</Name>
                <Text>Bar spacing</Text>
                <Value>200</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>BendingRoller</Name>
                <Text>Bending roller</Text>
                <Value>4</Value>
                <ValueType>ReinfBendingRoller</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>UVS</Name>
            <Text>Views and sections</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ShowSectionBody</Name>
                <Text>Show section body in section</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ShowSectionBodyInModel</Name>
                <Text>Show section body in model</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>SectionHeightFromElement</Name>
                <Text>Section height from element</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>SectionBottomLevel</Name>
                <Text>Section bottom level</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Enable>SectionHeightFromElement == False</Enable>
            </Parameter>
            <Parameter>
                <Name>SectionTopLevel</Name>
                <Text>Section top level</Text>
                <Value>500</Value>
                <ValueType>Length</ValueType>
                <Enable>SectionHeightFromElement == False</Enable>
            </Parameter>
            <Parameter>
                <Name>AutoUpdate</Name>
                <Text>Automatic update</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
