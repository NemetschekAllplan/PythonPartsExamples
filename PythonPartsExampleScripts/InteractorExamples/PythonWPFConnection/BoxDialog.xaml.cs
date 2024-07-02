using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace PythonWPFConnection
{
    public partial class NameValueArgs
    {
        public NameValueArgs(string name, double value)
        {
            Name  = name;
            Value = value;
        }

        public string Name
        {
            set; get;
        }

        public double Value
        {
            set; get;
        }
    };

    public delegate void UpdateValueEventHandler(object sender, NameValueArgs e);

    /// <summary>
    /// Box dialog class
    /// </summary>
    public partial class BoxDialog : Window
    {
        public BoxDialog(double length, double width, double height)
        {
            m_BoxLength = length;
            m_BoxWidth  = width;
            m_BoxHeight = height;

            InitializeComponent();

            this.DataContext = this;
        }

        public double BoxLength
        {
            get { return m_BoxLength; }
            set
            {
                m_BoxLength = value;

                UpdateValue(this, new NameValueArgs("Length",value));
            }
        }

        public double BoxWidth
        {
            get { return m_BoxWidth; }
            set
            {
                m_BoxWidth = value;

                UpdateValue(this,new NameValueArgs("Width",value));
            }
        }

        public double BoxHeight
        {
            get { return m_BoxHeight; }
            set
            {
                m_BoxHeight = value;

                UpdateValue(this,new NameValueArgs("Height",value));
            }
        }


        private double m_BoxLength;
        private double m_BoxWidth;
        private double m_BoxHeight;

        public event UpdateValueEventHandler UpdateValue;
    }
}
