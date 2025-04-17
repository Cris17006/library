# -*- coding: utf-8 -*-
{
    'name': "Library Book Checkout",

    'summary': "Members can borrow books from the library.",

    'author': "Cristian",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['library_member', 'mail'],
    'application': False,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/checkout_mass_message_wizard_view.xml',
        'views/library_menu.xml',
        'views/checkout_view2.xml',
        'views/checkout_kanban_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/library_checkout_stage.xml',
    ],

    'assets': {
        'web.assets_backend': [
            "library_checkout/static/src/css/checkout.css",
            "library_checkout/static/src/js/checkout.js",
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

