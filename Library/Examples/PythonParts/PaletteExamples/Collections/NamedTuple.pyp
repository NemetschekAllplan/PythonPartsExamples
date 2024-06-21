<?xml version="1.0" encoding="utf-8"?>
<Element>
    <LanguageFile>NamedTuple</LanguageFile>
    <Script>
        <Name>PaletteExamples\Collections\NamedTuple.py</Name>
        <Title>NamedTuple</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Reinforcement1</Name>
        <Text>Single element</Text>

        <Parameter>
            <Name>Expander</Name>
            <Text>As block</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>UShape</Name>
                <Text>,Diameter,Concrete cover,Top length,Bottom length</Text>
                <Value>Param01.png|12|30|1000|2000</Value>     <!--Separate by |-->
                <ValueType>namedtuple(Picture,ReinfBarDiameter,ReinfConcreteCover,Length,Length)</ValueType>
                <NamedTuple>
                    <TypeName>UShape</TypeName>
                    <FieldNames>Picture,Diameter,Cover,Length1,Length2</FieldNames>
                </NamedTuple>
                <MinValue>,,,100,200</MinValue>
                <!--<MaxValue></MaxValue>
                <Visible></Visible>
                <Enable></Enable>-->
            </Parameter>

            <Parameter>
                <Name>DisableBlockName</Name>
                <Text>Disable name</Text>
                <Value>Length2</Value>
                <ValueList>None|Diameter|Cover|Length1|Length2</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander</Name>
            <Text>As row</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>LShape</Name>
                <Text>L Shape</Text>
                <Value>14|25|1200</Value>
                <ValueType>namedtuple(ReinfBarDiameter,ReinfConcreteCover,Length)</ValueType>
                <NamedTuple>
                    <TypeName>LShape</TypeName>
                    <FieldNames>Diameter,Cover,Length1</FieldNames>
                </NamedTuple>
            </Parameter>

            <Parameter>
                <Name>HideRowName</Name>
                <Text>Hide name</Text>
                <Value>None</Value>
                <ValueList>None|Diameter|Cover|Length1</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Reinforcement2</Name>
        <Text>Block list</Text>

        <Parameter>
            <Name>UShapeList</Name>
            <Text>,Diameter,Concrete cover,Top length,Bottom length,"Group " + str($list_row + 1),Edit</Text>
            <Value>[Param01.png|12|30|1000|2000|0;
                    Param02.png|12|30|1000|2000|0;
                    Param03.png|12|30|1000|2000|0]
            </Value>
            <EventId>0,0,0,0,0,1000,0</EventId>
            <ValueType>namedtuple(Picture,ReinfBarDiameter,ReinfConcreteCover,Length,Length,Button,Separator)</ValueType>
            <NamedTuple>
                <TypeName>UShape</TypeName>
                <FieldNames>Picture,Diameter,Cover,Length1,Length2,Button</FieldNames>
            </NamedTuple>
            <MinValue>,,,100,200</MinValue>
        </Parameter>

        <Parameter>
            <Name>HideRow</Name>
            <Text>Hide row</Text>
            <Value>2</Value>
            <ValueType>Integer</ValueType>
            <MinValue>0</MinValue>
            <MaxValue>3</MaxValue>
        </Parameter>

        <Parameter>
            <Name>DisableColumn</Name>
            <Text>Disable name (column)</Text>
            <Value>Length2</Value>
            <ValueList>None|Diameter|Cover|Length1|Length2</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>ClickedButtonExpander</Name>
            <Text>Clicked button</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ButtonEventID</Name>
                <Text>Event ID</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>ButtonIndex</Name>
                <Text>Index</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>Reinforcement3</Name>
        <Text>List</Text>

        <Parameter>
            <Name>ItemCount</Name>
            <Text>Number of items</Text>
            <Value>4</Value>
            <MinValue>0</MinValue>
            <MaxValue>10</MaxValue>
            <ValueType>Integer</ValueType>
        </Parameter>

        <Parameter>
            <Name>StirrupList</Name>
            <Text></Text>
            <Value>[ |12|30|True;
                     |12|30|True;
                     |12|30|True;
                     |12|30|True]
            </Value>
            <ValueType>namedtuple(DisplayText,ReinfBarDiameter,ReinfConcreteCover,CheckBox)</ValueType>
            <NamedTuple>
                <TypeName>StirrupList</TypeName>
                <FieldNames>RowText,Diameter,Cover,Select</FieldNames>
            </NamedTuple>
            <Dimensions>ItemCount</Dimensions>
            <Enable>True,StirrupList[$list_row].Select,StirrupList[$list_row].Select,True</Enable>
        </Parameter>

        <Parameter>
            <Name>HideColumn</Name>
            <Text>Hide name (column)</Text>
            <Value>Cover</Value>
            <ValueList>None|Diameter|Cover</ValueList>
            <ValueType>StringComboBox</ValueType>
        </Parameter>
    </Page>
</Element>
