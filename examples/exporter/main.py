"""
This script uses the `export_theme` function from the `qt_material` package to generate
a custom Qt theme based on the 'dark_teal.xml' configuration. It defines additional style
parameters such as font, colors, and density scale, and outputs a QSS and RCC resource
bundle in the 'theme' directory for use in PySide6 applications.
"""

from qt_material import export_theme

extra = {

    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'monoespace',
    'font_size': '13px',
    'line_height': '13px',

    # Density Scale
    'density_scale': '0',

    # environ
    'pyside6': True,
    'linux': False,

}


export_theme(theme='dark_teal.xml', qss='dark_teal.qss', rcc='resources.rcc',
             output='theme', prefix='icon:/', invert_secondary=False, extra=extra)

