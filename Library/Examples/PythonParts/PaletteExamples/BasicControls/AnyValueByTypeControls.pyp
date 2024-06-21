<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>PaletteExamples\BasicControls\AnyValueByTypeControls.py</Name>
        <Title>AnyValueByType example</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
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
                <Value>[_]</Value>
                <ValueType>AnyValueByType</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
