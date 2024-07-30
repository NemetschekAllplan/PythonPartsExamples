<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\Text.py</Name>
        <Title>Text</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>TextTest</Text>

        <Parameter>
            <Name>StaticTextExp</Name>
            <Text>Static text</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>SingleText1</Name>
                <Text>First text is</Text>
                <Value>Hi</Value>
                <ValueTextId>1001</ValueTextId>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>SingleText2</Name>
                <Text>Second text is</Text>
                <Value>Hello</Value>
                <ValueTextId>1002</ValueTextId>
                <ValueType>Text</ValueType>
            </Parameter>

            <Parameter>
                <Name>Row1</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>FirstText</Name>
                    <Text></Text>
                    <Value>X</Value>
                    <ValueType>Text</ValueType>
                    <FontStyle>1</FontStyle>
                    <FontFaceCode>1</FontFaceCode>
                </Parameter>

                <Parameter>
                    <Name>SecondText</Name>
                    <Text></Text>
                    <Value>Y</Value>
                    <ValueType>Text</ValueType>
                    <FontStyle>2</FontStyle>
                    <FontFaceCode>2</FontFaceCode>
                </Parameter>

                <Parameter>
                    <Name>ThirdText</Name>
                    <Text></Text>
                    <Value>Z</Value>
                    <ValueType>Text</ValueType>
                    <FontStyle>2</FontStyle>
                    <FontFaceCode>4</FontFaceCode>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row2</Name>
                <Text>Cube dimensions</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>X</Name>
                    <Text>X</Text>
                    <Value>1000.0</Value>
                    <ValueType>Length</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Y</Name>
                    <Text>Y</Text>
                    <Value>2000.0</Value>
                    <ValueType>Length</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Z</Name>
                    <Text>Z</Text>
                    <Value>3000.0</Value>
                    <ValueType>Length</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row3</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>PenText</Name>
                    <Text></Text>
                    <Value>Pen</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>StrokeText</Name>
                    <Text></Text>
                    <Value>Stroke</Value>
                    <ValueType>Text</ValueType>
                </Parameter>

                <Parameter>
                    <Name>ColorText</Name>
                    <Text></Text>
                    <Value>Color</Value>
                    <ValueType>Text</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Row4</Name>
                <Text>Cube formats</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>Pen</Name>
                    <Text>Pen</Text>
                    <Value>1</Value>
                    <ValueType>Pen</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Stroke</Name>
                    <Text>Stroke</Text>
                    <Value>1</Value>
                    <ValueType>Stroke</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Color</Name>
                    <Text>Color</Text>
                    <Value>7</Value>
                    <ValueType>Color</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Orientation</Name>
            <Text>Orientation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>OrientationLeft</Name>
                <Text>Left</Text>
                <Value>Left</Value>
                <ValueType>Text</ValueType>
                <Orientation>Left</Orientation>
            </Parameter>
            <Parameter>
                <Name>OrientationMiddle</Name>
                <Text>Middle</Text>
                <Value>Middle</Value>
                <ValueType>Text</ValueType>
                <Orientation>Middle</Orientation>
            </Parameter>
            <Parameter>
                <Name>OrientationRight</Name>
                <Text>Right</Text>
                <Value>Right</Value>
                <ValueType>Text</ValueType>
                <Orientation>Right</Orientation>
            </Parameter>
        </Parameter>
    </Page>
</Element>
