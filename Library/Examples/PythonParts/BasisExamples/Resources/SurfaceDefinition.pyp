<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\Resources\SurfaceDefinition.py</Name>
        <Title>Expander</Title>
        <Version>1.0</Version>
    </Script>
    <Constants>
        <Constant>
            <Name>CREATE_SURFACE</Name>
            <Value>1001</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>DELETE_DIFFUSE_BITMAP</Name>
            <Value>1002</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>DELETE_BUMP_BITMAP</Name>
            <Value>1003</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>DELETE_ROUGHNESS_BITMAP</Name>
            <Value>1004</Value>
            <ValueType>Integer</ValueType>
        </Constant>
        <Constant>
            <Name>DELETE_REFLECTION_BITMAP</Name>
            <Value>1005</Value>
            <ValueType>Integer</ValueType>
        </Constant>
    </Constants>
    <Page>
        <Name>Page1</Name>
        <Text>Geometry</Text>

        <Parameter>
            <Name>Cube</Name>
            <Text>Cube</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>5000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>SurfaceExpander</Name>
            <Text>Surface</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Surface</Name>
                <Text>Surface</Text>
                <Value></Value>
                <DisableButtonIsShown>True</DisableButtonIsShown>
                <ValueType>MaterialButton</ValueType>
            </Parameter>
        </Parameter>
    </Page>

    <Page>
        <Name>Surface</Name>
        <Text>Surface</Text>

        <Parameter>
            <Name>SurfaceExpander</Name>
            <Text>Create surface</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RelativePathAndName</Name>
                <Text>Relative path and name</Text>
                <Value>PythonPartsExamples\CubeSurface</Value>
                <ValueType>String</ValueType>
            </Parameter>

            <Parameter>
                <Name>CreateSurfaceRow</Name>
                <Text> </Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>CreateSurface</Name>
                    <Text>Create surface</Text>
                    <EventId>CREATE_SURFACE</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>ColorExpander</Name>
            <Text>Color</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>DiffuseColorBitmapRow</Name>
                <Text>Bitmap</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>DiffuseColorBitmap</Name>
                    <Text>Bitmap</Text>
                    <Value></Value>
                    <ValueType>PictureButton</ValueType>
                    <ValueDialog>OpenFileDialog</ValueDialog>
                    <FileFilter>Bitmap-files(*.png)|*.png|</FileFilter>
                    <FileExtension>*.png</FileExtension>
                    <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
                    <HeightInRow>70</HeightInRow>
                    <Persistent>MODEL_AND_FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>DiffuseColorBitmapDel</Name>
                    <Text>Delete the bitmap</Text>
                    <EventId>DELETE_DIFFUSE_BITMAP</EventId>
                    <Value>10051</Value>
                    <ValueType>PictureResourceButton</ValueType>
                    <WidthInRow>5</WidthInRow>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>DiffuseColor</Name>
                <Text>Color</Text>
                <Value>255</Value>
                <ValueType>Integer</ValueType>
                <ValueDialog>RGBColorDialog</ValueDialog>
            </Parameter>
            <Parameter>
                <Name>DiffuseReflectivity</Name>
                <Text>Diffuse reflection</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>100</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>TransparencyExpander</Name>
            <Text>Transparency</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Transparency</Name>
                <Text>Intensity</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
            <Parameter>
                <Name>Refraction</Name>
                <Text>Refraction</Text>
                <MinValue>1</MinValue>
                <MaxValue>2.5</MaxValue>
                <Value>1</Value>
                <ValueType>Double</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>LuminanceExpander</Name>
            <Text>Luminance</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Emission</Name>
                <Text>Intensity</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>BumpExpander</Name>
            <Text>Bump</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>BumpBitmapRow</Name>
                <Text>Bitmap</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>BumpBitmap</Name>
                    <Text>Bitmap</Text>
                    <Value></Value>
                    <ValueType>PictureButton</ValueType>
                    <ValueDialog>OpenFileDialog</ValueDialog>
                    <FileFilter>Bitmap-files(*.png)|*.png|</FileFilter>
                    <FileExtension>*.png</FileExtension>
                    <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
                    <HeightInRow>70</HeightInRow>
                    <Persistent>MODEL_AND_FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>BumpBitmapDel</Name>
                    <Text>Delete the bitmap</Text>
                    <EventId>DELETE_BUMP_BITMAP</EventId>
                    <Value>10051</Value>
                    <ValueType>PictureResourceButton</ValueType>
                    <WidthInRow>5</WidthInRow>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>NormalMapStatus</Name>
                <Text>Normal map</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>BumpAmplitude</Name>
                <Text>Intensity</Text>
                <MinValue>-100</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
            <Parameter>
                <Name>ParallaxOffset</Name>
                <Text>Parallax offset</Text>
                <MinValue>-100</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
            <Parameter>
                <Name>ParallaxSamples</Name>
                <Text>Parallax samples</Text>
                <MinValue>2</MinValue>
                <MaxValue>200</MaxValue>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Roughness</Name>
            <Text>Roughness</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>RoughnessBitmapRow</Name>
                <Text>Bitmap</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>RoughnessBitmap</Name>
                    <Text>Bitmap</Text>
                    <Value></Value>
                    <ValueType>PictureButton</ValueType>
                    <ValueDialog>OpenFileDialog</ValueDialog>
                    <FileFilter>Bitmap-files(*.png)|*.png|</FileFilter>
                    <FileExtension>*.png</FileExtension>
                    <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
                    <HeightInRow>70</HeightInRow>
                    <Persistent>MODEL_AND_FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>RoughnessBitmapDel</Name>
                    <Text>Delete the bitmap</Text>
                    <EventId>DELETE_ROUGHNESS_BITMAP</EventId>
                    <Value>10051</Value>
                    <ValueType>PictureResourceButton</ValueType>
                    <WidthInRow>5</WidthInRow>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Roughness</Name>
                <Text>Intensity</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>GlossyReflectionExpander</Name>
            <Text>Glossy reflection</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ReflectionBitmapRow</Name>
                <Text>Bitmap</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>ReflectionBitmap</Name>
                    <Text>Bitmap</Text>
                    <Value></Value>
                    <ValueType>PictureButton</ValueType>
                    <ValueDialog>OpenFileDialog</ValueDialog>
                    <FileFilter>Bitmap-files(*.png)|*.png|</FileFilter>
                    <FileExtension>*.png</FileExtension>
                    <DefaultDirectories>etc|std|usr|prj</DefaultDirectories>
                    <HeightInRow>70</HeightInRow>
                    <Persistent>MODEL_AND_FAVORITE</Persistent>
                </Parameter>
                <Parameter>
                    <Name>ReflectionBitmapDel</Name>
                    <Text>Delete the bitmap</Text>
                    <EventId>DELETE_REFLECTION_BITMAP</EventId>
                    <Value>10051</Value>
                    <ValueType>PictureResourceButton</ValueType>
                    <WidthInRow>5</WidthInRow>
                </Parameter>
            </Parameter>

            <Parameter>
                <Name>Reflection</Name>
                <Text>Intensity</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>

            <Parameter>
                <Name>MultiToneFactor</Name>
                <Text>Coat of lacquer</Text>
                <MinValue>0</MinValue>
                <MaxValue>100</MaxValue>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
                <ValueSlider>True</ValueSlider>
                <IntervalValue>1</IntervalValue>
            </Parameter>
        </Parameter>
    </Page>
</Element>
