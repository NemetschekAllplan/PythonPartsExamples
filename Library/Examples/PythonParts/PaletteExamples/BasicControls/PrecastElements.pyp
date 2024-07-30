<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\PrecastElements.py</Name>
        <Title>PrecastElements</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>PrecastElements</Text>

        <Parameter>
            <Name>Factory</Name>
            <Text>Factory</Text>
            <ValueType>FactoryCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Norm</Name>
            <Text>Norm</Text>
            <ValueType>NormCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Concrete</Name>
            <Text>Concrete</Text>
            <ValueType>ConcreteGradeCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Fixture</Name>
            <Text>Fixture</Text>
            <ValueType>FixtureCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>PointFixture</Name>
            <Text>Point fixture</Text>
            <ValueType>PointFixtureCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>LineFixture</Name>
            <Text>Line fixture</Text>
            <ValueType>LineFixtureCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>AreaFixture</Name>
            <Text>Area fixture</Text>
            <ValueType>AreaFixtureCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Insulation</Name>
            <Text>Insulation</Text>
            <ValueType>InsulationCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Tile/Brick</Name>
            <Text>Tile/Brick</Text>
            <ValueType>BrickTileCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Element</Name>
            <Text>Element</Text>
            <ValueType>PrecastElementTypeCatalogReference</ValueType>
        </Parameter>

        <Parameter>
            <Name>Layer</Name>
            <Value>[]</Value>
            <ValueType>tuple(Text,Length,Text,MaterialCatalogReference)</ValueType>
            <Visible>True,False,False,True</Visible>
         </Parameter>

         <Parameter>
            <Name>SurfaceCatalogReference</Name>
            <Text>Surface catalog reference</Text>
            <ValueType>SurfaceCatalogReference</ValueType>
         </Parameter>

         <Parameter>
            <Name></Name>
            <ValueType>Separator</ValueType>
        </Parameter>

         <Parameter>
            <Name>FixtureElement</Name>
            <Text>Fixture</Text>
            <ValueType>Fixture</ValueType>
         </Parameter>
    </Page>
</Element>
