<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\Layout\Picture.py</Name>
        <Title>Picture</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>Picture1</Name>
            <Value>PictureForPalette.png</Value>    <!-- referencing local image -->
            <Orientation>Left</Orientation>
            <ValueType>Picture</ValueType>
        </Parameter>

        <Parameter>
            <Name>Picture2</Name>
            <Value>PictureForPalette.png</Value>    <!-- referencing local image -->
            <Orientation>Middle</Orientation>
            <ValueType>Picture</ValueType>
        </Parameter>

        <Parameter>
            <Name>Picture3</Name>
            <Value>11851</Value>                    <!-- referencing Allplan resource image -->
            <Orientation>Right</Orientation>
            <ValueType>Picture</ValueType>
        </Parameter>

        <Parameter>
            <Name>RowLength</Name>
            <Text>Length</Text>
            <TextId>e_LENGTH</TextId>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>LengthParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam01</Value>        <!-- referencing Allplan picture resource -->
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowWidth</Name>
            <Text>Width</Text>
            <TextId>e_WIDTH</TextId>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Width</Name>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>WidthParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam02</Value>
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>RowHeight</Name>
            <Text>Height</Text>
            <TextId>e_HEIGHT</TextId>
            <ValueType>Row</ValueType>

            <Parameter>
                <Name>Height</Name>
                <Value>500.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>HeightParamPicture</Name>
                <Value>AllplanSettings.PictResParam.eParam03</Value>
                <ValueType>Picture</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
