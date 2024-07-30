<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Visibility.py</Name>
        <Title>Visibility</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <Parameter>
            <Name>CheckBox1</Name>
            <Text>Define Pen</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>CheckBox2</Name>
            <Text>Define also Stroke and Color</Text>
            <Value>False</Value>
            <Visible>CheckBox1 == True</Visible>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>CheckBox3</Name>
            <Text>Show second page</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>EnableSecondPage</Name>
            <Text>Enable second page controls</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
        </Parameter>

        <Parameter>
            <Name>Pen</Name>
            <Text>Pen</Text>
            <Value>1</Value>
            <!-- <Enable>CheckBox1 == True</Enable> see possible implementation of the enable function in the py file -->
            <ValueType>Pen</ValueType>
        </Parameter>
        <Parameter>
            <Name>Stroke</Name>
            <Text>Stroke</Text>
            <Value>1</Value>
            <Visible>CheckBox1 == True and CheckBox2 == True</Visible>
            <ValueType>Stroke</ValueType>
        </Parameter>
        <Parameter>
            <Name>Color</Name>
            <Text>Color</Text>
            <Value>1</Value>
            <Visible>
if CheckBox1 and CheckBox2:
    return True
return False
            </Visible>
            <ValueType>Color</ValueType>
        </Parameter>

        <Parameter>
            <Name>CheckBox4</Name>
            <Text>Show geometry data expander</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>Expander</Name>
            <Text>Expander</Text>
            <ValueType>Expander</ValueType>
            <Visible>CheckBox4 == True</Visible>

            <Parameter>
                <Name>CheckBox5</Name>
                <Text>Define geometry</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>GeometryType</Name>
                <Text>Geometry type</Text>
                <Value>1</Value>
                <ValueType>RadioButtonGroup</ValueType>
                <Visible>CheckBox5 == True</Visible>

                <Parameter>
                    <Name>GeometryType1</Name>
                    <Text>Polyhedron</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>GeometryType2</Name>
                    <Text>Cylinder</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row1</Name>
                <Text>Polyhedron</Text>
                <ValueType>Row</ValueType>
                <Visible>CheckBox5 == True  and  GeometryType == 1</Visible>

                <Parameter>
                    <Name>Length</Name>
                    <Text>Length</Text>
                    <Value>1000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Width</Name>
                    <Text>Width</Text>
                    <Value>1000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Height</Name>
                    <Text>Height</Text>
                    <Value>1000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row2</Name>
                <Text>Cylinder</Text>
                <ValueType>Row</ValueType>
                <!-- <Visible>CheckBox4 == True  and  GeometryType == 2</Visible> see possible implementation of the visible function in the py file -->

                <Parameter>
                    <Name>CylinderRadius</Name>
                    <Text>Radius</Text>
                    <Value>500.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
                <Parameter>
                    <Name>CylinderHeight</Name>
                    <Text>Height</Text>
                    <Value>2000.</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Page2</Name>
        <Text>Page2</Text>
        <Visible>CheckBox3</Visible>
        <Enable>
if EnableSecondPage:
    return True
return False
        </Enable>

        <Parameter>
            <Name>Text1</Name>
            <Text>Text 1</Text>
            <Value>First text</Value>
            <ValueType>String</ValueType>
        </Parameter>
        <Parameter>
            <Name>Text2</Name>
            <Text>Text 2</Text>
            <Value>Sedond text</Value>
            <ValueType>String</ValueType>
        </Parameter>
    </Page>
</Element>
