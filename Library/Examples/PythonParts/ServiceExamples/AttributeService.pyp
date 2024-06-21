<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>ServiceExamples\AttributeService.py</Name>
        <Title>AttributeService</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    <Page>
        <Name>AttributeService</Name>
        <Text>Attribute access</Text>

        <Parameter>
            <Name>FromId</Name>
            <Text>Data from ID</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AttributeIDIn</Name>
                <Text>ID</Text>
                <Value>1</Value>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>AttributeNameByID</Name>
                <Text>Name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeTypeByID</Name>
                <Text>Type</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeDefaultValueByID</Name>
                <Text>Default value</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeControlTypeByID</Name>
                <Text>Control type</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeInputListByID</Name>
                <Text>List values</Text>
                <Value>["abc"]</Value>
                <Dimensions></Dimensions>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>FromName</Name>
            <Text>Data from name</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AttributeNameIn</Name>
                <Text>Name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>

            <Parameter>
                <Name>AttributeIDByName</Name>
                <Text>ID</Text>
                <Value></Value>
                <ValueType>Integer</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeTypeByName</Name>
                <Text>Type</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeDefaultValueByName</Name>
                <Text>Default value</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>AttributeDialog</Name>
            <Text>Attribute dialog</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AttributeByDlg</Name>
                <Text>Select attribute</Text>
                <Value></Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>AttributeSelection</ValueDialog>
            </Parameter>


            <Parameter>
                <Name>AttributeNameByDlg</Name>
                <Text>Name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
                <Enable>False</Enable>
            </Parameter>
            <Parameter>
                <Name>AttributeIDByDlg</Name>
                <Text>ID</Text>
                <Value></Value>
                <ValueType>Integer</ValueType>
                <Enable>False</Enable>
            </Parameter>
        </Parameter>
    </Page>
    <Page>
        <Name>UserAttribute</Name>
        <Text>Add user attribute</Text>

        <Parameter>
            <Name>UserAttribute</Name>
            <Text>Add user attribute</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>UserAttributeType</Name>
                <Text>AttributeType</Text>
                <Value>String</Value>
                <ValueList>String|Double|Integer|Date|Enum</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>UserAttributeName</Name>
                <Text>Attribute name</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>UserAttributeDefaultValue</Name>
                <Text>Default value</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>UserAttributeMinValue</Name>
                <Text>minimal value</Text>
                <Value></Value>
                <ValueType>Double</ValueType>
                <Visible>UserAttributeType in ["Double", "Integer", "DoubleVec", "IntegerVec"]</Visible>
            </Parameter>
            <Parameter>
                <Name>UserAttributeMaxValue</Name>
                <Text>maximal value</Text>
                <Value></Value>
                <ValueType>Double</ValueType>
                <Visible>UserAttributeType in ["Double", "Integer", "DoubleVec", "IntegerVec"]</Visible>
            </Parameter>
            <Parameter>
                <Name>UserAttributeDim</Name>
                <Text>Dimension</Text>
                <Value></Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>UserAttributeControlType</Name>
                <Text>Control type</Text>
                <Value></Value>
                <ValueList>
if UserAttributeType == "Date":
    return "Edit"

if UserAttributeType in ["String", "Double"]:
    return "Edit|ComboBox"

if UserAttributeType == "Integer":
    return "Edit|ComboBoxHatch|ComboBoxPattern|ComboBoxFilling|CheckBox|ComboBox"

if UserAttributeType == "Enum":
    return "ComboBoxFixed"
                </ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>UserAttributeListValuesCount</Name>
                <Text>list value count</Text>
                <Value>3</Value>
                <ValueType>Integer</ValueType>
                <Visible>UserAttributeControlType in ["ComboBox", "ComboBoxFixed"]</Visible>
            </Parameter>
            <Parameter>
                <Name>UserAttributeListValues</Name>
                <Text>list values</Text>
                <Value>["", "", ""]</Value>
                <Dimensions>UserAttributeListValuesCount</Dimensions>
                <ValueType>String</ValueType>
                <Visible>UserAttributeControlType in ["ComboBox", "ComboBoxFixed"]</Visible>
            </Parameter>

            <Parameter>
                <Name>CreateUserAttribute</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>CreateUserAttribute</Name>
                    <Text>Create user attribute</Text>
                    <EventId>1000</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>UserAttributeSeparator1</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>UserAttributeID</Name>
                <Text>Created attribute ID</Text>
                <Value></Value>
                <ValueType>Integer</ValueType>
                <Enable>False</Enable>
            </Parameter>

            <Parameter>
                <Name>UserAttributeSeparator1</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>UserAttribute</Name>
                <Text>User attribute</Text>
                <Value>1</Value>
                <ValueType>Attribute</ValueType>
                <AttributeId>55028</AttributeId>
            </Parameter>

        </Parameter>
    </Page>
</Element>
