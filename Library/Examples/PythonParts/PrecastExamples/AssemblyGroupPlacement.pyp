<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PrecastExamples\AssemblyGroupPlacement.py</Name>
    <Title>AssemblyGroupPlacement</Title>
    <Version>1.0</Version>
  </Script>
  <Page>
    <Name>Page1</Name>
    <Text>AssemblyGroup</Text>
    <Parameters>
      <Parameter>
        <Name>Length</Name>
        <TextId>1000</TextId>
        <Text>Length</Text>
        <Value>1000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Width</Name>
        <TextId>1001</TextId>
        <Text>Width</Text>
        <Value>2000</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Height</Name>
        <TextId>1002</TextId>
        <Text>Height</Text>
        <Value>200</Value>
        <ValueType>Length</ValueType>
      </Parameter>
      <Parameter>
        <Name>Library_Expander</Name>
        <TextId>1003</TextId>
        <Text>Library_Expander</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>LibraryPlacePoint</Name>
            <TextId>1004</TextId>
            <Text>Point</Text>
            <Value>200,400,100</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>Fixture_library</Name>
            <Text>Libraryfixture</Text>
            <TextId>1005</TextId>
            <Value>Etc\Library\Fixtures\Floors\ElectricalOutlets\E-Dose.pfx</Value>
            <ValueType>String</ValueType>
            <ValueDialog>FixtureDialog</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Fixture_Expander</Name>
        <TextId>1006</TextId>
        <Text>Fixture_Expander</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FixLength</Name>
            <TextId>1000</TextId>
            <Text>Length</Text>
            <Value>250</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>FixWidth</Name>
            <TextId>1001</TextId>
            <Text>Width</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>FixHeight</Name>
            <TextId>1002</TextId>
            <Text>Height</Text>
            <Value>75</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>FixturePlacePoint</Name>
            <TextId>1004</TextId>
            <Text>Point</Text>
            <Value>100,100,125</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
          <Parameter>
            <Name>Fixture_Name</Name>
            <TextId>1007</TextId>
            <Text>Fixturename</Text>
            <Value>Fix1</Value>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>CatRef</Name>
            <TextId>1008</TextId>
            <Text>Catalogs reference</Text>
            <Value>E-Dose</Value>
            <ValueType>PointFixtureCatalogReference</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Steel_Expander</Name>
        <TextId>1009</TextId>
        <Text>Steel_Expander</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SteelGrade</Name>
            <TextId>1010</TextId>
            <Text>Steel grade</Text>
            <Value>4</Value>
            <ValueType>ReinfSteelGrade</ValueType>
          </Parameter>
          <Parameter>
            <Name>BendingRoller</Name>
            <TextId>1011</TextId>
            <Text>Bending roller</Text>
            <Value>4</Value>
            <ValueType>ReinfBendingRoller</ValueType>
          </Parameter>
          <Parameter>
            <Name>DiameterShape1</Name>
            <TextId>1012</TextId>
            <Text>Bar diameter Shape 1</Text>
            <Value>10</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverShape1</Name>
            <TextId>1013</TextId>
            <Text>Concrete cover shape 1</Text>
            <Value>25</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>DistanceShape1</Name>
            <TextId>1014</TextId>
            <Text>Bar spacing</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
          </Parameter>
          <Parameter>
            <Name>DiameterShape2</Name>
            <TextId>1015</TextId>
            <Text>Bar diameter Shape 2</Text>
            <Value>20</Value>
            <ValueType>ReinfBarDiameter</ValueType>
          </Parameter>
          <Parameter>
            <Name>ConcreteCoverShape2</Name>
            <TextId>1016</TextId>
            <Text>Concrete cover shape 2</Text>
            <Value>35</Value>
            <ValueType>ReinfConcreteCover</ValueType>
          </Parameter>
          <Parameter>
            <Name>DistanceShape2</Name>
            <TextId>1017</TextId>
            <Text>Bar spacing</Text>
            <Value>200</Value>
            <ValueType>Length</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ASG_Expander</Name>
        <TextId>1018</TextId>
        <Text>ASG_Expander</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Name</Name>
            <TextId>1007</TextId>
            <Text>Name</Text>
            <Value>ASG_1</Value>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>Number</Name>
            <TextId>1019</TextId>
            <Text>Number</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
