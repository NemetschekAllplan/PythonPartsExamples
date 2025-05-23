<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>GeometryExamples\Operations\QuantityTakeOff\CenterCalculus.py</Name>
    <Title>Center calculation</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>SelectGeometry</Name>
    <Text>Center calculation of curves</Text>
    <Parameters>
      <Parameter>
        <Name>DescriptionText</Name>
        <Text>Selectable objects:</Text>
        <Value>2D and 3D curves
Hatching
Filling
Pattern</Value>
        <ValueType>Text</ValueType>
      </Parameter>
      <Parameter>
        <Name>CenterCalculusOptions</Name>
        <Text>Options of CenterCalculus</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PolygonOptionsText</Name>
            <Text>For polygons and polylines:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>EdgeNumber</Name>
            <Text>Number of the edge (0 = whole curve)</Text>
            <Value>0</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>ClosedPolygonOptionsText</Name>
            <Text>For closed polygons only:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>PlaneCenter</Name>
            <Text>Calculate center of:</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>PlaneCenterFalse</Name>
                <Text>curve / edge</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>PlaneCenterTrue</Name>
                <Text>area bounded by the polygon</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>ArcOptionsText</Name>
            <Text>For arcs:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>ArcCenter</Name>
            <Text>Calculate:</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>ArcCenterFalse</Name>
                <Text>arc center</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>ArcCenterTrue</Name>
                <Text>curve center</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>SplineOptionsText</Name>
            <Text>For splines and clothoids:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>Precision</Name>
            <Text>Precision</Text>
            <Value>0</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>ClosedBSplineOptionsText</Name>
            <Text>For closed BSpline3D only:</Text>
            <Value/>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>AreaCenter</Name>
            <Text>Calculate center of:</Text>
            <Value>0</Value>
            <ValueType>RadioButtonGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>AreaCenterFalse</Name>
                <Text>spline curve</Text>
                <Value>0</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
              <Parameter>
                <Name>AreaCenterTrue</Name>
                <Text>area bounded by the spline</Text>
                <Value>1</Value>
                <ValueType>RadioButton</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>CreateCGPoint</Name>
            <Text>Create CG symbol</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>CGSymbolPropertiesExpander</Name>
        <Text>CG symbol properties</Text>
        <ValueType>Expander</ValueType>
        <Visible>CreateCGPoint</Visible>
        <Parameters>
          <Parameter>
            <Name>CGSymbolCommonProp</Name>
            <Text/>
            <Value/>
            <ValueType>CommonProperties</ValueType>
          </Parameter>
          <Parameter>
            <Name>CGSymbolSize</Name>
            <Text>Symbol size</Text>
            <Value>100</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
