# -*- coding: utf-8 -*-
{
    'name': "Shop Products",
    'summary': "Generate product info automatically",
    'description': """
        Write the product name and the module generate info if exists in database api
    """,
    'author': "Cristian",
    'website': "https://fakeapi.platzi.com/en",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '18.1',
    # any module necessary for this one to work correctly
    'depends': ['library_app','base', 'product'],
    # always loaded
    'data': [
        #'security/ir.model.access.csv',  
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # external dependencies
    'external_dependencies': {
        'python': ['requests'],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}