<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\Symbol3D.py</Name>
        <Title>Symbol3D</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>SymbolId</Name>
            <Text>Symbol Id</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>Height</Name>
            <Text>Height</Text>
            <Value>10.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>10.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
       
        <Parameter>
            <Name>RotationAngle</Name>
            <Text>Rotation angle</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
        </Parameter>
       
        <Parameter>
            <Name>IsScaleDependent</Name>
            <Text>Scale dependent</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>PrimaryPointNumber</Name>
            <Text>Primary point number</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Parameter>        

        <Parameter>
            <Name>SecondaryPointNumber</Name>
            <Text>Secondary point number</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Parameter>        

        <Parameter>
            <Name>DescriptionText</Name>
            <Text>Description text</Text>
            <Value></Value>
            <ValueType>String</ValueType>
        </Parameter>

        <Parameter>
            <Name>IsStation</Name>
            <Text>Station</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>StationCode</Name>
            <Text>Station code</Text>
            <Value>0</Value>
            <Visible>IsStation == 1</Visible>                    
            <ValueType>Integer</ValueType>
        </Parameter>        

        <Parameter>
            <Name>ControlPointOffset</Name>
            <Text>Control point offset</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
        </Parameter>  
        
    </Page>
</Element>
