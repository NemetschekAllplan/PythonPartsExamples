<?xml version='1.0' encoding='UTF-8'?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>ServiceExamples\SaveWindowToImage.py</Name>
    <Title>Save viewport to image</Title>
    <Version>1.0</Version>
    <Interactor>True</Interactor>
  </Script>
  <Page>
    <Name>Page</Name>
    <Text>Save window to file</Text>
    <Parameters>
      <Parameter>
        <Name>ImageFilePath</Name>
        <Text>Image location</Text>
        <Value/>
        <ValueType>String</ValueType>
        <ValueDialog>SaveFileDialog</ValueDialog>
        <FileFilter>JPEG(*.jpg)|*.jpg|Portable Network Graphics(*.png)|*.png|Tagged Image File Format(*.tif)|*.tif|Mac PICT(*.pct)|*.pct|Windows Bitmap(*.bmp)|*.bmp|Personal Computer eXchange(*.pcx)|*.pcx|Photoshop Document(*.psd)|*.psd|Truevision Graphics Adapter(*.tga)|*.tga|</FileFilter>
        <FileExtension>bmp</FileExtension>
      </Parameter>
      <Parameter>
        <Name>SetImageSize</Name>
        <Text>Image size</Text>
        <Value>0</Value>
        <ValueType>RadioButtonGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>ImageSizeAsWindow</Name>
            <Text>as window size</Text>
            <Value>0</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
          <Parameter>
            <Name>ImageSizePredefined</Name>
            <Text>defined size</Text>
            <Value>1</Value>
            <ValueType>RadioButton</ValueType>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>ImageSize</Name>
        <Text>Image size (px)</Text>
        <Value>(0|0)</Value>
        <ValueType>tuple(Integer,Integer)</ValueType>
        <Visible>SetImageSize == 1, SetImageSize == 1</Visible>
      </Parameter>
    </Parameters>
  </Page>
</Element>
