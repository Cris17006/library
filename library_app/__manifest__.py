# -*- coding: utf-8 -*-
{
    'name': "Library Management",

    'summary': "Manage library catalog and book lending",

    'description': """
Long description of module's purpose
    """,

    'author': "Cristian",
    'license': "LGPL-3",
    'website': "https://github.com/PacktPublishing/Odoo-15-Development-Essentials",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/templates.xml',
        'views/library_menu.xml',
        'reports/library_book_report.xml',
        'reports/book_catalog.xml',
        'reports/library_publisher_report.xml',
        'reports/publisher_report.xml',
        'views/book_list_template.xml',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/res.partner.csv',
        'data/library.book.csv',
        'data/book_demo.xml',
    ],
}

