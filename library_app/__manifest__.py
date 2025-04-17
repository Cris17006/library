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
    'depends': ['base', 'web'],


    # always loaded
  'data': [
    # Seguridad y accesos
    'security/library_security.xml',
    'security/ir.model.access.csv',

    # Vistas base
    'views/book_view.xml',
    'views/views.xml',
    'views/library_menu.xml',

    # Templates frontend
    'views/book_list_template.xml',
    'views/templates.xml',

    # Reports y sus assets
    'reports/views/library_book_report.xml',
    'reports/views/library_publisher_report.xml',
    'reports/views/publisher_report.xml',
    'reports/views/book_catalog.xml',
    ],


    'assets': {
        'web.report_assets_common': [
        'library_app/static/src/css/reports.css',

        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'data/res.partner.csv',
        'data/library.book.csv',
        'data/book_demo.xml',
    ],
}

