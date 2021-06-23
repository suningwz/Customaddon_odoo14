# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Hospital Management Software',
    'sequence': -100,
    'description': """Hospital Management Software""",
    'category': 'Productivity',
    'website': 'https://www.odoomates.tech',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'mail', ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'views/patient.xml',
        'views/kid_patient.xml',
        'views/patient_gender.xml',
        'views/appointment.xml',
        'views/doctor_view.xml',
        'views/sale_order_inherit_view.xml',


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
