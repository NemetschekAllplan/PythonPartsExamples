<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>InteractorExamples\General\Events.py</Name>
    <Title>Events</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Constants>
    <Constant>
      <Name>FIRST_BUTTON_EVENT</Name>
      <Value>1001</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>SECOND_BUTTON_EVENT</Name>
      <Value>2001</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>FirstPage</Name>
    <Text>First page</Text>
    <Parameters>
      <Parameter>
        <Name>EventsToPrint</Name>
        <Text>Events to print</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PrintOnMouseLeave</Name>
            <Text>on_mouse_leave</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>PrintOnPreviewDraw</Name>
            <Text>on_preview_draw</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
          </Parameter>
          <Parameter>
            <Name>ProcessMouseMsgRow</Name>
            <Text>process_mouse_msg</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL:1</Value>
            <Parameters>
              <Parameter>
                <Name>InfoPicture</Name>
                <Text>This event is triggered with every mouse move.
Uncheck the box, to reduce the amout of text printed in the trace.</Text>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>Picture</ValueType>
              </Parameter>
              <Parameter>
                <Name>PrintProcessMouseMsg</Name>
                <Text/>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Others</Name>
            <Text>others</Text>
            <Value>True</Value>
            <ValueType>CheckBox</ValueType>
            <Enable>False</Enable>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Buttons</Name>
        <Text>Button events</Text>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>FirstButtonRow</Name>
            <Text>Trigger on_control_event 1001</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Button</Name>
                <Text>Press me!</Text>
                <EventId>FIRST_BUTTON_EVENT</EventId>
                <ValueType>Button</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>FirstButtonRow</Name>
            <Text>Trigger on_control_event 2001</Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>Button</Name>
                <Text>Press me!</Text>
                <EventId>SECOND_BUTTON_EVENT</EventId>
                <ValueType>Button</ValueType>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>ReferencePointButton</Name>
            <Text>Change the reference point</Text>
            <Value>AllplanPalette.RefPointPosition.eCenterCenter</Value>
            <ValueType>RefPointButton</ValueType>
            <EnumList2>AllplanPalette.RefPointButtonType.eCornersCenter</EnumList2>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>SecondPage</Name>
    <Text>Switch me!</Text>
    <Parameters>
      <Parameter>
        <Name>EditControlsExpander</Name>
        <Text>Edit controls</Text>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>StringParameter</Name>
            <Text>Type something here</Text>
            <Value/>
            <ValueType>String</ValueType>
          </Parameter>
          <Parameter>
            <Name>SliderParameter</Name>
            <Text>Move the slider</Text>
            <Value>5</Value>
            <ValueType>Integer</ValueType>
            <ValueSlider>True</ValueSlider>
            <MinValue>1</MinValue>
            <MaxValue>10</MaxValue>
            <IntervalValue>1</IntervalValue>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DialogControlsExpander</Name>
        <Text>Dialog controls</Text>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>ColorID</Name>
            <Text>Color</Text>
            <Value>255</Value>
            <ValueType>Integer</ValueType>
            <ValueDialog>RGBColorDialog</ValueDialog>
          </Parameter>
          <Parameter>
            <Name>AttributeID</Name>
            <Text>Change the attribute</Text>
            <Value>222</Value>
            <ValueType>AttributeId</ValueType>
            <ValueDialog>AttributeSelection</ValueDialog>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>GeometryControlsExpander</Name>
        <Text>Geometry controls</Text>
        <ValueType>Expander</ValueType>
        <Visible>True</Visible>
        <Parameters>
          <Parameter>
            <Name>Point</Name>
            <Text>Point</Text>
            <Value>Point3D(0,0,0)</Value>
            <ValueType>Point3D</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
</Element>
