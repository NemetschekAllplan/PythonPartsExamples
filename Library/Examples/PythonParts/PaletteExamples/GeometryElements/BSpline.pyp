<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\GeometryElements\BSpline.py</Name>
        <Title>BSpline</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>

    <!-- <Page>                             currently not possible to create a BSpline2D in Allplan
        <Name>Page1</Name>
        <Text>2D bspline</Text>

        <Parameter>
            <Name>Format2D</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp2D</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BSpline2DSingleRowExp</Name>
            <Text>BSpline - Single row for x/y</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BSpline1</Name>
                <Text>Point</Text>
                <Value>BSpline2D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((0,7000)(1000,9100)(3000,6000)(6000,9000)))</Value>
                <ValueType>BSpline2D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BSpline2DOneRowExp</Name>
            <Text>BSpline - One row for x/y</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BSpline2</Name>
                <Text>Point</Text>
                <Value>BSpline2D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((12000,7000)(13000,9100)(15000,6000)(18000,9000)))</Value>
                <ValueType>BSpline2D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BSpline2DOneRowExp</Name>
            <Text>List of BSpline2D</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BSplineCount</Name>
                <Text>BSpline count</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>BSplineList</Name>
                <Text>Point</Text>
                <Value>[BSpline2D(StartVector(1, 1)EndVector(1, 1)Points((11000,2000)(13000,3100)(14000,3500)(15000,0)));BSpline2D(StartVector(1, 1)EndVector(1, 1)Points((15000,2000)(16000,3100)(17000,3500)(20000,0)))]</Value>
                <ValueType>BSpline2D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>BSplineCount</Dimensions>
            </Parameter>
        </Parameter>
    </Page> -->

    <Page>
        <Name>Page2</Name>
        <Text>3D bspline</Text>

        <Parameter>
            <Name>Format3D</Name>
            <Text>Format</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>CommonProp3D</Name>
                <Text></Text>
                <Value></Value>
                <ValueType>CommonProperties</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BSpline3DSingleRowExp</Name>
            <Text>BSpline - Single row for x/y/z</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BSpline6</Name>
                <Text>Point</Text>
                <Value>BSpline3D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((0,0,0)(1000,2100,1000)(3000,-1000,3000)(6000,2000,0)))</Value>
                <ValueType>BSpline3D</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>BSpline3DOneRowExp</Name>
            <Text>BSpline - One row for x/y/z</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BSpline7</Name>
                <Text>Point</Text>
                <Value>BSpline3D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((12000,0,0)(13000,2100,1000)(15000,4000,3000)(18000,2000,0)))</Value>
                <ValueType>BSpline3D</ValueType>
                <XYZinRow>True</XYZinRow>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Page2</Name>
        <Text>3D bspline list</Text>

        <Parameter>
            <Name>BSpline3DListExp</Name>
            <Text>List of BSpline3yD</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Format3D</Name>
                <Text>Format</Text>
                <ValueType>Expander</ValueType>

                <Parameter>
                    <Name>CommonProp3DList</Name>
                    <Text></Text>
                    <Value>CommonProperties(Color(5))</Value>
                    <ValueType>CommonProperties</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>BSplineCount</Name>
                <Text>BSpline count</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>BSplineList</Name>
                <Text>Point</Text>
                <Value>[BSpline3D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((0,7000,0)(1000,9100,1000)(3000,6000,3000)(6000,9000,0)));BSpline3D(IsPeriodic(0)Degree(3)Weights()Knots(0,0,0,0,1,1,1,1)Points((12000,7000,0)(13000,9100,1000)(15000,6000,3000)(18000,9000,0)))]</Value>
                <ValueType>BSpline3D</ValueType>
                <ValueListStartRow>1</ValueListStartRow>
                <Dimensions>BSplineCount</Dimensions>
            </Parameter>
        </Parameter>
    </Page>
</Element>
