<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\AnyValueByTypeControls.py</Name>
        <Title>AnyValueByType example</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>…
    <Constants>
        <Constant>
            <Name>ADD_CONTROL_BEGINNING</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>ADD_CONTROL_END</Name>
            <Value>1002</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>REMOVE_CONTROL</Name>
            <Value>1000</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Page1</Text>

        <Parameter>
            <Name>EditControlExp</Name>
            <Text>Edit control by value type</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>EditControlValueType</Name>
                <Text>Value type</Text>
                <Value>Length</Value>
                <ValueList>Angle|Double|Integer|Length|String</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>EditControlMinValue</Name>
                <Text>Min value</Text>
                <Value>{"value_type": "Length", "text": "Min value", "value": "0", "value_list": "", "min_value": "", "max_value": "10000"}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=EditControlValueType;max_value=EditControlMaxValue</Constraint>
            </Parameter>

            <Parameter>
                <Name>EditControlMaxValue</Name>
                <Text>Max value</Text>
                <Value>{"value_type": "Length", "text": "Max value", "value": "10000", "value_list": "", "min_value": "0", "max_value": ""}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=EditControlValueType;min_value=EditControlMinValue</Constraint>
            </Parameter>

            <Parameter>
                <Name>EditControl</Name>
                <Text></Text>
                <Value>{"value_type": "Length", "text": "Edit control", "value": "1000", "value_list": "", "min_value": "0", "max_value": "10000"}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=EditControlValueType;min_value=EditControlMinValue;max_value=EditControlMaxValue</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>OtherControlsExp</Name>
            <Text>Other controls by value type</Text>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>OtherControlValueType</Name>
                <Text>Value type</Text>
                <Value>CheckBox</Value>
                <ValueList>CheckBox|Pen|Stroke|Color|Layer|Hatch|Pattern|Font|ReinfSteelGrade|ReinfConcreteGrade|Separator</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>OtherControl</Name>
                <Text></Text>
                <Value>{"value_type": "CheckBox", "text": "Other control", "value": "", "value_list": "", "min_value": "", "max_value": ""}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=OtherControlValueType</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ComboBoxExp</Name>
            <Text>Combo box by value type</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ComboBoxValueType</Name>
                <Text>Value type</Text>
                <Value>LengthComboBox</Value>
                <ValueList>AngleComboBox|DoubleComboBox|IntegerComboBox|LengthComboBox|StringComboBox</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ComboBoxMinValue</Name>
                <Text>Min value</Text>
                <Value>{"value_type": "Length", "text": "Min value", "value": "0", "value_list": "", "min_value": "", "max_value": ""}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=ComboBoxValueType.replace("ComboBox", "")</Constraint>
            </Parameter>

            <Parameter>
                <Name>ComboBoxMaxValue</Name>
                <Text>Max value</Text>
                <Value>{"value_type": "Length", "text": "Max value", "value": "10000", "value_list": "", "min_value": "", "max_value": ""}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=ComboBoxValueType.replace("ComboBox", "")</Constraint>
            </Parameter>

            <Parameter>
                <Name>ComboBox</Name>
                <Text></Text>
                <Value>{"value_type": "LengthComboBox", "text": "Combo box", "value": "1000", "value_list": "1000|2000|3000|4000|5000", "min_value": "0", "max_value": "10000"}</Value>
                <ValueType>AnyValueByType</ValueType>
                <Constraint>value_type=ComboBoxValueType;min_value=ComboBoxMinValue;max_value=ComboBoxMaxValue</Constraint>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander</Name>
            <Text>List with any values</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>AnyValueByTypeList</Name>
                <Text> </Text>
                <Value>[{'value_type': 'Integer', 'text': 'Integer value', 'value': '1', 'value_list': '', 'min_value': '0', 'max_value': ''};{'value_type': 'Double', 'text': 'Double value', 'value': '1.5', 'value_list': '', 'min_value': '', 'max_value': '10'};{'value_type': 'Length', 'text': 'Length value', 'value': '2000', 'value_list': '', 'min_value': '', 'max_value': ''};{'value_type': 'CheckBox', 'text': 'Checkbox', 'value': 'False', 'value_list': '', 'min_value': '', 'max_value': ''};{'value_type': 'StringComboBox', 'text': 'Language', 'value': 'German', 'value_list': 'German|English|French|Italian', 'min_value': '', 'max_value': ''}]</Value>
                <ValueType>AnyValueByType</ValueType>
            </Parameter>

            <Parameter>
                <Name>Separator</Name>
                <ValueType>Separator</ValueType>
            </Parameter>

            <Parameter>
                <Name>DynamicValueListRow</Name>
                <Text>Add/remove controls</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>AddEndButton</Name>
                    <Text>Add at the end</Text>
                    <EventId>ADD_CONTROL_END</EventId>
                    <Value>18925</Value>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>AddStartButton</Name>
                    <Text>Add at the beginning</Text>
                    <EventId>ADD_CONTROL_BEGINNING</EventId>
                    <Value>18927</Value>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>Button </Name>
                    <Text>Remove last control</Text>
                    <EventId>REMOVE_CONTROL</EventId>
                    <Value>18943</Value>
                    <ValueType>PictureResourceButton</ValueType>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>NewControlValueType</Name>
                <Text>Value type</Text>
                <Value>String</Value>
                <ValueList>Text|String|Integer|Double|Length|CheckBox|StringComboBox|IntegerComboBox|Separator</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>NewControlText</Name>
                <Text>Text</Text>
                <Value>This goes on the left side</Value>
                <ValueType>String</ValueType>
                <Visible>NewControlValueType != "Separator"</Visible>
            </Parameter>
            <Parameter>
                <Name>NewControlValueList</Name>
                <Text>Value list</Text>
                <Value>Separate|entries|with|pipes</Value>
                <ValueType>String</ValueType>
                <Visible>"ComboBox" in NewControlValueType</Visible>
            </Parameter>
        </Parameter>
    </Page>
</Element>
