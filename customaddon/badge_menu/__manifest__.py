# -*- coding: utf-8 -*-
{
    'name': "Showing a menu badge in Odoo",

    'summary': """
        Showing a menu badge in Odoo
        """,

    'description': """
        Showing a menu badge in Odoo 
    """,

    'author': "mrthanh.ledinh@outlook.com",
    'website': "",
    'category': 'Tools',
    'version': '0.1',
    "license": "",

    # any module necessary for this one to work correctly
    'images': ['static/description/icon.png'],
    'depends': ['base', 'web'],
    "data": [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
