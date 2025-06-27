<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Chamfer.py</Name>
    <Title>Chamfer</Title>
    <Version>1.0</Version>
  </Script>
  <!--<Page>
        <Name>Line3D</Name>
        <Text>Line3D</Text>

        <Parameter>
            <Name>Color2</Name>
            <Text>Line color</Text>
            <Value>2</Value>
            <ValueType>Color</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1X1_2</Name>
            <Text>line 1 start pointx</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1Y1_2</Name>
            <Text>                   y</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1Z1_2</Name>
            <Text>                   z</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1X2_2</Name>
            <Text>line 1 end point x</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1Y2_2</Name>
            <Text>                 y</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line1Z2_2</Name>
            <Text>                 z</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2X1_2</Name>
            <Text>line 1 start pointx</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2Y1_2</Name>
            <Text>                   y</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2Z1_2</Name>
            <Text>                   z</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2X2_2</Name>
            <Text>line 1 end point x</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2Y2_2</Name>
            <Text>                 y</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>Line2Z2_2</Name>
            <Text>                 z</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>PointX_2</Name>
            <Text>Point through which chamfer is to pass x</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>PointY_2</Name>
            <Text>           y</Text>
            <Value>500.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>PointZ_2</Name>
            <Text>           y</Text>
            <Value>0.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>-->
  <Page>
    <Name>Polyhedron3D</Name>
    <Text>Polyhedron3D</Text>
    <Parameters>
      <Parameter>
        <Name>Color4</Name>
        <Text>Line color</Text>
        <Value>4</Value>
        <ValueType>Color</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length4</Name>
        <Text>Length</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width4</Name>
        <Text>Width</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness4</Name>
        <Text>Thickness</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>ChamferWidth4</Name>
        <Text>Chamfer width</Text>
        <Value>200.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Edges4</Name>
        <Text>Edges</Text>
        <Value>4, 5, 6, 7</Value>
        <ValueType>String</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>BRep3D</Name>
    <Text>BRep3D</Text>
    <Parameters>
      <Parameter>
        <Name>Color5</Name>
        <Text>Line color</Text>
        <Value>5</Value>
        <ValueType>Color</ValueType>
      </Parameter>
      <Parameter>
        <Name>Length5</Name>
        <Text>Length</Text>
        <Value>1500.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width5</Name>
        <Text>Width</Text>
        <Value>2000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Thickness5</Name>
        <Text>Thickness</Text>
        <Value>1000.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>ChamferWidth5</Name>
        <Text>Chamfer width</Text>
        <Value>200.</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Edges5</Name>
        <Text>Edges</Text>
        <Value>4, 5, 6, 7</Value>
        <ValueType>String</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
