<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ServiceExamples\AttributeService.py</Name>
    <Title>AttributeService</Title>
    <Version>1.0</Version>
    <ReadLastInput>True</ReadLastInput>
  </Script>
  <Page>
    <Name>AttributeService</Name>
    <Text>Attribute access</Text>
    <Parameters>
      <Parameter>
        <Name>FromId</Name>
        <Text>Data from ID</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AttributeIDIn</Name>
            <Text>ID</Text>
            <Value>1</Value>
            <ValueType>Integer</ValueType>
          </Parameter>
          <Parameter>
            <Name>AttributeNameByID</Name>
            <Text>Name</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeTypeByID</Name>
            <Text>Type</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeDefaultValueByID</Name>
            <Text>Default value</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeControlTypeByID</Name>
            <Text>Control type</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeInputListByID</Name>
            <Text>List values</Text>
            <Value>["abc"]</Value>
            <Dimensions/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>FromName</Name>
        <Text>Data from name</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AttributeNameIn</Name>
            <Text>Name</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>AttributeIDByName</Name>
            <Text>ID</Text>
            <Value/>
            <ValueType>Integer</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeTypeByName</Name>
            <Text>Type</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeDefaultValueByName</Name>
            <Text>Default value</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>AttributeDialog</Name>
        <Text>Attribute dialog</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>AttributeByDlg</Name>
            <Text>Select attribute</Text>
            <Value/>
            <ValueType>Integer</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>AttributeNameByDlg</Name>
            <Text>Name</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Enable>False</Enable>
          </Parameter>
          <Parameter>
            <Name>AttributeIDByDlg</Name>
            <Text>ID</Text>
            <Value/>
            <ValueType>Integer</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>UserAttribute</Name>
    <Text>Add user attribute</Text>
    <Parameters>
      <Parameter>
        <Name>UserAttribute</Name>
        <Text>Add user attribute</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
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
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>UserAttributeDefaultValue</Name>
            <Text>Default value</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>UserAttributeMinValue</Name>
            <Text>minimal value</Text>
            <Value/>
            <ValueType>Double</ValueType>
            <Visible>UserAttributeType in ["Double", "Integer", "DoubleVec", "IntegerVec"]</Visible>
          </Parameter>
          <Parameter>
            <Name>UserAttributeMaxValue</Name>
            <Text>maximal value</Text>
            <Value/>
            <ValueType>Double</ValueType>
            <Visible>UserAttributeType in ["Double", "Integer", "DoubleVec", "IntegerVec"]</Visible>
          </Parameter>
          <Parameter>
            <Name>UserAttributeDim</Name>
            <Text>Dimension</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>UserAttributeControlType</Name>
            <Text>Control type</Text>
            <Value/>
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
            <Parameters>
              <Parameter>
                <Name>CreateUserAttribute</Name>
                <Text>Create user attribute</Text>
                <EventId>1000</EventId>
                <ValueType>Button</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>UserAttributeSeparator1</Name>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>UserAttributeID</Name>
            <Text>Created attribute ID</Text>
            <Value/>
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
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
