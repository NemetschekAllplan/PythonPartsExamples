<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ArchitectureExamples\Objects\FlushPier.py</Name>
        <Title>Flush Pier</Title>
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
        <Name>Page1</Name>
        <Text>Main Page</Text>

        <Parameter>
            <Name>GeometryExp</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>
   
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>1010</Value>
                <ValueType>Length</ValueType>
                <MinValue>10</MinValue>
            </Parameter>

            <Parameter>
                <Name>HeightSettings</Name>
                <Text>Height</Text>
                <Value>PlaneReferences</Value>
                <ValueType>PlaneReferences</ValueType>
                <ValueDialog>PlaneReferences</ValueDialog>
            </Parameter>     
        </Parameter>

        <Parameter>
            <Name>AttributesExp</Name>
            <Text>Attributes</Text>
            <ValueType>Expander</ValueType>
   
            <Parameter>
                <Name>Trade</Name>
                <Text>Trade</Text>
                <Value>-1</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>Trade</ValueDialog>
            </Parameter>

            <Parameter>
                <Name>Priority</Name>
                <Text>Priority</Text>
                <Value>100</Value>
                <ValueType>Integer</ValueType>                
            </Parameter>            

            <Parameter>
                <Name>CalculationMode</Name>
                <Text>Calculation mode</Text>
                <Value>0</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>120</AttributeId>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>MaterialSelectionExp</Name>
            <Text>Material Selection</Text>
            <ValueType>Expander</ValueType>
   
            <Parameter>
                <Name>Material</Name>
                <Text>Material</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>

            <Parameter>
                <Name>Status</Name>
                <Text>Status</Text>
                <Value>6</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>49</AttributeId>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>FormatPropertiesExpander</Name>
            <Text>Format properties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SetFormatProperties</Name>
                <Text>Set format properties</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>                    
            </Parameter>

            <Parameter>
                <Name>CommonProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>
        
        <Parameter>
            <Name>SurfaceElementsExp</Name>
            <Text>Surface elements</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElemProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>SurfaceElementProperties</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>
            
            <Parameter>
                <Name>SurfaceRow</Name>
                <Text>Surface (Animation)</Text>                
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsSurface</Name>
                    <Text>Surface</Text>                    
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>SurfaceName</Name>
                    <Text>Surface</Text>                    
                    <Value></Value>
                    <ValueType>MaterialButton</ValueType>                    
                </Parameter>
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

        <Parameter>
            <Name>ElementTierCount</Name>
            <Text>Element tier count</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
        </Parameter>

    </Page>
</Element>
