<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PaletteExamples\ValueList.py</Name>
    <Title>ValueList</Title>
    <Version>1.0</Version>
  </Script>
  <Constants>
    <Constant>
      <Name>BUTTON_GROUP_EVENT_ID</Name>
      <Value>1000</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>BUTTON_GROUP_EVENT_ID2</Name>
      <Value>2000</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>ValueList</Name>
    <Text>General lists</Text>
    <Parameters>
      <Parameter>
        <Name>Expander1</Name>
        <Text>1-dim. "Length" list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CubeCount</Name>
            <Text>Number of cubes</Text>
            <Value>5</Value>
            <MinValue>0</MinValue>
            <MaxValue>10</MaxValue>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Row0</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Dimension</Name>
                <Value>Cube dimension</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>CubeDimensions</Name>
            <Text/>
            <Value>[1000.,1200.,1400.,1600.,1800.]</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
            <ValueListStartRow>1</ValueListStartRow>
            <Dimensions>1 + CubeCount - 1</Dimensions>
            <!-- for testing -->
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>2-dim. "Length" list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>CoordDimension3D</Name>
            <Text>Coord. dim. 3D</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>Row1</Name>
            <Text> </Text>
            <Value>1</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Number</Name>
                <Value>Nr.</Value>
                <ValueType>Text</ValueType>
                <WidthInRow>10</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>X</Name>
                <Value>X</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>Y</Name>
                <Value>Y</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>Z</Name>
                <Value>Z</Value>
                <ValueType>Text</ValueType>
                <Visible>CoordDimension3D</Visible>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>CoordinatesRow</Name>
            <Text/>
            <Value>1</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Coordinates</Name>
                <Text>Coordinate</Text>
                <Value>[[0 for x in range(3)] for y in range(5)]</Value>
                <ValueType>Length</ValueType>
                <Dimensions>CubeCount,CoordDimension3D + 2</Dimensions>
                <ValueListStartRow>1</ValueListStartRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>"tuple" list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>Row2</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>TextHeight</Name>
                <Value>Text height</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>Text</Name>
                <Value>Text</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>TextData</Name>
            <Text/>
            <Value>[10|Cube] * 5</Value>
            <ValueType>tuple(Double,String)</ValueType>
            <MinValue>5,"?"</MinValue>
            <Dimensions>CubeCount</Dimensions>
            <ValueListStartRow>1</ValueListStartRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander2</Name>
        <Text>"tuple" list with one visible row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>VisibleRefPointRow</Name>
            <Text>Visible reference point</Text>
            <Value>2</Value>
            <MinValue>1</MinValue>
            <MaxValue>CubeCount</MaxValue>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>Row1</Name>
            <Text>Reference point</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>X</Name>
                <Value>X</Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>Y</Name>
                <Value>Y</Value>
                <ValueType>Text</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Row2</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>RefPointLocation</Name>
                <Text/>
                <Value>[(Left|Bottom)] * 5</Value>
                <ValueList>Left|Center|Right,Bottom|Center|Top</ValueList>
                <ValueType>tuple(StringComboBox,StringComboBox)</ValueType>
                <Dimensions>CubeCount</Dimensions>
                <ValueListStartRow>1</ValueListStartRow>
                <ValueIndexName>VisibleRefPointRow</ValueIndexName>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>Strings</Name>
    <Text>String list</Text>
    <Parameters>
      <Parameter>
        <Name>Expander2</Name>
        <Text>2-dim. "Length" list</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>RowCount</Name>
            <Text>Row count</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>ColumnCount</Name>
            <Text>Column count</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>StringListRow</Name>
            <Text/>
            <Value>1</Value>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>StringList</Name>
                <Text>String</Text>
                <Value>[["Text1", "Text2"]] * 3</Value>
                <ValueType>String</ValueType>
                <Dimensions>1 + RowCount - 1,ColumnCount</Dimensions>
                <!-- for testing -->
                <ValueListStartRow>1</ValueListStartRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>ListGroupPage</Name>
    <Text>List group</Text>
    <Parameters>
      <Parameter>
        <Name>Expander3</Name>
        <Text>List group</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>SectionCount</Name>
            <Text>Sectioncount</Text>
            <Value>3</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ListGroup1</Name>
        <ValueType>ListGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>GroupExpander</Name>
            <Text>"Field " + str($list_row + 1)</Text>
            <ValueType>Expander</ValueType>
            <Parameters>
              <Parameter>
                <Name>SectionName</Name>
                <Text>Section name</Text>
                <Value>["A", "B", "C"]</Value>
                <ValueType>String</ValueType>
                <Dimensions>SectionCount</Dimensions>
              </Parameter>
              <Parameter>
                <Name>Distance</Name>
                <Text>Distance</Text>
                <Value>[1000, 2000, 0]</Value>
                <ValueType>Length</ValueType>
                <Dimensions>SectionCount</Dimensions>
                <Visible>$list_row &lt; SectionCount - 1</Visible>
              </Parameter>
              <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>0</Value>
                <ValueType>Length</ValueType>
                <Visible>$list_row == SectionCount - 1</Visible>
                <Enable>False</Enable>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>GroupButtonRow</Name>
            <Text>"Group " + str($list_row + 1)</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>GroupButton</Name>
                <Text>Edit</Text>
                <EventId>BUTTON_GROUP_EVENT_ID</EventId>
                <ValueType>Button</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ClickedButtonExpander</Name>
        <Text>Clicked button</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ButtonEventID</Name>
            <Text>Event ID</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>ButtonIndex</Name>
            <Text>Index</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GroupExpander2</Name>
        <Text>List group with Row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ListGroup2</Name>
            <ValueType>ListGroup</ValueType>
            <Parameters>
              <Parameter>
                <Name>GroupRow</Name>
                <Text>"Field " + str($list_row + 1)</Text>
                <ValueType>Row</ValueType>
                <Parameters>
                  <Parameter>
                    <Name>SectionName2</Name>
                    <Text>Section name</Text>
                    <Value>["a", "b", "c"]</Value>
                    <ValueType>String</ValueType>
                    <Dimensions>SectionCount</Dimensions>
                  </Parameter>
                  <Parameter>
                    <Name>Distance2</Name>
                    <Text>Distance</Text>
                    <Value>[11, 12, 13]</Value>
                    <ValueType>Double</ValueType>
                    <Dimensions>SectionCount</Dimensions>
                    <Visible>$list_row &lt; SectionCount - 1</Visible>
                  </Parameter>
                  <Parameter>
                    <Name>Length2</Name>
                    <Text>Length</Text>
                    <Value>0</Value>
                    <ValueType>Double</ValueType>
                    <Visible>$list_row == SectionCount - 1</Visible>
                    <Enable>False</Enable>
                  </Parameter>
                  <Parameter>
                    <Name>GroupButton2</Name>
                    <Text>Edit</Text>
                    <EventId>BUTTON_GROUP_EVENT_ID2</EventId>
                    <ValueType>Button</ValueType>
                  </Parameter>
                </Parameters>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ClickedButtonExpander2</Name>
        <Text>Clicked button</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>ButtonEventID2</Name>
            <Text>Event ID</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>ButtonIndex2</Name>
            <Text>Index</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>VisiblePage</Name>
    <Text>Enable/Visible item</Text>
    <Parameters>
      <Parameter>
        <Name>Expander41</Name>
        <Text>Enable and visible item by $list_row</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>EnableVisibleItemsByListRow</Name>
            <Text/>
            <Value>[1000.,1200.,1400.,1600.,1800.,2000]</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
            <Visible>$list_row != HideRowListRow</Visible>
            <Enable>$list_row != EnableRowListRow</Enable>
          </Parameter>
          <Parameter>
            <Name>HideRowListRow</Name>
            <Text>Hide row</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>5</MaxValue>
          </Parameter>
          <Parameter>
            <Name>EnableRowListRow</Name>
            <Text>Disable row</Text>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>5</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Expander42</Name>
        <Text>Enable and visible item by function</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>EnableVisibleItemsByFunction</Name>
            <Text/>
            <Value>[2000.,2200.,2400.,2600.,2800.,3000]</Value>
            <ValueType>Length</ValueType>
            <MinValue>100</MinValue>
          </Parameter>
          <Parameter>
            <Name>HideListRow</Name>
            <Text>Hide row</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>5</MaxValue>
          </Parameter>
          <Parameter>
            <Name>EnableListRow</Name>
            <Text>Disable row</Text>
            <Value>4</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>5</MaxValue>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>__HiddenPage__</Name>
    <Parameters>
      <Parameter>
        <Name>InitCoord</Name>
        <Value>True</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>
