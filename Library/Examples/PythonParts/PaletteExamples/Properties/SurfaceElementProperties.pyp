<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Properties\SurfaceElementProperties.py</Name>
        <Title>SurfaceElementProperties</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>Width</Name>
            <Text>Width</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter> 

        <Parameter>
            <Name>SurfaceElemPropExp</Name>
            <Text>SurfaceElementProperties</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElementProp</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>SurfaceElementProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SurfaceElemPropCondExp</Name>
            <Text>SurfaceElementProperties with visible condition</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElementPropCond</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>SurfaceElementProperties</ValueType>
                <Visible>|SurfaceElementPropCond.BitmapSelected:False|SurfaceElementPropCond.BitmapID:False|
                |SurfaceElementPropCond.FillingSelected:False|SurfaceElementPropCond.FillingID:False</Visible>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SingleParameterExp</Name>
            <Text>Single Parameter</Text>
            <ValueType>Expander</ValueType>

             <Parameter>
                <Name>UseAreaInGroundplan</Name>
                <Text>Display in plan view</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>                    
            </Parameter>

            <Parameter>
                <Name>HatchRow</Name>
                <Text>Hatching</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsHatch</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>                    
                </Parameter>
                <Parameter>
                    <Name>HatchId</Name>
                    <Value>303</Value>
                    <ValueType>Hatch</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>PatternRow</Name>
                <Text>Pattern</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsPattern</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>                    
                </Parameter>
                <Parameter>
                    <Name>PatternId</Name>
                    <Value>301</Value>
                    <ValueType>Pattern</ValueType>                    
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FillingRow</Name>
                <Text>Fill</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsFilling</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>                    
                </Parameter>
                <Parameter>
                    <Name>FillingId</Name>
                    <TextId>e_FILLING</TextId>
                    <Value>24</Value>
                    <ValueType>Color</ValueType>                    
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>FaceStyleRow</Name>
                <Text>Style area</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsFaceStyle</Name>
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>                    
                </Parameter>
                <Parameter>
                    <Name>FaceStyleId</Name>
                    <Value>301</Value>
                    <ValueType>FaceStyle</ValueType>                    
                </Parameter>
            </Parameter>            

            <Parameter>
                <Name>BitmapRow</Name>
                <Text>Bitmap area</Text>                
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>IsBitmap</Name>
                    <Text>Bitmap</Text>                    
                    <Value>False</Value>
                    <ValueType>CheckBox</ValueType>
                </Parameter>
                <Parameter>
                    <Name>BitmapName</Name>
                    <Text>Bitmap</Text>                    
                    <Value></Value>
                    <ValueType>String</ValueType>
                    <ValueDialog>BitmapResourceDialog</ValueDialog>
                </Parameter>
            </Parameter>
        </Parameter>
        
    </Page>
    <Page>
        <Name>List</Name>
        <Text>List</Text>

        <Parameter>
            <Name>SurfaceElemPropListExp</Name>
            <Text>SurfaceElementProperties list</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SurfaceElemPropCount</Name>
                <Text>Count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>SurfaceElemPropSep</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>SurfaceElemPropList</Name>
                <Text></Text>
                <TextDyn>"Column " + str($list_row + 1)</TextDyn>
                <Value>[SurfaceElementProperties();SurfaceElementProperties();SurfaceElementProperties()]</Value>
                <ValueType>SurfaceElementProperties</ValueType>
                <Dimensions>SurfaceElemPropCount</Dimensions>
            </Parameter>
        </Parameter>
    </Page>
</Element>
