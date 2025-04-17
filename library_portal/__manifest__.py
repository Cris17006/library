# -*- coding: utf-8 -*-
{
    'name': "Library Portal",

    'summary': "Portal for Library Members",

    'author': "Cristian",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['library_checkout', 'portal'],

    'assets': {
        "web.assets_backend": [
            "library_portal/static/src/css/library.css",
            "library_portal/static/src/css/catalog.css",
            "library_portal/static/src/css/book_info.css",
        ],
        "web.assets_frontend": [
            # "library_portal/static/src/js/catalog_button.js",
    ],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/library_security.xml',
        'views/main_templates.xml',
        'views/portal_templates.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

