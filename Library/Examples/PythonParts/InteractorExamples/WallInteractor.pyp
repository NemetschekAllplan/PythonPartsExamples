<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\WallInteractor.py</Name>
    <Title>WallInteractor</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>Wall</Name>
    <Text>Wall</Text>
    <Parameters>
      <Parameter>
        <Name>IsPythonPart</Name>
        <Text>Create PythonPart</Text>
        <Value>False</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>TierCount</Name>
        <Text>Tier count</Text>
        <Value>2</Value>
        <ValueType>Integer</ValueType>
        <MinValue>1</MinValue>
        <MaxValue>20</MaxValue>
      </Parameter>
      <Parameter>
        <Name>Row0</Name>
        <Text> </Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>ThicknessText</Name>
            <Value>Tier thickness</Value>
            <ValueType>Text</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Thickness</Name>
        <Text/>
        <Value>[240,160]</Value>
        <ValueType>Length</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueListStartRow>1</ValueListStartRow>
      </Parameter>
      <Parameter>
        <Name>OverallThickness</Name>
        <Text>Overall thickness</Text>
        <Value>400</Value>
        <ValueType>Length</ValueType>
        <Enable>False</Enable>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>AxisFromTop</Name>
        <Text>Axis distance from top</Text>
        <Value>0</Value>
        <ValueType>Length</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>OverallThickness</MaxValue>
      </Parameter>
      <Parameter>
        <Name>AxisFromBottom</Name>
        <Text>Axis distance from bottom</Text>
        <Value>400</Value>
        <ValueType>Length</ValueType>
        <MinValue>0</MinValue>
        <MaxValue>OverallThickness</MaxValue>
      </Parameter>
      <Parameter>
        <Name>MirroTiers</Name>
        <Text>Mirror tiers at axis</Text>
        <Value>False</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Page1</Name>
    <Text>Tier</Text>
    <Parameters>
      <Parameter>
        <Name>Row</Name>
        <Text>Tier number</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>TierIndex</Name>
            <Text/>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
            <Enable>True</Enable>
            <MinValue>1</MinValue>
            <MaxValue>TierCount</MaxValue>
          </Parameter>
          <Parameter>
            <Name>NextTier</Name>
            <Text/>
            <Value>arrowup.png</Value>
            <EventId>1001</EventId>
            <ValueType>PictureButton</ValueType>
            <Enable>TierIndex &lt; TierCount</Enable>
          </Parameter>
          <Parameter>
            <Name>PreviousTier</Name>
            <Text/>
            <Value>arrowdown.png</Value>
            <EventId>1002</EventId>
            <ValueType>PictureButton</ValueType>
            <Enable>TierIndex &gt; 1</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Row1</Name>
        <Text>Plane references</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>PlaneReferences</Name>
            <Text/>
            <Value>[None] * 2</Value>
            <ValueType>PlaneReferences</ValueType>
            <ValueDialog>PlaneReferences</ValueDialog>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Material</Name>
        <Text>Material</Text>
        <TextId>e_MATERIAL</TextId>
        <Value>[""] * 2</Value>
        <ValueType>String</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
      </Parameter>
      <Parameter>
        <Name>Row2</Name>
        <Text>Trade</Text>
        <TextId>e_TRADE</TextId>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>Trade</Name>
            <Value>[0] * 2</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>Trade</ValueDialog>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>Layer</Name>
        <Text>Layer</Text>
        <TextId>e_LAYER</TextId>
        <Value>[-1] * 2</Value>
        <ValueType>Layer</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
      </Parameter>
      <Parameter>
        <Name>Pen</Name>
        <Text>Pen</Text>
        <TextId>e_PEN</TextId>
        <Value>[1] * 2</Value>
        <ValueType>Pen</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
        <Enable>not PenByLayer[TierIndex - 1]</Enable>
      </Parameter>
      <Parameter>
        <Name>PenByLayer</Name>
        <Text>Pen by layer</Text>
        <TextId>e_PEN_BY_LAYER</TextId>
        <Value>[False] * 2</Value>
        <ValueType>CheckBox</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
      </Parameter>
      <Parameter>
        <Name>Stroke</Name>
        <Text>Linetype</Text>
        <TextId>e_LINETYPE</TextId>
        <Value>[1] * 2</Value>
        <ValueType>Stroke</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
        <Enable>not StrokeByLayer[TierIndex - 1]</Enable>
      </Parameter>
      <Parameter>
        <Name>StrokeByLayer</Name>
        <Text>Linetype by layer</Text>
        <TextId>e_LINETYPE_BY_LAYER</TextId>
        <Value>[False] * 2</Value>
        <ValueType>CheckBox</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
      </Parameter>
      <Parameter>
        <Name>Color</Name>
        <Text>Color</Text>
        <TextId>e_COLOR</TextId>
        <Value>[7] * 2</Value>
        <ValueType>Color</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
        <Enable>not ColorByLayer[TierIndex - 1]</Enable>
      </Parameter>
      <Parameter>
        <Name>ColorByLayer</Name>
        <Text>Color by layer</Text>
        <TextId>e_COLOR_BY_LAYER</TextId>
        <Value>[False] * 2</Value>
        <ValueType>CheckBox</ValueType>
        <Dimensions>TierCount</Dimensions>
        <ValueIndexName>TierIndex</ValueIndexName>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>HatchRow</Name>
        <Text>Hatch ID</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>IsHatch</Name>
            <Value>[True, False]</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
          <Parameter>
            <Name>HatchId</Name>
            <Value>[303, 303]</Value>
            <ValueType>Hatch</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>PatternRow</Name>
        <Text>Pattern ID</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>IsPattern</Name>
            <Value>[False, True]</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
          <Parameter>
            <Name>PatternId</Name>
            <Value>[301, 301]</Value>
            <ValueType>Pattern</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>FaceStyleRow</Name>
        <Text>FaceStyle ID</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>IsFaceStyle</Name>
            <Value>[False] * 2</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
          <Parameter>
            <Name>FaceStyleId</Name>
            <Value>[301] * 2</Value>
            <ValueType>FaceStyle</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>FillingRow</Name>
        <Text>Filling ID</Text>
        <ValueType>Row</ValueType>
        <Parameters>
          <Parameter>
            <Name>IsFilling</Name>
            <Value>[False] * 2</Value>
            <ValueType>CheckBox</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
          <Parameter>
            <Name>FillingId</Name>
            <TextId>e_FILLING</TextId>
            <Value>[24] * 2</Value>
            <ValueType>Color</ValueType>
            <Dimensions>TierCount</Dimensions>
            <ValueIndexName>TierIndex</ValueIndexName>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Text/>
    <Parameters>
      <Parameter>
        <Name>StartPoint</Name>
        <Value/>
        <ValueType>Point3D</ValueType>
      </Parameter>
      <Parameter>
        <Name>EndPoint</Name>
        <Value/>
        <ValueType>Point3D</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
